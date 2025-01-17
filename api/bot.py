from flask import Flask, request
import telegram

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "7621067756:AAGBJl_QSppcyQJx6hL88WnUcVBQvxNGlU0"
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

@app.route("/api/webhook", methods=["POST"])
def webhook():
    # Parse the incoming update
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # Check for new chat members and delete join messages
    if update.message and (update.message.new_chat_members or update.message.group_chat_created):
        try:
            bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
        except telegram.error.TelegramError as e:
            print(f"Error deleting message: {e}")

    return "ok", 200

@app.route("/api/webhook", methods=["GET"])
def webhook_info():
    return "This endpoint is for POST requests only.", 405
