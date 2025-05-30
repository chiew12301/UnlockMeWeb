import os
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
GAME_URL = os.getenv("GAME_URL")

bot = Bot(token=TOKEN)
app = Flask(__name__)

dispatcher = Dispatcher(bot, None, workers=0)

def start(update, context):
    keyboard = [
        [InlineKeyboardButton("🎮 Play Unlock Me", url=GAME_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Try Unlock Me by KurumiC below!", reply_markup=reply_markup)

dispatcher.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
