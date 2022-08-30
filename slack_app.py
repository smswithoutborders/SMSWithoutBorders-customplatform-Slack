import logging
from slack_sdk.oauth import AuthorizeUrlGenerator
from slack_sdk.oauth.installation_store import FileInstallationStore, Installation
from slack_sdk.oauth.state_store import FileOAuthStateStore
from slack_sdk import errors
from slack_bolt import App

import misc
import json


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Issue and consume state parameter value on the server-side.
state_store = FileOAuthStateStore(expiration_seconds=300, base_dir="./data")
# Persist installation data and lookup it by IDs.
installation_store = FileInstallationStore(base_dir="./data")

creds = misc.get_creds('configs/credentials.json')


class Slack:
    """
        SW/OB Slack app
    """

    def __init__(self, baseUrl=None) -> None:
        self.baseUrl = baseUrl
        self.clientId = creds["client_id"]
        self.clientSecret = creds["client_secret"]
        if baseUrl is not None:
            self.callback = f"{baseUrl}/oauth/slack/callback"
        self.signingSecret = creds["signing_secret"]
        self.botToken = creds["bot_token"]
        self.authorize_url_generator = AuthorizeUrlGenerator(
            client_id=creds["client_id"],
            scopes=["channels:read", "groups:read", "im:read", "mpim:read", "usergroups:read", "users:read", "users.profile:read", "channels:join", "app_mentions:read", "im:history"],
            user_scopes=["chat:write", "channels:write", "groups:write", "im:write", "mpim:write", "channels:read", "groups:read", "im:read", "mpim:read", "usergroups:read", "users:read", "users.profile:read", "users:read.email"]
        )
        self.app = App(token=self.botToken)


    def init(self):
        """
        """
        state = state_store.issue()
        url = self.authorize_url_generator.generate(state)
        return { "url": url }


    def validate(self, code):
        try:

            response = self.app.client.oauth_v2_access(client_id=self.clientId, client_secret=self.clientSecret, code=code)
            if not bool(response.get("ok", "")):
                raise errors.SlackApiError("Could not validate code")

            user = response.get("authed_user", {})
            user_id = user["id"]
            profile = self.app.client.users_profile_get(user=user_id)
            profile = profile.get("profile", {})

            result = {
                "profile": profile,
                "access_token": user["access_token"]
            }

            creds = json.dumps(result, indent=2)
            return creds

        except errors.SlackApiError as err:
            logger.debug("Error obtaining user token and profile: %s", err)
            return None


    def revoke(self, user_token):
        try:
            app = App(token=user_token)
            res = app.client.auth_revoke()
            if bool(res.get("ok", "")):
                return True
            else:
                raise errors.SlackApiError("Error revoking token")
        except errors.SlackApiError as err:
            logger.debug("Error revoking token: %s", err)


