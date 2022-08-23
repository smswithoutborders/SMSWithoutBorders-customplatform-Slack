import os
import json
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_app import Slack
from slack_sdk import errors

import misc


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


creds = misc.get_creds('configs/credentials.json')


slack_app = Slack()
app = slack_app.app


@app.event("app_mention")
def handle_app_mention_events(body, logger, say, event):
	try:
		event = body.get("event", {})
		user = event["user"]
	    
		message = {'channel': user, 'text': f"Hi there, <@{event['user']}>!", 'blocks':[
	        {
	            "type": "header",
	            "text": {
	                "type": "plain_text",
	                "text": "Connect to SWOB"
	            }
	        },
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
	                    "url": f"{slack_app.init()['url']}"
	                }
	            ]
	        }
		]}
		
		app.client.chat_postMessage(**message)
		
		say(f"Hi there, <@{event['user']}>! I sent a DM requesting you connect to SMSWithoutBorders")
	except errors.SlackApiError as err:
		logger.debug("Error responding to event: %s", err)



if __name__ == "__main__":
	handler = SocketModeHandler(app, creds["app_level_token"])
	handler.start()
