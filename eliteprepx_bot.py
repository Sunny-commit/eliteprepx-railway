import os
import telebot
from telebot import types

BOT_TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_ID = 5904719884

# ✅ Premium links
PREMIUM_LINKS = {
    "gate": "https://drive.google.com/your-gate-link",
    "jee": "https://drive.google.com/your-jee-link",
    "neet": "https://drive.google.com/your-neet-link",
    "ai": "https://drive.google.com/your-ai-link",
    "interview": "https://drive.google.com/your-interview-link",
    "all": "https://drive.google.com/your-full-premium-pack"
}

# ✅ Start Command
@bot.message_handler(commands=['start'])
def welcome(msg):
    user = msg.from_user
    os.makedirs("data", exist_ok=True)
    with open("data/users.txt", "a") as f:
        f.write(f"{user.first_name} (@{user.username}) - {user.id}\n")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📘 GATE", "📗 JEE", "📕 NEET")
    markup.row("🤖 AI/ML", "💻 Interview Kits")
    markup.row("💎 Get Premium Access")

    bot.send_message(
        msg.chat.id,
        "👋 *Welcome to ElitePrepX!*\n\n🎓 Your all-in-one resource bot for:\n- Competitive Exams\n- AI/ML Projects\n- Interview Prep\n\nSelect a category to get started 👇",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ✅ Response Handler
@bot.message_handler(func=lambda m: m.text is not None)
def reply(m):
    text = m.text.lower().strip()

    if "i paid" in text:
        bot.reply_to(m, "❗To unlock premium content, please send a *payment screenshot*. No text-based confirmation allowed.", parse_mode="Markdown")
        return

    if text == "📘 gate":
        gate_premium_info(m)
    elif text == "📗 jee":
        jee_premium_info(m)
    elif text == "📕 neet":
        neet_premium_info(m)
    elif text == "🤖 ai/ml":
        ai_premium_info(m)
    elif text == "💻 interview kits":
        interview_premium_info(m)
    elif "premium" in text:
        all_premium_info(m)
    else:
        bot.reply_to(m, "❓ Please use the buttons below to navigate.")

# ✅ Subject Info Functions
def gate_premium_info(msg):
    bot.reply_to(msg, "📘 *GATE Premium Access* - ₹29\nPay via UPI: `patetichandu@oksbi`\nSend screenshot here.", parse_mode="Markdown")

def jee_premium_info(msg):
    bot.reply_to(msg, "📗 *JEE Premium Access* - ₹29\nPay via UPI: `patetichandu@oksbi`\nSend screenshot here.", parse_mode="Markdown")

def neet_premium_info(msg):
    bot.reply_to(msg, "📕 *NEET Premium Access* - ₹29\nPay via UPI: `patetichandu@oksbi`\nSend screenshot here.", parse_mode="Markdown")

def ai_premium_info(msg):
    bot.reply_to(msg, "🤖 *AI/ML Premium Access* - ₹39\nPay via UPI: `patetichandu@oksbi`\nSend screenshot here.", parse_mode="Markdown")

def interview_premium_info(msg):
    bot.reply_to(msg, "💻 *Interview Kits Premium* - ₹39\nPay via UPI: `patetichandu@oksbi`\nSend screenshot here.", parse_mode="Markdown")

def all_premium_info(msg):
    bot.reply_to(msg, """💎 *ElitePrepX Full Premium Access*
📃 All Subjects Included:
- UPSC, GATE, JEE, NEET, AI/ML, Interview Kits

💰 ₹49 via UPI: `patetichandu@oksbi`
📸 Send your payment *screenshot here*.
⏳ We’ll verify and send links soon.""", parse_mode="Markdown")

# ✅ Screenshot Handler
@bot.message_handler(content_types=['photo', 'document'])
def handle_payment_screenshot(msg):
    user = msg.from_user
    caption = msg.caption if msg.caption else "No caption"
    bot.forward_message(chat_id=ADMIN_ID, from_chat_id=msg.chat.id, message_id=msg.message_id)
    bot.send_message(
        ADMIN_ID,
        f"📸 *Screenshot Received*\n👤 @{user.username or 'NoUsername'}\n🆔 `{user.id}`\n✏️ _{caption}_",
        parse_mode="Markdown"
    )
    bot.reply_to(msg, "✅ Screenshot received!\nYour payment is being verified.\nYou’ll get the premium content shortly.")

# ✅ Admin Command to Manually Send Content
@bot.message_handler(commands=['give'])
def manual_send_premium(msg):
    if msg.from_user.id != ADMIN_ID:
        bot.reply_to(msg, "⛔ You're not authorized to use this command.")
        return

    try:
        parts = msg.text.split()
        if len(parts) != 3:
            bot.reply_to(msg, "❗Usage: /give <user_id> <category>")
            return

        user_id, category = parts[1], parts[2].lower()
        if category not in PREMIUM_LINKS:
            bot.reply_to(msg, f"❌ Invalid category. Choose: {', '.join(PREMIUM_LINKS.keys())}")
            return

        # ✅ Check if already sent
        os.makedirs("data", exist_ok=True)
        track_file = "data/premium_users.txt"
        if os.path.exists(track_file):
            with open(track_file, "r") as f:
                if f"{user_id}-{category}" in f.read():
                    bot.reply_to(msg, f"⚠️ Already sent {category} premium to user {user_id}.")
                    return

        # ✅ Send premium
        bot.send_message(chat_id=user_id,
                         text=f"✅ Here's your *{category.upper()}* premium content:\n{PREMIUM_LINKS[category]}",
                         parse_mode="Markdown")

        # ✅ Log it
        with open(track_file, "a") as f:
            f.write(f"{user_id}-{category}\n")

        bot.reply_to(msg, f"✅ Sent {category.upper()} premium to user ID {user_id}.")

    except Exception as e:
        bot.reply_to(msg, f"⚠️ Error: {str(e)}")

# ✅ Start the Bot
bot.infinity_polling()
