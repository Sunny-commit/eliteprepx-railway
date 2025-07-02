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
    markup.row("📘 GATE", "📗 JEE", "📕 NEET")
    markup.row("🤖 AI/ML", "💻 Interview Kits")
    markup.row("💎 Get Premium Access")

    bot.send_message(
        msg.chat.id,
        f"👋 *Welcome to ElitePrepX!*\n\n🎓 Your all-in-one resource bot for:\n- Competitive Exams\n- AI/ML Projects\n- Interview Prep\n\nSelect a category to get started 👇",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# 🔍 Handle button responses
@bot.message_handler(func=lambda m: True)
def reply(m):
    text = m.text.lower()
    if "gate" in text:
        bot.reply_to(m, "📘 GATE Materials:\nhttps://your-link")
    elif "jee" in text:
        bot.reply_to(m, "📗 JEE Materials:\nhttps://your-link")
    elif "neet" in text:
        bot.reply_to(m, "📕 NEET PDFs:\nhttps://your-link")
    elif "ml" in text or "ai" in text:
        bot.reply_to(m, "🤖 AI/ML PDFs & Cheat Sheets:\nhttps://your-link")
    elif "interview" in text:
        bot.reply_to(m, "💻 SDE Interview Kits:\nhttps://your-link")
    elif "premium" in text:
        premium_info(m)
    else:
        bot.reply_to(m, "❓ Please use the buttons below to navigate.")

# 💎 Premium Info
def premium_info(msg):
    response = """💎 *ElitePrepX Premium Access*

📚 Unlock exclusive study packs:
- UPSC Notes & Strategy
- JEE Advanced Solutions
- GATE Previous Year Sets
- NEET Full-Length Mocks
- AI/ML Projects & Cheat Sheets
- Coding Roadmaps + SDE Kits

💰 Just ₹49 via UPI: `patetichandu@oksbi`  
📸 Send your *payment screenshot here*.

⏳ We’ll verify & send premium links directly in chat.
"""
    bot.reply_to(msg, response, parse_mode="Markdown")

# 📸 Screenshot detection for payment confirmation
@bot.message_handler(content_types=['photo', 'document'])
def handle_payment_screenshot(msg):
    user = msg.from_user
    caption = msg.caption if msg.caption else "No caption"

    # Notify admin
    bot.send_message(
        ADMIN_ID,
        f"📸 *Screenshot Received*\n👤 From: @{user.username or 'NoUsername'}\n🧾 ID: `{user.id}`\n✏️ Caption: _{caption}_",
        parse_mode="Markdown"
    )

    # Acknowledge user
    bot.reply_to(msg, "✅ Screenshot received!\nYour payment is being verified.\nYou’ll get the premium content shortly.")

# 🔁 Keep the bot running
bot.infinity_polling()
