import os
import telebot
from telebot import types
from datetime import datetime
import csv

BOT_TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)
ADMIN_ID = 5904719884

# Paths
PREF_FILE = "data/user_preferences.txt"
QUIZ_FILE = "data/quiz_scores.txt"
PENDING_FILE = "data/pending_purchases.txt"
GRANTED_LOG = "data/granted_purchases.txt"
USERS_TXT = "data/users.txt"
USERS_CSV = "data/users.csv"
UPLOAD_LOG = "C:/Users/patet/OneDrive/Desktop/eliteprepx-railway/data/upload_log.txt"

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

# ---------- START ----------
@bot.message_handler(commands=['start'])
def welcome(msg):
    user = msg.from_user
    uid = user.id
    name = user.first_name or "Unknown"
    username = f"@{user.username}" if user.username else "NoUsername"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs("data", exist_ok=True)
    if not os.path.exists(USERS_TXT): open(USERS_TXT, "w").close()
    with open(USERS_TXT, "r+") as f:
        if not any(str(uid) in line for line in f.readlines()):
            f.write(f"{timestamp} - {name} ({username}) - {uid}\n")
    if not os.path.exists(USERS_CSV):
        with open(USERS_CSV, "w", newline='') as f:
            csv.writer(f).writerow(["Timestamp", "Name", "Username", "UserID"])
    with open(USERS_CSV, "a", newline='') as f:
        csv.writer(f).writerow([timestamp, name, username, uid])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📘 GATE", "📗 JEE", "📕 NEET")
    markup.add("🤖 AI/ML", "🧠 Interview Kits")
    markup.add("💎 Get Premium Access")
    markup.add("📚 Smart Recommender", "🗓️ Daily Digest", "🎯 Take Quiz")
    bot.send_message(msg.chat.id, "👋 *Welcome to ElitePrepX!*\n\nChoose a category below:", parse_mode="Markdown", reply_markup=markup)

# ---------- FREE MATERIAL ----------
@bot.message_handler(func=lambda m: m.text in ["📘 GATE", "📗 JEE", "📕 NEET", "🤖 AI/ML", "🧠 Interview Kits"])
def free_reply(m):
    subject = {
        "📘 GATE": "gate", "📗 JEE": "jee", "📕 NEET": "neet",
        "🤖 AI/ML": "ai", "🧠 Interview Kits": "interview"
    }[m.text]
    with open(PREF_FILE, "a") as f:
        f.write(f"{m.from_user.id},{subject}\n")
    bot.reply_to(m, f"📂 Free {subject.upper()} Materials:\n{FREE_LINKS[subject]}")

# ---------- PREMIUM OPTIONS ----------
@bot.message_handler(func=lambda m: m.text == "💎 Get Premium Access")
def premium_options(m):
    markup = types.InlineKeyboardMarkup()
    for label, key, price in [
        ("GATE", "gate", 29), ("JEE", "jee", 29), ("NEET", "neet", 29),
        ("AI/ML", "ai", 39), ("Interview", "interview", 39), ("All Access", "all", 49)
    ]:
        markup.add(types.InlineKeyboardButton(f"{label} Premium - ₹{price}", callback_data=f"premium_{key}"))
    bot.send_message(m.chat.id, "💎 *Choose a Premium Plan:*", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("premium_"))
def handle_premium_selection(call):
    plan = call.data.split("_")[1]
    price = {"gate":29, "jee":29, "neet":29, "ai":39, "interview":39, "all":49}[plan]
    with open(PENDING_FILE, "a") as f:
        f.write(f"{call.from_user.id},{plan}\n")
    bot.send_message(call.message.chat.id, f"💳 *{plan.upper()} Premium* - ₹{price}\nPay via UPI: `patetichandu@oksbi`\nSend screenshot here.", parse_mode="Markdown")

