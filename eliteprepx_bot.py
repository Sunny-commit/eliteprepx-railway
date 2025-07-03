import os
import telebot
from telebot import types

BOT_TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)

# 🔒 Replace with your Telegram numeric ID (from @userinfobot)
ADMIN_ID = 5904719884

# 🧾 Log every user who starts
@bot.message_handler(commands=['start'])
def welcome(msg):
    user = msg.from_user
    with open("users.txt", "a") as f:
        f.write(f"{user.first_name} (@{user.username}) - {user.id}\n")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("\ud83d\udcd8 GATE", "\ud83d\udcd7 JEE", "\ud83d\udcd5 NEET")
    markup.row("\ud83e\udd16 AI/ML", "💻 Interview Kits")
    markup.row("💎 Get Premium Access")

    bot.send_message(
        msg.chat.id,
        f"\ud83d\udc4b *Welcome to ElitePrepX!*\n\n\ud83c\udf93 Your all-in-one resource bot for:\n- Competitive Exams\n- AI/ML Projects\n- Interview Prep\n\nSelect a category to get started 👇",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# 🔍 Handle button responses (Exact match only)
@bot.message_handler(func=lambda m: m.text is not None)
def reply(m):
    text = m.text.lower().strip()

    if "i paid" in text:
        bot.reply_to(m, "❗To unlock premium content, please send a *payment screenshot*. No text-based confirmation allowed.", parse_mode="Markdown")
        return

    if text == "\ud83d\udcd8 gate":
        gate_premium_info(m)
    elif text == "\ud83d\udcd7 jee":
        jee_premium_info(m)
    elif text == "\ud83d\udcd5 neet":
        neet_premium_info(m)
    elif text == "\ud83e\udd16 ai/ml":
        ai_premium_info(m)
    elif text == "💻 interview kits":
        interview_premium_info(m)
    elif "premium" in text:
        all_premium_info(m)
    else:
        bot.reply_to(m, "❓ Please use the buttons below to navigate.")

# 💎 Subject-wise Premium Info
def gate_premium_info(msg):
    bot.reply_to(msg, "\ud83d\udcd8 *GATE Premium Access* - ₹29\nPay via UPI: `patetichandu@oksbi`\nSend screenshot here.", parse_mode="Markdown")

def jee_premium_info(msg):
    bot.reply_to(msg, "\ud83d\udcd7 *JEE Premium Access* - ₹29\nPay via UPI: `patetichandu@oksbi`\nSend screenshot here.", parse_mode="Markdown")

def neet_premium_info(msg):
    bot.reply_to(msg, "\ud83d\udcd5 *NEET Premium Access* - ₹29\nPay via UPI: `patetichandu@oksbi`\nSend screenshot here.", parse_mode="Markdown")

def ai_premium_info(msg):
    bot.reply_to(msg, "\ud83e\udd16 *AI/ML Premium Access* - ₹39\nPay via UPI: `patetichandu@oksbi`\nSend screenshot here.", parse_mode="Markdown")

def interview_premium_info(msg):
    bot.reply_to(msg, "💻 *Interview Kits Premium* - ₹39\nPay via UPI: `patetichandu@oksbi`\nSend screenshot here.", parse_mode="Markdown")

def all_premium_info(msg):
    response = """\ud83d\udc8e *ElitePrepX Full Premium Access*

📃 Unlock all subject packs:
- UPSC Notes & Strategy
- JEE Advanced Solutions
- GATE PYQs
- NEET Mock Tests
- AI/ML Projects & Cheat Sheets
- SDE Roadmaps + Kits

💰 ₹49 via UPI: `patetichandu@oksbi`  
📸 Send payment *screenshot here*.

⏳ We’ll verify and send links shortly.
"""
    bot.reply_to(msg, response, parse_mode="Markdown")

# 📸 Screenshot detection for payment confirmation
@bot.message_handler(content_types=['photo', 'document'])
def handle_payment_screenshot(msg):
    user = msg.from_user
    caption = msg.caption if msg.caption else "No caption"

    # Forward the screenshot to admin
    bot.forward_message(chat_id=ADMIN_ID, from_chat_id=msg.chat.id, message_id=msg.message_id)

    # Notify admin with details
    bot.send_message(
        ADMIN_ID,
        f"\ud83d\udcf8 *Screenshot Received*\n\ud83d\udc64 From: @{user.username or 'NoUsername'}\n🧾 ID: `{user.id}`\n✏️ Caption: _{caption}_",
        parse_mode="Markdown"
    )

    # Acknowledge user
    bot.reply_to(msg, "✅ Screenshot received!\nYour payment is being verified.\nYou’ll get the premium content shortly.")

# ⭯️ Keep the bot running
bot.infinity_polling()
