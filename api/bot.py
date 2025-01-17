from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiohttp import web
import logging
import os

# Logging setup
logging.basicConfig(level=logging.INFO)

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv("7621067756:AAGBJl_QSppcyQJx6hL88WnUcVBQvxNGlU0")
WEBHOOK_URL = os.getenv("https://delete-join-messages-bot.vercel.app/api/webhook")

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# Handle new chat members
@dp.message_handler(content_types=["new_chat_members"])
async def handle_new_member(message: types.Message):
    try:
        # Delete the join message
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        logging.info(f"Deleted join message: {message.message_id}")
    except Exception as e:
        logging.error(f"Failed to delete message: {e}")

# Webhook endpoint
async def handle_webhook(request):
    try:
        data = await request.json()
        update = Update.to_object(data)
        await dp.process_update(update)
        return web.Response()
    except Exception as e:
        logging.error(f"Error processing update: {e}")
        return web.Response(status=500)

# Initialize aiohttp app
app = web.Application()
app.router.add_post("/api/webhook", handle_webhook)

if __name__ == "__main__":
    logging.info("Starting bot...")
    web.run_app(app, port=8000)
