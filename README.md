# OAuth2 Slack App
A simple slack app that authenticates users given their app's **Client ID** and **Client Secret** and sends a message on their behalf.


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
pip3 install -r requirements. txt
```


### Creating and Installing your Slack App
- Head over to the [Slack API site](https://api.slack.com/apps) and create a new slack app.
- Select the workspace you want your app to be installed in.
- After your app is created, go to *OAuth & Permissions* on your sidebar menu.
- Scroll down to the **Scopes** section where we have *Bot Token Scopes* and *User Token Scopes*.
- Add a new scope for each of them. For each, select `chat:write`.
- Go back to your sidebar menu in the *Settings* sections and go to *Install App*.
- Click on the button to install your app to the workspace.
- If you make any more changes to the scope, be sure to reinstall your app.
- Go back to your *Auth & Permissions* page. You should be able to find where to add a callback URL. This is the URL our flask app will go to after you've been authenticated.
- The base URL of this Flask app (if running locally) is `http://127.0.0.1:5000/` and the callback URL is `http://127.0.0.1:5000/oauth/slack/callback`. However, the slack API only accepts `https` sites for callback URLs. I recommend you install [ngrok](https://ngrok.com) and set it up where it will generate an `https` URL out of your localhost URL. 
- Once this is done, add it as your callback URL. Do not forget to add the `oauth/slack/callback` endpoint.
- Head back to your slack workspace and invite your app to the channel you intend it should send messages to.


### Running your app to send a message on your behalf
- In this project's root, rename the `.example.env` file to `.env`.
- Grab the Client ID and Client Secret of yor Slack App from the API site and add. Also add your callback URL.
- Run `flask run` on your terminal.

#### API Reference
- `GET /`: 
Displays homepage to begin authentication
- `GET /auth/slack`: 
Displays a consent screen with the various scopes for users to grant permission

- `POST /oauth/slack/callback`: 
Exchanges temporary authorization code for the access token
  ###### Parameters
    - `code`: Temporal authorization code issued by slack after granting consent.
- `POST /slack/send`: 
Send message to slack with stored access token
  ###### Parameters
    - `channel`: A channel ID or channel name you are currently present in. User ID if you want to DM someone.
    - `message`: The message or text you intend sending.



#### References
- [Slack API OAuth2 Docs](https://api.slack.com/authentication/oauth-v2)


You are good to go!!

