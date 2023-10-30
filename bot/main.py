import os
import asyncio
from slack_bolt.async_app import AsyncApp
from bot.utils import my_function, draft_email
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError
from pylnbits.config import Config
from pylnbits.user_wallet import UserWallet
from aiohttp.client import ClientSession
import qrcode
from io import BytesIO


# Set Slack API credentials
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")

# Initialize the Slack app
app = AsyncApp(token=SLACK_BOT_TOKEN)

# Lnbits
c = Config(in_key=os.environ.get('IN_KEY'), admin_key=os.environ.get('ADMIN_KEY'), lnbits_url=os.environ.get('LNBITS_URL'))
url = c.lnbits_url

async def get_bot_user_id():
    """
    Get the bot user ID using the Slack API.
    Returns:
        str: The bot user ID.
    """
    try:
        # Initialize the Slack client with your bot token
        slack_client = AsyncWebClient(token=os.environ["SLACK_BOT_TOKEN"])
        response = await slack_client.auth_test()
        return response["user_id"]
    except SlackApiError as e:
        print(f"Error: {e}")

async def get_history(channel_id, thread_ts):
    messages = []
    try:
        slack_client = AsyncWebClient(token=os.environ["SLACK_BOT_TOKEN"])
        response = await slack_client.conversations_replies(
            channel=channel_id,
            ts=thread_ts
        )
        # Check for errors
        if not response['ok']:
            raise SlackApiError(f"Error: {response['error']}")
        # Iterate through the messages to find the thread
        messages_payload = response['messages']
        for message in messages_payload:
            print(f"{message['user']}: {message['text']}")
            messages.append({'user': message['user'], 'text': message['text']})
    except SlackApiError as e:
        print(f"Error: {e}")

    return messages

async def upload_file(channel_id, buf, thread_ts):
    upload_response = {}
    try:
        slack_client = AsyncWebClient(token=os.environ["SLACK_BOT_TOKEN"])
        upload_response = await slack_client.files_upload_v2(
                channel=channel_id,
                file=buf,
                filename=f'{thread_ts}.png',
                thread_ts=thread_ts,
                initial_comment='Hey there! To keep the magic happening, could you settle this little invoice? 🧾✨'
            )
    except SlackApiError as e:
        print(f"Error: {e}")

    return upload_response

@app.event("app_mention")
async def handle_mentions(body, say):
    """
    Event listener for mentions in Slack.
    When the bot is mentioned, this function processes the text and sends a response.

    Args:
        body (dict): The event data received from Slack.
        say (callable): A function for sending a response to the channel.
    """
    event = body["event"]
    text = event["text"]
    bot_user_id = get_bot_user_id()

    mention = f"<@{await bot_user_id}>"
    text = text.replace(mention, "").strip()

    # Get the timestamp of the message that mentioned the bot
    thread_ts = event.get('thread_ts', event['ts'])
    channel_id = event["channel"]

    history_message = await get_history(channel_id, thread_ts)

    async with ClientSession() as session:
        # GET wallet details
        uw = UserWallet(c, session)
        userwallet = await uw.get_wallet_details()
        print(f"user wallet info : {userwallet}")

        res = await uw.create_invoice(False, 10, "Langchain LNBits Bot", "")
        payment_hash = res['payment_hash']

        # Generate QR code
        invoice_text = res['payment_request']
        img = qrcode.make(invoice_text)
        buf = BytesIO()
        img.save(buf)
        buf.seek(0)

        # Upload QR code image to Slack
        upload_response = await upload_file(channel_id, buf, thread_ts)

        # Check for errors in the upload response
        if not upload_response['ok']:
            error_message = upload_response['error']
            await say(text=f"Error uploading QR code: {error_message}", thread_ts=thread_ts)
            return

        paid = False
        while not paid:
            await asyncio.sleep(1)
            res = await uw.check_invoice(payment_hash)
            paid = res['paid']

            if res['details']['time'] > res['details']['expiry']:
                await say(text="Oh no! 🙀 It seems like this invoice turned into a pumpkin at midnight! 🎃 To restart the enchantment, a little golden coin is needed! 💰", thread_ts=thread_ts)
                return

    await say(text="You're a star! 🌟 Your payment has sprinkled fairy dust on our servers! ✨ Now, let me whip up some magic and process that for you! 🧙‍♂️", thread_ts=thread_ts)
    response = draft_email(text)
    await say(text=response, thread_ts=thread_ts)



# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 5000)))