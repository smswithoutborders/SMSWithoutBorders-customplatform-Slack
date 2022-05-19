# OAuth2 Slack App
A simple slack app that authenticates users given their app's **Client ID** and **Client Secret** and sends a message on their behalf.


### Dependencies
- [Flask](https://pypi.org/project/Flask/)
- [Slack Web Client](https://pypi.org/project/slackclient/)
- [Python Requests](https://pypi.org/project/requests/)


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

You are good to go!!

