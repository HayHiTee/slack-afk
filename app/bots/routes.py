from flask import jsonify, request, Blueprint

from app import db
from app.bots import bot
from app.bots.models import User
from app.bots.slash_commands import SlackBots
from app.bots.thread import run_thread_fn
from instance.config import  Config

Slack_Bots = SlackBots(User(), db)


@bot.route('/slash', methods=['GET', 'POST'])
def slash():
    data = request.form
    print(data)
    if request.method == "POST":
        verification_token = Config.VERIFICATION_TOKEN
        print(verification_token)
        print(data['token'])
        if data['token'] == verification_token:
            username = data.get("user_id", "invalid_name")
            response_url = data.get("response_url")
            data_text = data['text'].split(" ")
            payload = {"text":"Got it"}
            try:
                hours = Slack_Bots.get_valid_hour(data_text)
            except ValueError:
                msg = "Invalid time"
                payload = {'text': msg, "response_type": "ephemeral"}
                return jsonify(payload)
            if 'lunch' in data_text:
                lunch_payload = Slack_Bots.get_lunch_message(username, hours)
                # Slack_Bots.send_to_response_url(response_url, lunch_payload)
                # Run in separate thread
                run_thread_fn(Slack_Bots.send_to_response_url, url=response_url, payload=lunch_payload)
            elif 'errands' in data_text:
                errand_payload = Slack_Bots.get_errand_message(username, hours)
                # Slack_Bots.send_to_response_url(response_url, errand_payload)
                run_thread_fn(Slack_Bots.send_to_response_url, url=response_url, payload=errand_payload)
            else:
                msg = 'Invalid command!'
                payload = {'text': msg, "response_type": "ephemeral"}
            return jsonify(payload), 200
        else:
            return jsonify({"error": "Not found"})
    elif request.method == "GET":
        return jsonify({"text": "Welcome"})


@bot.route('/slash/auth/redirect', methods=['GET'])
def redirect():
    code = request.args.get('code')
    print(code)
    return Slack_Bots.get_access_token(code)


@bot.route('/hello')
def index():
    return 'Hello, World!'
