import logging

from slack_sdk import errors
from slack_bolt import App

logger = logging.getLogger(__name__)

def message_channel(channel_id: str, message: str, token: str) -> bool:
    """
    """
    try:
        app = App(token=token)
        res = app.client.chat_postMessage(channel=channel_id, text=message)
        return bool(res.get("ok", ""))

    except errors.SlackApiError as err:
        logger.exception(" - Error posting message: %s", err)
        raise err

    except Exception as error:
        raise error


def send_dm(email: str, message: str, token: str) -> bool:
    """
    """
    try:
        app = App(token=token)
        response = app.client.users_lookupByEmail(email=email)
        if bool(response.get("ok", "")) is False:
            return False

        user = response.get("user", {})
        uid = user.get("id", "")
        res = app.client.chat_postMessage(channel=uid, text=message)

        return bool(res.get("ok", ""))

    except errors.SlackApiError as err:
        logger.exception("- Error posting message: %s", err)
        raise err

    except Exception as error:
        raise error