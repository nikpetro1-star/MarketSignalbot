import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import TOKEN, TRIAL_LINK, TRIAL_HOURS
from database import add_user, get_expired


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    add_user(user_id)

    await update.message.reply_text(
        f"48H VIP Trial Access:\n{TRIAL_LINK}\n\nJoin the group and follow signals."
    )


async def expiry_checker(app: Application):
    while True:
        expired_users = get_expired(TRIAL_HOURS)

        for (user_id,) in expired_users:
            try:
                await app.bot.send_message(
                    user_id,
                    "Your 48h trial ended. Upgrade to VIP."
                )
            except:
                pass

        await asyncio.sleep(3600)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    loop = asyncio.get_event_loop()
    loop.create_task(expiry_checker(app))

    app.run_polling()


if __name__ == "__main__":
    main()
