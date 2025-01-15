from flask import Flask, request
import telegram

# Initialize Flask app
app = Flask(__name__)

# Telegram bot token
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Initialize the Telegram bot
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

@app.route("/api/webhook", methods=["POST"])
def webhook():
    # Parse the incoming update
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # Check if it's a message and if it contains a "new_chat_member" field
    if update.message and (update.message.new_chat_members or update.message.group_chat_created):
        # Delete the message
        try:
            bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
        except telegram.error.TelegramError as e:
            print(f"Error deleting message: {e}")

    return "ok", 200
