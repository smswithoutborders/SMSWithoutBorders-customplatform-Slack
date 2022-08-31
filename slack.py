import logging
from slack_sdk import errors
from slack_bolt import App


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def message_channel(channel_id, message, token):
    try:
        app = App()
        res = app.client.chat_postMessage(channel=channel_id, text=message, token=token)
        return bool(res.get("ok", ""))
    except errors.SlackApiError as err:
            logger.debug("Error posting message: %s", err)


def send_dm(email, message, token):
    try:
        app = App()
        response = app.client.users_lookupByEmail(email=email, token=token)
        print(response)
        if bool(response.get("ok", "")) is False:
            return False

        user = response.get("user", {})
        uid = user.get("id", "")
        print(uid)
        res = app.client.chat_postMessage(channel=uid, text=message, token=token)

        return bool(res.get("ok", ""))

    except errors.SlackApiError as err:
            logger.debug("Error posting message: %s", err)
            print(err)


