import os
import telebot
from flask import Flask
import threading

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running 24/7!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بكِ! البوت يعمل الآن بشكل سحابي على مدار الساعة.")

def run_bot():
    bot.remove_webhook()  # مسح أي اتصال سابق لمنع تعارض 409
    bot.infinity_polling()

if __name__ == '__main__':
    t = threading.Thread(target=run_bot)
    t.start()

    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
