import os
import telebot
from flask import Flask
import threading
from telebot import types

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# تخزين بيانات المستخدمين مؤقتاً
user_wallets = {}
user_balances = {}
user_states = {}

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
    btn7 = types.KeyboardButton("📥 إيداع العملات")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    markup.add(btn7)

    bot.reply_to(message, "أهلاً بكِ في بوت التعدين المطور! استخدمي الأزرار أدناه للتحكم:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text
    chat_id = message.chat.id

    # تهيئة الرصيد الابتدائي للمستخدم إذا لم يكن موجوداً
    if chat_id not in user_balances:
        user_balances[chat_id] = 60.0

    current_state = user_states.get(chat_id)

    if text == "📊 الحساب والمحفظة":
        wallet = user_wallets.get(chat_id, "لم يتم إضافة محفظة بعد")
        balance = user_balances[chat_id]
        bot.reply_to(message, f"📊 **معلومات الحساب:**\n- الرصيد الحالي: `{balance} عملة`\n- المحفظة: `{wallet}`", parse_mode="Markdown")

    elif text == "⛏️ بدء التعدين":
        user_balances[chat_id] += 5.0
        new_balance = user_balances[chat_id]
        bot.reply_to(message, f"⛏️ تم التعدين بنجاح!\n➕ تمت إضافة 5 عملات إلى رصيدك.\n💰 رصيدك الحالي: `{new_balance} عملة`", parse_mode="Markdown")

    elif text == "👥 رابط الإحالة":
        bot.reply_to(message, "👥 إليكِ رابط الإحالة الخاص بكِ لدعوة الأصدقاء:\n`https://t.me/your_bot?start=ref123`", parse_mode="Markdown")

    elif text == "💵 سحب الأرباح":
        balance = user_balances[chat_id]
        wallet = user_wallets.get(chat_id)
        if not wallet or wallet == "لم يتم إضافة محفظة بعد":
            bot.reply_to(message, "⚠️ يجب إضافة محفظة أولاً عبر زر '👛 إضافة المحفظة' قبل طلب السحب.")
        elif balance < 10:
            bot.reply_to(message, "⚠️ الحد الأدنى للسحب هو 10 عملات.")
        else:
            bot.reply_to(message, f"💵 تم تقديم طلب سحب `{balance} عملة` إلى محفظتك بنجاح! ⏳ قيد المعالجة للتحويل.")
            user_balances[chat_id] = 0.0

    elif text == "👛 إضافة المحفظة":
        user_states[chat_id] = 'awaiting_wallet'
        bot.reply_to(message, "👛 الرجاء إرسال عنوان محفظتك الآن في رسالة مستقلة ليتم حفظه.")

    elif text == "📥 إيداع العملات":
        user_states[chat_id] = 'awaiting_deposit'
        bot.reply_to(message, "📥 الرجاء إرسال عدد العملات المراد إيداعها إلى رصيدك (أرسل رقماً فقط):")

    elif text == "👤 الملف الشخصي":
        user_name = message.from_user.first_name
        user_id = message.from_user.id
        balance = user_balances[chat_id]
        wallet = user_wallets.get(chat_id, "غير مسجلة")
        profile_info = f"👤 **الملف الشخصي:**\n\n- الاسم: {user_name}\n- المعرف: `{user_id}`\n- الرصيد: `{balance} عملة`\n- المحفظة: `{wallet}`\n- الحالة: نشط 🟢"
        bot.reply_to(message, profile_info, parse_mode="Markdown")

    else:
        # معالجة النصوص بناءً على حالة المستخدم (حفظ محفظة أو إيداع)
        if current_state == 'awaiting_wallet':
            user_wallets[chat_id] = text
            user_states[chat_id] = None
            bot.reply_to(message, f"✅ تم حفظ المحفظة بنجاح:\n`{text}`", parse_mode="Markdown")
        elif current_state == 'awaiting_deposit':
            try:
                amount = float(text)
                user_balances[chat_id] += amount
                user_states[chat_id] = None
                bot.reply_to(message, f"✅ تم إيداع `{amount} عملة` بنجاح!\n💰 رصيدك الجديد: `{user_balances[chat_id]} عملة`", parse_mode="Markdown")
            except ValueError:
                bot.reply_to(message, "⚠️ الرجاء إرسال رقم صحيح لعدد العملات المراد إيداعها.")
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
