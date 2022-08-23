# SMSWithoutBorders Custom Platform - Slack

### Installing Dependencies
- Create a virtual environment
```bash
python3 -m venv venv
```
- Activate the virtual environment
```bash
. venv/bin/activate
```
- Install dependencies in `requirements.txt`
```bash
pip3 install -r requirements.txt
```


### Creating and setting up your Slack App
- Head over to the [Slack API site](https://api.slack.com/apps) and create a new slack app.
- Select the workspace you want your app to be installed in.
- After your app is created, go to *OAuth & Permissions* on your sidebar menu.
- Scroll down to the **Scopes** section where we have *Bot Token Scopes* and *User Token Scopes*.
- For the bot token scopes, add `app_mentions:read`, `channels:history`, `channels:join`, `chat:write`, `im:history`, `im:read`, `im:write`,and `users:write`
- For the user token scopes, add `chat:write`
- Go back to your sidebar menu in the *Settings* sections and go to *Install App*.
- Click on the button to install your app to the workspace.
- If you make any more changes to the scope, be sure to reinstall your app.



### Adding configurations and events
- In the configs directory, create a `credentials.json` file. The content should look like this:
```json
{
    "client_id": "",
    "client_secret": "",
    "signing_secret": "",
    "bot_token": "",
    "app_level_token": ""
}
```
- Grab your slack app's client id, client secret and signing secret on the *Basic Information* page of the API site and add in the credentials file. Also copy the bot token from the *OAuth & Permissions* page.
- Go to the *Socket Mode* page and turn on socket mode.
- Now go to the *Basic Information* page and scroll to the *App Level Tokens* section. Generate an app-level token and make sure to select the `connections:write` and `authorizations:read` scopes.
- Copy your app-level token and add to your credentials file.
- Go to the *Event Subscription* page and turn on events. (You won't need a request URL since you turned on socket mode)
- Scroll down the page where we have *Subscribe to bot events* and add the `app_mention`, `message.channels` and `message.im` events for now. (Make sure to save changes and reinstall the app)

### Steps to run
- Once all dependencies are installed and the `credentials.json` file is ready, run the events file. This should always be running so that it can listen to events.
```bash
python3 events.py
```
- In the `slack_app` file, we have 3 methods:
	- `init`: To generate the authorization url. It returns a key-value pair with `url` as the key. This URL leads to the consent screen.
	- `validate`: It accepts the temporary code you exchange in order to get the access token. For testing purposes, you can copy the code from the URL bar of your browser after granting the slack app permission and feed into this method. It returns two key-value pairs containing the `user_id` and their `access_token`. This token is the user access token different from the bot token.
	- `revoke`: In this method, you pass in the user access token inorder to revoke it.
- In the `slack.py` file, we have 2 functions:
	- `message_channel`: Which accepts the channel id or channel name and the message.
	- `send_dm`: Which accepts the email address of the receiver and and the intended message.
If the messages are successfully sent, it will return `True`.
- In order to test events are working, try tagging your bot in a channel it belongs to and it should send you a DM to connect to SWOB to Slack.

#### References
- [Slack API OAuth2 Docs](https://api.slack.com/authentication/oauth-v2)


You are good to go!!


