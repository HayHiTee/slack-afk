from flask import current_app

VERIFICATION_TOKEN = current_app.config.get("VERIFICATION_TOKEN")
SLACK_BASE_URL = current_app.config.get("SLACK_BASE_URL")