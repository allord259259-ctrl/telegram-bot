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
    # إنشاء لوحة أزرار تفاعلية
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("اضغط هنا للتجربة", callback_data="test_btn")
    markup.add(btn1)

    bot.reply_to(message, "أهلاً بكِ! البوت يعمل الآن على مدار الساعة. جربي الضغط على الزر أدناه:", reply_markup=markup)

# معالج نقرات الأزرار التفاعلية
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "test_btn":
        # إظهار إشعار صغير للمستخدم عند الضغط
        bot.answer_callback_query(call.id, "تم استلام ضغطتك بنجاح! 🎉")
        # إرسال رسالة رد تفاعلية
        bot.send_message(call.message.chat.id, "رائع جداً! الأزرار تعمل بكفاءة تامة الآن.")

def run_bot():
    bot.remove_webhook()
    bot.infinity_polling()

if __name__ == '__main__':
    t = threading.Thread(target=run_bot)
    t.start()

    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