# ---------- PAYMENT HANDLING ----------
@bot.message_handler(content_types=['photo', 'document'])
def handle_payment_screenshot(msg):
    uid = str(msg.from_user.id)
    username = f"@{msg.from_user.username}" if msg.from_user.username else "NoUsername"
    bot.forward_message(ADMIN_ID, msg.chat.id, msg.message_id)

    user_line = None
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE) as f:
            user_line = next((line for line in f if uid in line), None)

    if user_line:
        plan = user_line.split(",")[1]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Give ACCESS", callback_data=f"approve_{uid}_{plan}"))
        bot.send_message(ADMIN_ID, f"📸 Screenshot from {username} | ID: `{uid}`\nPlan: *{plan.upper()}*", parse_mode="Markdown", reply_markup=markup)
    else:
        bot.send_message(ADMIN_ID, f"⚠️ Screenshot from {username} | ID: `{uid}`\n*No plan selected!*", parse_mode="Markdown")
    bot.reply_to(msg, "✅ Screenshot received. Please wait for admin verification.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_"))
def approve_user(call):
    _, uid, plan = call.data.split("_")
    if plan not in PREMIUM_LINKS:
        return bot.send_message(ADMIN_ID, "⚠️ Invalid plan.")

    bot.send_message(int(uid), f"🎉 *Access Granted!*\nYour {plan.upper()} Premium:\n{PREMIUM_LINKS[plan]}", parse_mode="Markdown")
    bot.send_message(ADMIN_ID, f"✅ Granted {plan.upper()} to user {uid}")
    with open(GRANTED_LOG, "a") as f:
        f.write(f"{datetime.now()},{uid},{plan}\n")
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE) as f:
            lines = [line for line in f if not line.startswith(uid)]
        with open(PENDING_FILE, "w") as f:
            f.writelines(lines)

# ---------- SMART RECOMMENDER ----------
@bot.message_handler(func=lambda m: m.text == "📚 Smart Recommender")
def smart_recommend(m):
    uid = str(m.from_user.id)
    if not os.path.exists(PREF_FILE):
        return bot.reply_to(m, "❗ No preference data available.")
    with open(PREF_FILE) as f:
        prefs = [line.strip().split(',')[1] for line in f if line.startswith(uid)]
    if prefs:
        links = [FREE_LINKS[p] for p in set(prefs) if p in FREE_LINKS]
        msg = "📋 *Recommended for You:*\n" + "\n".join(links)
    else:
        msg = "❗ No preferences found. Try exploring a few subjects first!"
    bot.send_message(m.chat.id, msg, parse_mode="Markdown")

# ---------- DAILY DIGEST ----------
@bot.message_handler(func=lambda m: m.text == "🗓️ Daily Digest")
def daily_digest(m):
    bot.send_message(m.chat.id, "🗞️ *ElitePrepX Digest*\n- Tip: Review 2 topics daily\n- Update: GATE 2025 Mocks\n- Hot: AI Interview Cheatsheets", parse_mode="Markdown")

# ---------- QUIZ ----------
@bot.message_handler(func=lambda m: m.text == "🎯 Take Quiz")
def quiz(m):
    question = "Which exam is for engineering PG in India?"
    opts = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for o in ["NEET", "GATE", "JEE"]: opts.add(o)
    bot.send_message(m.chat.id, question, reply_markup=opts)

@bot.message_handler(func=lambda m: m.text in ["NEET", "GATE", "JEE"])
def quiz_answer(m):
    score = 1 if m.text == "GATE" else 0
    with open(QUIZ_FILE, "a") as f:
        f.write(f"{m.from_user.id},{score},{datetime.now()}\n")
    msg = "✅ Correct! You earned a quiz reward." if score else "❌ Incorrect. Try again tomorrow."
    bot.send_message(m.chat.id, msg)

# ---------- ADMIN: LIST USERS ----------
@bot.message_handler(commands=['list_users'])
def list_users(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    if not os.path.exists(USERS_TXT):
        return bot.reply_to(msg, "No users yet.")
    with open(USERS_TXT, "r") as f:
        users = f.read()[-4000:]
    bot.send_message(msg.chat.id, f"📋 *Registered Users:*\n\n{users}", parse_mode="Markdown")

bot.infinity_polling()
