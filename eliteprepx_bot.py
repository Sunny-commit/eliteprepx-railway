import os
import telebot
from telebot import types

BOT_TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_ID = 5904719884

# 🔗 Drive links
FREE_LINKS = {
    "gate": "https://drive.google.com/your-free-gate",
    "jee": "https://drive.google.com/your-free-jee",
    "neet": "https://drive.google.com/your-free-neet",
    "ai": "https://drive.google.com/your-free-ai",
    "interview": "https://drive.google.com/your-free-interview"
}
PREMIUM_LINKS = {
    "gate": "https://drive.google.com/your-premium-gate",
    "jee": "https://drive.google.com/your-premium-jee",
    "neet": "https://drive.google.com/your-premium-neet",
    "ai": "https://drive.google.com/your-premium-ai",
    "interview": "https://drive.google.com/your-premium-interview",
    "all": "https://drive.google.com/your-full-premium"
}

# 🧾 Start command
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

# 🆓 Free content
@bot.message_handler(func=lambda m: m.text in ["📘 GATE", "📗 JEE", "📕 NEET", "🤖 AI/ML", "💻 Interview Kits"])
def free_reply(m):
    key = {
        "📘 GATE": "gate",
        "📗 JEE": "jee",
        "📕 NEET": "neet",
        "🤖 AI/ML": "ai",
        "💻 Interview Kits": "interview"
    }[m.text]
    bot.reply_to(m, f"📂 Free {m.text} Materials:\n{FREE_LINKS[key]}")

# 💎 Premium trigger
@bot.message_handler(func=lambda m: m.text == "💎 Get Premium Access")
def show_premium_options(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🎯 GATE Premium", "🧪 JEE Premium", "🩺 NEET Premium")
    markup.row("🧠 AI/ML Premium", "🧑‍💼 Interview Premium")
    markup.row("📦 All Access - ₹49")
    bot.send_message(m.chat.id, "💎 Select a premium pack to continue 👇", reply_markup=markup)

# 💰 Show UPI and ask screenshot
@bot.message_handler(func=lambda m: m.text.endswith("Premium") or "All Access" in m.text)
def premium_request(m):
    subject_map = {
        "🎯 gate premium": ("gate", 29),
        "🧪 jee premium": ("jee", 29),
        "🩺 neet premium": ("neet", 29),
        "🧠 ai/ml premium": ("ai", 39),
        "🧑‍💼 interview premium": ("interview", 39),
        "📦 all access - ₹49": ("all", 49)
    }
    text = m.text.lower().strip()
    if text not in subject_map:
        bot.reply_to(m, "❓ Invalid selection.")
        return
    category, price = subject_map[text]
    bot.reply_to(
        m,
        f"💎 *{category.upper()} Premium Access* - ₹{price}\n\nUPI: `patetichandu@oksbi`\n📸 Send payment *screenshot here* for verification.",
        parse_mode="Markdown"
    )

# 📸 Screenshot handler
@bot.message_handler(content_types=['photo', 'document'])
def handle_payment_screenshot(msg):
    user = msg.from_user
    caption = msg.caption or "No caption"
    bot.forward_message(chat_id=ADMIN_ID, from_chat_id=msg.chat.id, message_id=msg.message_id)
    bot.send_message(
        ADMIN_ID,
        f"📸 *Screenshot Received*\n👤 @{user.username or 'NoUsername'}\n🆔 `{user.id}`\n✏️ Caption: _{caption}_",
        parse_mode="Markdown"
    )
    bot.reply_to(msg, "✅ Screenshot received!\nWe’ll verify and send your content shortly.")

# 🔐 Admin command
@bot.message_handler(commands=['give'])
def give_premium(msg):
    if msg.from_user.id != ADMIN_ID:
        bot.reply_to(msg, "⛔ Not authorized.")
        return

    try:
        _, user_id, category = msg.text.split()
        if category not in PREMIUM_LINKS:
            bot.reply_to(msg, f"❌ Invalid category. Use: {', '.join(PREMIUM_LINKS)}")
            return

        filepath = "data/premium_users.txt"
        os.makedirs("data", exist_ok=True)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                if f"{user_id}-{category}" in f.read():
                    bot.reply_to(msg, "⚠️ Already sent.")
                    return

        bot.send_message(int(user_id), f"✅ Your *{category.upper()}* premium content:\n{PREMIUM_LINKS[category]}", parse_mode="Markdown")
        with open(filepath, "a") as f:
            f.write(f"{user_id}-{category}\n")

        bot.reply_to(msg, f"✅ Sent to {user_id}")

    except Exception as e:
        bot.reply_to(msg, f"❌ Error: {str(e)}")

# ⏳ Stay alive
bot.infinity_polling()
