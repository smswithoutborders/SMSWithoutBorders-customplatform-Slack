import os
import json
import logging
logger = logging.getLogger(__name__)

from slack_sdk.oauth import AuthorizeUrlGenerator
from slack_sdk import errors
from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings

credentials_path = os.path.join(os.path.dirname(__file__), "configs", "credentials.json")

if not os.path.exists(credentials_path):
	error = "credentials.json file not found at %s" % credentials_path
	raise FileNotFoundError(error)

c = open(credentials_path)
creds = json.load(c)

class Slack:
    """
        SW/OB Slack app
    """

    def __init__(self, originalUrl:str) -> None:
        self.clientId = creds["client_id"]
        self.clientSecret = creds["client_secret"]
        self.callback = f"{originalUrl}/platforms/slack/protocols/oauth2/redirect_codes/"
        self.scopes = ["chat:write", "channels:write", "groups:write", "im:write", "mpim:write", "channels:read", "groups:read", "im:read", "mpim:read", "usergroups:read", "users:read", "users.profile:read", "users:read.email"]
        self.authorize_url_generator = AuthorizeUrlGenerator(
            client_id=creds["client_id"],
            user_scopes=self.scopes,
            redirect_uri=self.callback
        )
        self.oauth_settings = OAuthSettings(
            client_id=creds["client_id"],
            client_secret=creds["client_secret"]
        )
        self.slack = App(oauth_settings=self.oauth_settings)

    def init(self):
        """
        """
        try:
            url = self.authorize_url_generator.generate("")

            logger.info("- Successfully fetched init url")

            return { "url": url }
        
        except Exception as error:
            logger.error("Slack-OAuth2-init failed. See logs below")
            raise error

    def validate(self, code:str) -> dict:
        """
        """
        try:
            response = self.slack.client.oauth_v2_access(client_id=self.clientId, client_secret=self.clientSecret, code=code, redirect_uri=self.callback)

            if not bool(response.get("ok", "")):
                raise errors.SlackApiError("Could not validate code")

            user = response.get("authed_user", {})
            user_id = user["id"]
            profile = self.slack.client.users_profile_get(user=user_id, token=user["access_token"])
            profile = profile.get("profile", {})

            logger.info("- Successfully fetched token and profile")

            result = {
                "profile": profile,
                "token": json.dumps(user)
            }

            return result

        except errors.SlackApiError as err:
            logger.error("Error obtaining user token and profile: %s", err)
            raise error
        
        except Exception as error:
            logger.error("Slack-OAuth2-validate failed. See logs below")
            raise error


    def revoke(self, token:dict) -> bool:
        """
        """
        try:
            app = App(token=token["access_token"])
            res = app.client.auth_revoke()
            if bool(res.get("ok", "")):
                logger.info("- Successfully revoked access")

                return True
            else:
                raise errors.SlackApiError("Error revoking token")

        except errors.SlackApiError as err:
            logger.error("Error revoking token: %s", err)
            raise error

        except Exception as error:
            logger.error("Slack-OAuth2-revoke failed. See logs below")
            raise error