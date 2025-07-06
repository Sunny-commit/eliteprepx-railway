import os
import csv
import telebot
from telebot import types
from datetime import datetime

BOT_TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)
ADMIN_ID = 5904719884

FREE_LINKS = {
    "gate": "https://drive.google.com/file/d/1BatyPPAPGKbszQmLgk6UQMjP87LyyN__/view?usp=sharing",
    "jee": "https://drive.google.com/file/d/1GTO6XS6JUlzv_NMghQozd553fkM5HVhj/view?usp=sharing",
    "neet": "https://drive.google.com/file/d/1e7P878YjfXpVBc68dne_GHy11H86aGF5/view?usp=sharing",
    "ai": "https://drive.google.com/file/d/1XVx4bGjcwiylqrlOVwPUtMu5Ia_GMfIA/view?usp=sharing",
    "interview": "https://drive.google.com/file/d/1NUawkwaHqeUU65_NsAYb2Ol5n3uFhEQ_/view?usp=sharing"
}

PREMIUM_LINKS = {
    "gate": "https://drive.google.com/drive/folders/1LTpsruxkCYh5YOtJhlP7Ony7Iwv80k08?usp=sharing",
    "jee": "https://drive.google.com/drive/folders/1b7W_kkjMhcL39xDbZkV_jKK0i4XOmOmi?usp=sharing",
    "neet": "https://drive.google.com/drive/folders/1UllrkYS9uJUDVQErUGG_13QZmdLF6xrm?usp=sharing",
    "ai": "https://drive.google.com/drive/folders/1IWl7u561verrrS5RobHFGHyPniYF9241?usp=sharing",
    "interview": "https://drive.google.com/drive/folders/17ConfzIT6L2a7tvwJ9ndtHFltPeci91k?usp=sharing",
    "all": "https://drive.google.com/drive/folders/16Ps3a2WVHbtYWean7s8jBCj8Xg10-mpm?usp=sharing"
}

PREF_FILE = "data/user_preferences.txt"
QUIZ_FILE = "data/quiz_scores.txt"


@bot.message_handler(commands=['start'])
def welcome(msg):
    user = msg.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else "NoUsername"
    name = user.first_name or "Unknown"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs("data", exist_ok=True)

    # Save to users.txt if not already present
    txt_path = "data/users.txt"
    if not os.path.exists(txt_path):
        open(txt_path, "w").close()

    with open(txt_path, "r+") as f:
        lines = f.readlines()
        if not any(str(user_id) in line for line in lines):
            f.write(f"{timestamp} - {name} ({username}) - {user_id}\n")

    # Save to users.csv
    csv_path = "data/users.csv"
    if not os.path.exists(csv_path):
        with open(csv_path, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Name", "Username", "UserID"])
    with open(csv_path, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, name, username, user_id])

    # Send welcome
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📘 GATE", "📗 JEE", "📕 NEET")
    markup.add("🤖 AI/ML", "🧠 Interview Kits")
    markup.add("💎 Get Premium Access")
    markup.add("📚 Smart Recommender", "🗓️ Daily Digest", "🎯 Take Quiz")

    bot.send_message(
        msg.chat.id,
        """👋 *Welcome to ElitePrepX!*\n\nChoose a category below:""",
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: m.text in ["📘 GATE", "📗 JEE", "📕 NEET", "🤖 AI/ML", "🧠 Interview Kits"])
def free_reply(m):
    key = {
        "📘 GATE": "gate",
        "📗 JEE": "jee",
        "📕 NEET": "neet",
        "🤖 AI/ML": "ai",
        "🧠 Interview Kits": "interview"
    }[m.text]
    with open(PREF_FILE, "a") as f:
        f.write(f"{m.from_user.id},{key}\n")
    bot.reply_to(m, f"📂 Free {key.upper()} Materials:\n{FREE_LINKS[key]}")


@bot.message_handler(func=lambda m: m.text == "💎 Get Premium Access")
def premium_options(m):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎯 GATE Premium - ₹29", callback_data="premium_gate"))
    markup.add(types.InlineKeyboardButton("🧪 JEE Premium - ₹29", callback_data="premium_jee"))
    markup.add(types.InlineKeyboardButton("🧬 NEET Premium - ₹29", callback_data="premium_neet"))
    markup.add(types.InlineKeyboardButton("🤖 AI/ML Premium - ₹39", callback_data="premium_ai"))
    markup.add(types.InlineKeyboardButton("🧠 Interview Premium - ₹39", callback_data="premium_interview"))
    markup.add(types.InlineKeyboardButton("💼 All Access - ₹49", callback_data="premium_all"))
    bot.send_message(m.chat.id, "💎 *Choose a Premium Plan:*", reply_markup=markup, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data.startswith("premium_"))
def handle_premium_buttons(call):
    key = call.data.replace("premium_", "")
    prices = {
        "gate": 29, "jee": 29, "neet": 29,
        "ai": 39, "interview": 39, "all": 49
    }
    price = prices[key]
    bot.send_message(call.message.chat.id, f"💳 *{key.upper()} Premium* - ₹{price}\nPay via UPI: `patetichandu@oksbi`\nSend screenshot here.", parse_mode="Markdown")


@bot.message_handler(content_types=['photo', 'document'])
def handle_payment_screenshot(msg):
    user = msg.from_user
    bot.forward_message(ADMIN_ID, msg.chat.id, msg.message_id)
    bot.send_message(ADMIN_ID, f"📸 Screenshot from @{user.username or 'NoUsername'} | ID: `{user.id}`", parse_mode="Markdown")
    bot.reply_to(msg, "✅ Screenshot received. Verification in progress.")


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


@bot.message_handler(func=lambda m: m.text == "📚 Smart Recommender")
def smart_recommend(msg):
    user_id = str(msg.from_user.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔙 Back to Main Menu")
    if os.path.exists(PREF_FILE):
        with open(PREF_FILE, "r") as f:
            lines = [line.strip() for line in f if line.startswith(user_id)]
        if lines:
            subjects = list({line.split(',')[1] for line in lines})
            links = [FREE_LINKS[s] for s in subjects if s in FREE_LINKS]
            response = "📋 *Recommended PDFs for You:*\n" + "\n".join(links)
        else:
            response = "❓ No preference found. Please explore some subjects first."
    else:
        response = "❓ No data available."
    bot.send_message(msg.chat.id, response, parse_mode="Markdown", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == "🗓️ Daily Digest")
def daily_digest(msg):
    bot.reply_to(msg, "📰 *ElitePrepX Daily Digest*\n- Tip: Revise 2 topics/day\n- New Premium: GATE Mock 2025\n- Trending: AI Interview Questions\n(Feature under development)", parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.text == "🎯 Take Quiz")
def quiz(msg):
    question = "Which exam is for engineering PG in India?"
    options = ["NEET", "GATE", "JEE"]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for opt in options:
        markup.add(opt)
    markup.add("🔙 Back to Main Menu")
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


@bot.message_handler(func=lambda m: m.text == "🔙 Back to Main Menu")
def back_to_main_menu(msg):
    welcome(msg)


bot.infinity_polling()
