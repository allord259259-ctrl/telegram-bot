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

# أمر /start مع الأزرار المحدثة (إضافة الملف الشخصي والمحافظ)
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

    bot.reply_to(message, "أهلاً بكِ! تم تحديث البوت بنجاح لإضافة المحافظ والملف الشخصي:", reply_markup=markup)

# معالجة نصوص الأزرار الجديدة والقديمة
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
    elif "إضافة المحفظة" in text:
        bot.reply_to(message, "👛 الرجاء إرسال عنوان محفظتك (مثال: عنوان شبكة TRC20 أو TON) ليتم حفظه بنجاح.")
    elif "الملف الشخصي" in text:
        user_name = message.from_user.first_name
        user_id = message.from_user.id
        profile_info = f"👤 **الملف الشخصي:**\n\n- الاسم: {user_name}\n- المعرف (ID): `{user_id}`\n- الحالة: نشط 🟢\n- الرصيد: 60.0 عملة"
        bot.reply_to(message, profile_info, parse_mode="Markdown")
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
