import os
import telebot
from flask import Flask
import threading
from telebot import types

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# تخزين مؤقت للمحافظ (لتجربة البوت)
user_wallets = {}

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
    btn5 = types.KeyboardButton("👛 إضافة المحفظة")
    btn6 = types.KeyboardButton("👤 الملف الشخصي")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)

    bot.reply_to(message, "أهلاً بكِ في بوت التعدين! استخدمي الأزرار أدناه:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text
    chat_id = message.chat.id

    if text == "📊 الحساب والمحفظة":
        wallet = user_wallets.get(chat_id, "لم يتم إضافة محفظة بعد")
        bot.reply_to(message, f"📊 معلومات الحساب والمحفظة:\n- المحفظة المحفوظة: `{wallet}`", parse_mode="Markdown")
    elif text == "⛏️ بدء التعدين":
        bot.reply_to(message, "⛏️ جاري بدء عملية التعدين بنجاح...")
    elif text == "👥 رابط الإحالة":
        bot.reply_to(message, "👥 إليكِ رابط الإحالة الخاص بكِ: https://t.me/your_bot?start=ref123")
    elif text == "💵 سحب الأرباح":
        bot.reply_to(message, "💵 تم استلام طلب السحب بنجاح! قيد المعالجة للتحويل.")
    elif text == "👛 إضافة المحفظة":
        bot.reply_to(message, "👛 الرجاء إرسال عنوان محفظتك الآن في رسالة مستقلة ليتم حفظه.")
    elif text == "👤 الملف الشخصي":
        user_name = message.from_user.first_name
        user_id = message.from_user.id
        bot.reply_to(message, f"👤 الملف الشخصي:\n- الاسم: {user_name}\n- المعرف: `{user_id}`\n- الحالة: نشط 🟢", parse_mode="Markdown")
    else:
        # اعتبر أي نص آخر يتم إرساله هو عنوان محفظة تم إدخاله
        user_wallets[chat_id] = text
        bot.reply_to(message, f"✅ تم حفظ المحفظة بنجاح:\n`{text}`", parse_mode="Markdown")

def run_bot():
    bot.remove_webhook()
    bot.infinity_polling()

if __name__ == '__main__':
    t = threading.Thread(target=run_bot)
    t.start()

    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
