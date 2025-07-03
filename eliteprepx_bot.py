import os
import telebot
from telebot import types
from datetime import datetime

BOT_TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)
ADMIN_ID = 5904719884

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

PREF_FILE = "data/user_preferences.txt"
QUIZ_FILE = "data/quiz_scores.txt"

# Helper: Show main menu
def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("\U0001F4D8 GATE", "\U0001F4D7 JEE", "\U0001F4D5 NEET")
    markup.row("\U0001F916 AI/ML", "\U0001F4BB Interview Kits")
    markup.row("\U0001F48E Get Premium Access", "\U0001F4DA Smart Recommender")
    markup.row("\U0001F4C5 Daily Digest", "\U0001F3B2 Take Quiz")
    bot.send_message(chat_id, "\U0001F44B *Welcome to ElitePrepX!*\n\nChoose a category below:", parse_mode="Markdown", reply_markup=markup)

# Start
@bot.message_handler(commands=['start'])
def welcome(msg):
    user = msg.from_user
    os.makedirs("data", exist_ok=True)
    with open("data/users.txt", "a") as f:
        f.write(f"{user.first_name} (@{user.username}) - {user.id}\n")
    show_main_menu(msg.chat.id)

# Free content
@bot.message_handler(func=lambda m: m.text in ["\U0001F4D8 GATE", "\U0001F4D7 JEE", "\U0001F4D5 NEET", "\U0001F916 AI/ML", "\U0001F4BB Interview Kits"])
def free_reply(m):
    key = {
        "\U0001F4D8 GATE": "gate",
        "\U0001F4D7 JEE": "jee",
        "\U0001F4D5 NEET": "neet",
        "\U0001F916 AI/ML": "ai",
        "\U0001F4BB Interview Kits": "interview"
    }[m.text]
    with open(PREF_FILE, "a") as f:
        f.write(f"{m.from_user.id},{key}\n")
    bot.reply_to(m, f"\U0001F4C2 Free {key.upper()} Materials:\n{FREE_LINKS[key]}")

# Premium access
@bot.message_handler(func=lambda m: m.text == "\U0001F48E Get Premium Access")
def show_premium_options(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("\U0001F3AF GATE Premium", "\U0001F9EA JEE Premium", "\U0001FA7A NEET Premium")
    markup.row("\U0001F9E0 AI/ML Premium", "\U0001F468‍\U0001F4BC Interview Premium")
    markup.row("\U0001F4E6 All Access - ₹49")
    markup.row("\U0001F519 Back to Main Menu")
    bot.send_message(m.chat.id, "Select a premium plan:", reply_markup=markup)

@bot.message_handler(func=lambda m: "premium" in m.text.lower() or m.text == "\U0001F519 Back to Main Menu")
def handle_premium_request(m):
    if m.text == "\U0001F519 Back to Main Menu":
        show_main_menu(m.chat.id)
        return

    subject_map = {
        "gate": ("gate", 29), "jee": ("jee", 29), "neet": ("neet", 29),
        "ai/ml": ("ai", 39), "interview": ("interview", 39),
        "all": ("all", 49)
    }
    for key in subject_map:
        if key in m.text.lower():
            category, price = subject_map[key]
            bot.reply_to(m, f"\U0001F4B8 *{category.upper()} Premium* - ₹{price}\nPay via UPI: `patetichandu@oksbi`\nSend screenshot here.", parse_mode="Markdown")
            return

# Screenshot verification
@bot.message_handler(content_types=['photo', 'document'])
def handle_payment_screenshot(msg):
    user = msg.from_user
    bot.forward_message(ADMIN_ID, msg.chat.id, msg.message_id)
    bot.send_message(ADMIN_ID, f"\U0001F4F8 Screenshot from @{user.username or 'NoUsername'} | ID: `{user.id}`", parse_mode="Markdown")
    bot.reply_to(msg, "\u2705 Screenshot received. Verification in progress.")

# Admin manually sends premium content
@bot.message_handler(commands=['give'])
def give_premium(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        _, user_id, category = msg.text.split()
        if category not in PREMIUM_LINKS:
            return bot.reply_to(msg, f"Invalid category.")
        bot.send_message(int(user_id), f"✅ *Your {category.upper()} Premium*:\n{PREMIUM_LINKS[category]}", parse_mode="Markdown")
        bot.reply_to(msg, f"Sent to {user_id}")
    except:
        bot.reply_to(msg, "Invalid command. Use /give <user_id> <category>")

# AI Recommender based on preferences
@bot.message_handler(func=lambda m: m.text == "\U0001F4DA Smart Recommender")
def smart_recommend(msg):
    user_id = str(msg.from_user.id)
    if os.path.exists(PREF_FILE):
        with open(PREF_FILE, "r") as f:
            lines = [line.strip() for line in f if line.startswith(user_id)]
        if lines:
            subjects = list({line.split(',')[1] for line in lines})
            links = [FREE_LINKS[s] for s in subjects if s in FREE_LINKS]
            response = "\U0001F4CB *Recommended PDFs for You:*\n" + "\n".join(links)
        else:
            response = "\u2753 No preference found. Please explore some subjects first."
    else:
        response = "\u2753 No data available."
    bot.reply_to(msg, response, parse_mode="Markdown")

# Daily Digest (Basic Simulated)
@bot.message_handler(func=lambda m: m.text == "\U0001F4C5 Daily Digest")
def daily_digest(msg):
    bot.reply_to(msg, "📰 *ElitePrepX Daily Digest*\n- Tip: Revise at least 2 topics/day\n- New Premium Added: GATE Mock 2025\n- Trending: AI Interview Questions\n(Feature under development)", parse_mode="Markdown")

# Quiz feature (demo only)
@bot.message_handler(func=lambda m: m.text == "\U0001F3B2 Take Quiz")
def quiz(msg):
    question = "Which exam is for engineering PG in India?"
    options = ["NEET", "GATE", "JEE"]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for opt in options:
        markup.row(opt)
    bot.send_message(msg.chat.id, question, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["NEET", "GATE", "JEE"])
def handle_quiz_answer(m):
    score = 1 if m.text == "GATE" else 0
    with open(QUIZ_FILE, "a") as f:
        f.write(f"{m.from_user.id},{score},{datetime.now()}\n")
    if score:
        bot.reply_to(m, "✅ Correct! You’ve earned a quiz reward.")
    else:
        bot.reply_to(m, "❌ Incorrect. Try again tomorrow.")

# Keep bot alive
bot.infinity_polling()
