import os
import slack
from pathlib import Path
from dotenv import load_dotenv
import requests
import logging
from operator import itemgetter
import json
from slack.errors import SlackApiError
from slackeventsapi import SlackEventAdapter
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events', app)

logging.basicConfig(level='INFO', format='%(asctime)s-%(levelname)s-%(message)s')

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

SLACK_APP_CLIENT_ID = os.environ['SLACK_APP_CLIENT_ID']
SLACK_APP_CLIENT_SECRET = os.environ['SLACK_APP_CLIENT_SECRET']
OAUTH_CALLBACK = os.environ['OAUTH_CALLBACK']
BASE_URL = "http://127.0.0.1:5000"


@app.route('/')
def homepage():
    # checks for stored token
    if os.path.exists("creds.json"):
        return '<h1>You have already been authenticated</h1>'
    return '<p>Welcome to the sample Slack OAuth app! Click <a href="/auth/slack">here</a> to log in</p>'


@app.route('/auth/slack', methods=['GET'])
def auth():
    oauth_base = "https://slack.com/oauth/v2/authorize?"
    url = f"{oauth_base}redirect_uri={OAUTH_CALLBACK}&client_id={SLACK_APP_CLIENT_ID}&user_scope=chat:write,channels:write,groups:write,im:write,mpim:write,channels:read,groups:read,im:read,mpim:read"

    return redirect(url)


@app.route('/oauth/slack/callback', methods=['POST'])
def authCallback():
    code = request.json['code']
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
    creds = json.dumps({"access_token": access_token}, indent=2)
    with open('creds.json', 'w') as f:
        f.write(creds)

    user_info = {"userId": tokenResponse.json()['authed_user']['id'], "appId": tokenResponse.json()['app_id']}
    return jsonify(user_info)


@app.route('/slack/send', methods=['POST'])
def sendMessage():
    if os.path.exists("creds.json"):
        try:
            channel = request.json['channel']
            message = request.json['message']
            f = open('creds.json')
            data = json.load(f)
            if data['access_token']:
                client = slack.WebClient(token=data['access_token'])
                client.chat_postMessage(channel=channel, text=message, as_user=True)
                return "<h1>Your message was sent :)</h1>", 200
        except SlackApiError as e:
            return e.response["error"]
    else:
        return redirect(BASE_URL)

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    user_id = event.get('user')

    message = {'channel': user_id, 'blocks':[
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": (
                    "Greetings from the *SWOB Slack App* \n\n"
                    "Get started by connecting your slack account to SMS Without Borders in order for the SWOB App to send messages to this workspace on your behalf :)"
                )
			},
		},
        
		{
			"type": "actions",
			"block_id": "actionblock789",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Connect to SWOB"
					},
                    "style": "primary",
					"url": "https://05c7-41-202-207-147.sa.ngrok.io/auth/slack"
				}
			]
		}
    ]}

    client = slack.WebClient(token=os.environ['BOT_TOKEN'])
    client.chat_postMessage(**message)


if __name__ == "__main__":
    app.run(debug=True)
