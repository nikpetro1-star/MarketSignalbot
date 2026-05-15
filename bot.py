import os
import time
import asyncio
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ======================
# ENV VARIABLES (Railway)
# ======================
TOKEN = os.getenv("TOKEN")
TRIAL_LINK = os.getenv("TRIAL_LINK")
TRIAL_HOURS = int(os.getenv("TRIAL_HOURS", 48))

# ======================
# DATABASE
# ======================
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    start_time INTEGER
)
""")
conn.commit()


def add_user(user_id):
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (user_id, start_time) VALUES (?, ?)",
            (user_id, int(time.time()))
        )
        conn.commit()


def get_expired(hours):
    cutoff = int(time.time()) - hours * 3600
    cur.execute("SELECT user_id FROM users WHERE start_time < ?", (cutoff,))
    return cur.fetchall()


# ======================
# COMMANDS
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    add_user(user_id)

    await update.message.reply_text(
        f"🔥 48H VIP Trial Access\n\n{TRIAL_LINK}\n\nJoin the group and follow live signals."
    )


# ======================
# EXPIRY SYSTEM
# ======================
async def expiry_checker(app: Application):
    while True:
        expired_users = get_expired(TRIAL_HOURS)

        for (user_id,) in expired_users:
            try:
                await app.bot.send_message(
                    user_id,
                    "⛔ Your 48h trial ended.\n\nUpgrade to VIP to continue receiving signals."
                )
            except:
                pass

        await asyncio.sleep(3600)


# ======================
# POST INIT (IMPORTANT FIX)
# ======================
async def post_init(app):
    app.create_task(expiry_checker(app))


# ======================
# MAIN
# ======================
def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()


if __name__ == "__main__":
    main()
