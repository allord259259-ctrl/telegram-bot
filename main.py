import os
import telebot
from flask import Flask
import threading
from telebot import types

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running 24/7!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📊 الحساب والمحفظة")
    btn2 = types.KeyboardButton("⛏️ بدء التعدين")
    btn3 = types.KeyboardButton("👥 رابط الإحالة")
    btn4 = types.KeyboardButton("💵 سحب الأرباح")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    bot.reply_to(message, "أهلاً بكِ! البوت يعمل الآن بشكل سحابي على مدار الساعة.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text
    if "الحساب والمحفظة" in text:
        bot.reply_to(message, "📊 معلومات الحساب والمحفظة الخاصة بكِ:")
    elif "بدء التعدين" in text:
        bot.reply_to(message, "⛏️ جاري بدء عملية التعدين بنجاح...")
    elif "رابط الإحالة" in text:
        bot.reply_to(message, "👥 إليكِ رابط الإحالة الخاص بكِ لدعوة الأصدقاء:")
    elif "سحب الأرباح" in text:
        bot.reply_to(message, "💵 تم استلام طلب السحب بنجاح! قيد المعالجة للتحويل.")
    else:
        bot.reply_to(message, "الرجاء استخدام الأزرار أدناه للتفاعل مع البوت.")

def run_bot():
    bot.remove_webhook()
    bot.infinity_polling()

if __name__ == '__main__':
    t = threading.Thread(target=run_bot)
    t.start()

    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
