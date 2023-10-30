# Slack Bot using LangChain and LNBits

![Bot Demo](./images/bot_demo.gif)

This repository is a proof of concept app that demonstrates a bot using [LangChain](https://github.com/hwchase17/langchain) and [LNBits](https://lnbits.com) to create a Slack bot that can be used to answer questions and charge for the answers using the Lightning Network Invoices.

The project [Slack AI Assistant with Python & LangChain](https://docs.datalumina.io/3y3XPD66nBJaub/b/2808AFE6-41C8-46EF-A4AB-52A4B021993A/Part-1-—-Slack-Setup) was used as base for this project.

Video Demo: [YouTube](https://youtu.be/XEQXDKYb_Yw)

## Slack Setup

#### 1. Create a new Slack app

- Choose an existing Slack workspace or create a new one.
- Go to https://api.slack.com/apps and sign in with your Slack account.
- Click "Create New App" and provide an app name and select your workspace as the development workspace. Click "Create App".

#### 2. Set up your bot

- Under the "Add features and functionality" section, click on "Bots".
- Click "Add a Bot User" and fill in the display name and default username. Save your changes.

#### 3. Add permissions to your bot

- In the left sidebar menu, click on "OAuth & Permissions".
- Scroll down to "Scopes" and add the required bot token scopes. For this example, you'll need at least app_mentions:read, chat:write, files:write, and channels:history.

#### 4. Install the bot to your workspace
- In the left sidebar menu to go basic information and click on "Install App".
- Click "Install App to Workspace" and authorize the app.

#### 5. Retrieve the bot token
- After installation, go back to “OAuth & Permissions" page.
- Copy the "Bot User OAuth Access Token" (it starts with xoxb-). You'll need it for your Python script.


## LNBits Setup
#### 1. Create a wallet
- Go to [LNBits](https://legend.lnbits.com) and add a new wallet.
- You will need to add the data in Api docs in the `.env` file.

## Python Setup

#### 1. Clone the repository:

```bash
git clone https://github.com/ibiscp/Slack-Langchain-LNBits.git

```

#### 2. Install the necessary dependencies for the backend

```bash
poetry install
```

#### 3. Set up the environment variables in the `.env` file

#### 4. Start the backend

```bash
python3 bot/main.py
```

## Ngrok Setup
#### 1. Expose your local server using ngrok
- If you haven't installed ngrok, you can download it from https://ngrok.com/download or, on macOS, install it via Homebrew by running: `brew install ngrok` 
- In a new terminal (macOS/Linux) or Command Prompt (Windows), start ngrok by running the following command: ngrok http 5000 
- Note the HTTPS URL provided by ngrok (e.g., https://yoursubdomain.ngrok.io). You'll need it for the next step.

Remember that if you installed ngrok via Homebrew, you can run ngrok http 5000 from any directory in the terminal. If you downloaded it from the website, navigate to the directory where ngrok is installed before running the command.

#### 2. Configure your Slack app with the ngrok URL
- Go back to your Slack app settings at https://api.slack.com/apps. 
- Click on "Event Subscriptions" in the left sidebar menu.
- Enable events and enter your ngrok URL followed by /slack/events (e.g., https://yoursubdomain.ngrok.io/slack/events).
- Scroll down to "Subscribe to bot events" and click "Add Bot User Event". Add the app_mention event and save your changes.
- Please note that every time you restart ngrok in the terminal, you have to update the URL in Slack — this is just for testing.

#### 3. Reinstall your Slack app to update the permissions
- In the left sidebar menu, click on "Install App". 
- Click "Reinstall App to Workspace" and authorize the app.

#### 4. Add your bot to a Slack channel
- Type /invite @bot-name in the channel.

