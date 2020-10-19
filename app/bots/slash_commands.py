import json
from datetime import datetime, timedelta
import pytz
import requests
from flask_sqlalchemy import SQLAlchemy
from flask import redirect

from app.bots.models import User
from app.bots.thread import run_thread_fn
from instance.config import Config


# from instance.config import SLACK_BASE_URL, SLACK_CLIENT_ID, SLACK_CLIENT_SECRET


class SlackBots:
    def __init__(self, user: User, db: SQLAlchemy):
        self.user = user
        self.db = db

    def send_to_response_url(self, url, payload):
        rs = requests.post(url, json=payload, headers=self.get_header())
        print(rs.status_code)
        print(rs.content)

    def get_access_token(self, code):
        access_token_url = f"{Config.SLACK_BASE_URL}/api/oauth.v2.access"
        payload = {
            "code": code,
            "client_id": Config.SLACK_CLIENT_ID,
            "client_secret": Config.SLACK_CLIENT_SECRET,
            "redirect_uri": ""
        }
        print(payload)
        rs = requests.get(access_token_url, params=payload, headers=self.get_header())
        print(rs.status_code)
        print(rs.content)
        if 200 <= rs.status_code < 300:
            access_token_data = json.loads(rs.text)
            if access_token_data.get("ok"):
                self.add_to_user(access_token_data)
            print(access_token_data)
            return redirect("https://app.slack.com/client/", code=302)
            # return access_token_data

    @staticmethod
    def get_valid_hour(data_text):
        hours = 1
        try:
            hours = data_text[1]
        except IndexError:
            print("hour not specified")
        return float(hours)

    def get_lunch_message(self, username, hours):
        utc_date = self.add_to_time(hours)
        current_time = self.parse_to_slack_time(utc_date)
        text = f'<@{username}> is out to lunch till {current_time}'
        # self.update_user_status(user_id=username,
        #                         status_text="Out to Lunch",
        #                         expiration_time=int(utc_date.timestamp()),
        #                         emoji=":fries:")
        # Run in separate thread
        run_thread_fn(self.update_user_status, user_id=username,
                      status_text="Out to Lunch",
                      expiration_time=int(utc_date.timestamp()),
                      emoji=":fries:")
        return {'text': text, "response_type": "in_channel", "delete_original": "true", }

    def get_errand_message(self, username, hours):
        utc_date = self.add_to_time(hours)
        current_time = self.parse_to_slack_time(utc_date)
        text = f'<@{username}> is out on errands till {current_time}'
        # self.update_user_status(user_id=username,
        #                         status_text="Out on errand",
        #                         expiration_time=int(utc_date.timestamp()),
        #                         emoji=":mountain_railway:")
        # Run in separate thread
        run_thread_fn(self.update_user_status, user_id=username,
                      status_text="Out on errand",
                      expiration_time=int(utc_date.timestamp()),
                      emoji=":mountain_railway:")
        return {'text': text, "response_type": "in_channel"}

    @staticmethod
    def add_to_time(hours):
        utc = pytz.utc
        utc_date = utc.localize(datetime.utcnow() + timedelta(hours=hours))
        return utc_date

    @staticmethod
    def parse_to_slack_time(utc_date):
        alt_time = utc_date.timetz().strftime("%I:%M %p")  # Provide alternative time in AM/PM
        slack_time = f"<!date^{int(utc_date.timestamp())}^{{time}}|{alt_time} UCT>"
        print(slack_time)
        return slack_time  # return time in AM and PM

    def update_user_status(self, user_id, status_text, expiration_time, emoji, ):
        slack_base_url = Config.SLACK_BASE_URL
        status_url = f"{slack_base_url}/api/users.profile.set"
        print(status_url)
        payload = {
            "profile": {
                "status_text": status_text,
                "status_emoji": emoji,
                "status_expiration": expiration_time
            }
        }
        user = self.get_user_by_auth_user_id(user_id)
        if user:
            print(payload)
            rs = requests.post(status_url, json=payload, headers=self.get_header(user.access_token))
            print(rs.status_code)
            print(rs.text)

    @staticmethod
    def get_header(token=""):
        headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': f'Bearer {token}'}
        print(headers)
        return headers

    def add_to_user(self, data):
        user = self.get_user_by_auth_user_id(data.get("authed_user").get("id"))
        self.user = user if user else self.user
        self.user.access_token = data.get("authed_user").get("access_token")
        self.user.auth_user_id = data.get("authed_user").get("id")
        self.user.scope = data.get("scope")
        self.user.team_id = data.get("team").get("id")
        self.user.team_name = data.get("team").get("name")

        # Check if user already exist
        if not user:
            self.db.session.add(self.user)
        self.db.session.commit()

    def get_user_by_auth_user_id(self, auth_user_id):
        user = self.user.query.filter_by(auth_user_id=auth_user_id).first()
        if user:
            print("access_token", user.access_token)
        return user
