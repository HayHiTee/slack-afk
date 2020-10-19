import os


class Config:
    VERIFICATION_TOKEN = os.environ.get('VERIFICATION_TOKEN', "ok")
    SECRET_KEY = 'dev'
    DATABASE = os.path.join('', 'flaskr.sqlite')
    SLACK_BASE_URL = "https://slack.com"
    SLACK_CLIENT_ID = os.environ.get('SLACK_CLIENT_ID')
    SLACK_CLIENT_SECRET = os.environ.get('SLACK_CLIENT_SECRET')
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", 'sqlite:///test.db')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
