# This is your updated Telegram bot code with tight integration to Drive automation features.
# It enforces premium plan selection before screenshot submission and adds auto-granting with inline admin approval.

import os
import telebot
from telebot import types
from datetime import datetime
import csv

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
PENDING_FILE = "data/pending_purchases.txt"
GRANTED_LOG = "data/granted_purchases.txt"
UPLOAD_LOG = "C:/Users/patet/OneDrive/Desktop/eliteprepx-railway/data/upload_log.txt"

@bot.message_handler(commands=['start'])
def welcome(msg):
    user = msg.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else "NoUsername"
    name = user.first_name or "Unknown"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs("data", exist_ok=True)

    entry_text = f"{timestamp} - {name} ({username}) - {user_id}\n"
    txt_path = "data/users.txt"
    if not os.path.exists(txt_path):
        open(txt_path, "w").close()
    with open(txt_path, "r+") as f:
        if not any(str(user_id) in line for line in f.readlines()):
            f.write(entry_text)

    csv_path = "data/users.csv"
    if not os.path.exists(csv_path):
        with open(csv_path, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Name", "Username", "UserID"])
    with open(csv_path, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, name, username, user_id])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📘 GATE", "📗 JEE", "📕 NEET")
    markup.add("🤖 AI/ML", "🧠 Interview Kits")
    markup.add("💎 Get Premium Access")
    markup.add("📚 Smart Recommender", "🗓️ Daily Digest", "🎯 Take Quiz")
    bot.send_message(
        msg.chat.id,
        """👋 *Welcome to ElitePrepX!*

Choose a category below:""",
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
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    markup = InlineKeyboardMarkup()
    options = [
        ("🎯 GATE Premium - ₹29", "gate"),
        ("🧪 JEE Premium - ₹29", "jee"),
        ("🧬 NEET Premium - ₹29", "neet"),
        ("🤖 AI/ML Premium - ₹39", "ai"),
        ("🧠 Interview Premium - ₹39", "interview"),
        ("💼 All Access - ₹49", "all")
    ]
    for text, val in options:
        markup.add(InlineKeyboardButton(text, callback_data=f"premium_{val}"))
    bot.send_message(m.chat.id, "💎 *Choose a Premium Plan:*", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("premium_"))
def handle_premium_buttons(call):
    key = call.data.replace("premium_", "")
    price = {"gate": 29, "jee": 29, "neet": 29, "ai": 39, "interview": 39, "all": 49}[key]
    with open(PENDING_FILE, "a") as f:
        f.write(f"{call.from_user.id},{key}\n")
    bot.send_message(call.message.chat.id, f"💳 *{key.upper()} Premium* - ₹{price}\nPay via UPI: `patetichandu@oksbi`\nSend screenshot here.", parse_mode="Markdown")

@bot.message_handler(content_types=['photo', 'document'])
def handle_payment_screenshot(msg):
    user = msg.from_user
    user_id = str(user.id)
    username = f"@{user.username}" if user.username else "NoUsername"

    bot.forward_message(ADMIN_ID, msg.chat.id, msg.message_id)

    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE, "r") as f:
            lines = [line.strip() for line in f.readlines()]
        user_line = next((line for line in lines if user_id in line), None)
    else:
        user_line = None

    if user_line:
        plan = user_line.split(",")[1]
        from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ Give ACCESS", callback_data=f"approve_{user_id}_{plan}"))
        bot.send_message(ADMIN_ID, f"📸 Screenshot from {username} | ID: `{user_id}`\nSelected Plan: *{plan.upper()}*", parse_mode="Markdown", reply_markup=markup)
    else:
        bot.send_message(ADMIN_ID, f"📸 Screenshot from {username} | ID: `{user_id}`\n⚠️ *No plan selected yet!*", parse_mode="Markdown")

    bot.reply_to(msg, "✅ Screenshot received. Please wait for admin verification.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_"))
def approve_user_plan(call):
    _, uid, plan = call.data.split("_")
    if plan not in PREMIUM_LINKS:
        return bot.send_message(ADMIN_ID, "⚠️ Invalid plan code.")

    bot.send_message(int(uid), f"🎉 *Access Granted!*\nYour {plan.upper()} Premium Materials:\n{PREMIUM_LINKS[plan]}", parse_mode="Markdown")
    bot.send_message(ADMIN_ID, f"✅ Sent {plan.upper()} premium to user ID {uid}")

    # Log granted access
    with open(GRANTED_LOG, "a") as f:
        f.write(f"{datetime.now()}, {uid}, {plan}\n")

    # Remove user from pending
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE, "r") as f:
            lines = [line.strip() for line in f if not line.startswith(uid)]
        with open(PENDING_FILE, "w") as f:
            f.write("\n".join(lines) + "\n")

@bot.message_handler(commands=['give'])
def give_premium(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        _, user_id, category = msg.text.split()
        if category not in PREMIUM_LINKS:
            return bot.reply_to(msg, "Invalid category.")
        bot.send_message(int(user_id), f"✅ *Your {category.upper()} Premium*:\n{PREMIUM_LINKS[category]}", parse_mode="Markdown")
        bot.reply_to(msg, f"Sent to {user_id}")
    except:
        bot.reply_to(msg, "Invalid command. Use /give <user_id> <category>")

bot.infinity_polling()
