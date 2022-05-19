import os
import sys
import slack
from pathlib import Path
from dotenv import load_dotenv
import requests
import logging
from urllib.parse import urlencode
from operator import itemgetter
import json

from flask import Flask, request, redirect
app = Flask(__name__)

logging.basicConfig(level='INFO', format='%(asctime)s-%(levelname)s-%(message)s')

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

SLACK_APP_CLIENT_ID = os.environ['SLACK_APP_CLIENT_ID']
SLACK_APP_CLIENT_SECRET = os.environ['SLACK_APP_CLIENT_SECRET']
OAUTH_CALLBACK = os.environ['OAUTH_CALLBACK']
BASE_URL = "http://127.0.0.1:5000/"


@app.route('/')
def homepage():
    # checks for stored token
    if os.path.exists("creds.json"):
        f = open('creds.json')
        data = json.load(f)
        if data[SLACK_APP_CLIENT_ID]:
            client = slack.WebClient(token=data[SLACK_APP_CLIENT_ID])
            client.chat_postMessage(channel='#bots', text="Hello World", as_user=True)
            return "<h1>Your message was sent :)</h1>", 200

    return '<p>Welcome to the sample Slack OAuth app! Click <a href="/auth/slack">here</a> to log in</p>'


@app.route('/auth/slack', methods=['GET'])
def auth():
    oauth_base = "https://slack.com/oauth/v2/authorize?"
    url = f"{oauth_base}scope=incoming-webhook,commands,chat:write&redirect_uri={OAUTH_CALLBACK}&client_id={SLACK_APP_CLIENT_ID}&user_scope=chat:write"

    return redirect(url)


@app.route('/oauth/slack/callback', methods=['GET'])
def authCallback():
    code = request.args['code']
    app.logger.info('requesting token using %s code' % code)

    tokenResponse = requests.post("https://slack.com/api/oauth.v2.access",
        data={
            "client_id": SLACK_APP_CLIENT_ID,
            "client_secret": SLACK_APP_CLIENT_SECRET,
            "redirect_uri": OAUTH_CALLBACK,
            "code": code
        })
    app.logger.info('status_code: %s' % tokenResponse.status_code)
    app.logger.info('response: %s' % tokenResponse.json())
    authed_user = itemgetter('authed_user')(tokenResponse.json())
    access_token = itemgetter('access_token')(authed_user)

    # store token
    creds = json.dumps({SLACK_APP_CLIENT_ID: access_token}, indent=2)
    with open('creds.json', 'w') as f:
        f.write(creds)
    
    # Sends message
    client = slack.WebClient(token=access_token)
    client.chat_postMessage(channel='#bots', text="Hello World", as_user=True)

    return "<h1>Your message was sent :)</h1>", 200


if __name__ == "__main__":
    app.run(debug=True)