import os
import telebot
from telebot import types

BOT_TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)

# Track user info
@bot.message_handler(commands=['start'])
def welcome(msg):
    user = msg.from_user
    with open("users.txt", "a") as f:
        f.write(f"{user.first_name} (@{user.username}) - {user.id}\n")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📘 GATE", "📗 JEE", "📕 NEET")
    markup.row("🤖 AI/ML", "💻 Interview Kits")
    markup.row("💎 Premium Access")

    bot.send_message(
        msg.chat.id,
        "👋 *Welcome to ElitePrepX Bot!*\n\nChoose a category below:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: True)
def reply(m):
    text = m.text.lower()
    if "gate" in text:
        bot.reply_to(m, "📘 GATE PDF:\nhttps://your-link")
    elif "ml" in text or "ai" in text:
        bot.reply_to(m, "🤖 AI/ML PDF:\nhttps://your-link")
    elif "jee" in text:
        bot.reply_to(m, "📗 JEE Materials:\nhttps://your-link")
    elif "neet" in text:
        bot.reply_to(m, "📕 NEET PDFs:\nhttps://your-link")
    elif "interview" in text:
        bot.reply_to(m, "💻 Interview Prep:\nhttps://your-link")
    elif "premium" in text:
        premium_info(m)
    elif "i paid" in text:
        send_premium_links(m)
    else:
        bot.reply_to(m, "❓ Choose a valid category from the buttons.")

def premium_info(msg):
    response = """💎 *ElitePrepX Premium Access*

📚 Get exclusive PDFs for:
- UPSC Notes
- JEE Advanced Solutions
- GATE Previous Papers
- NEET Mock Tests
- AI/ML Projects & eBooks
- SDE Interview Kits

💰 One-time Payment: ₹49
📲 UPI: `eliteprepx@paytm`
📸 Send screenshot after payment.

✅ Files will be shared directly here.
"""
    bot.reply_to(msg, response, parse_mode="Markdown")

def send_premium_links(msg):
    bot.reply_to(msg, """✅ Payment received!

📂 UPSC Notes: https://...
📂 GATE PDFs: https://...
📂 AI/ML eBooks: https://...
📂 Coding Roadmap: https://...
📂 Interview Kits: https://...
""")

bot.infinity_polling()
