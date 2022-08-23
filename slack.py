import json
import os
import logging

from slack_sdk import WebClient
from slack_sdk import errors
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import misc


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

creds = misc.get_creds('creds.json')

app = App(token=creds['access_token'])


def message_channel(channel_id, message):
    try:
        res = app.client.chat_postMessage(channel=channel_id, text=message)
        return bool(res.get("ok", ""))
    except errors.SlackApiError as err:
            logger.debug("Error posting message: %s", err)


def send_dm(email, message):
    try:

        response = app.client.users_lookupByEmail(email=email)
        print(response)
        if bool(response.get("ok", "")) is False:
            return False

        user = response.get("user", {})
        uid = user.get("id", "")
        print(uid)
        res = app.client.chat_postMessage(channel=uid, text=message)

        return bool(res.get("ok", ""))

    except errors.SlackApiError as err:
            logger.debug("Error posting message: %s", err)
            print(err)


