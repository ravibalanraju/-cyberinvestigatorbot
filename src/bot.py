# src/bot.py
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler
)
from src.config import BOT_TOKEN, ADMIN_ID
from src.handlers.user_handlers import start_handler, help_handler
from src.handlers.admin_handlers import cmd_allow, cmd_list_pending
from src.handlers.scan_handlers import scan_cmd
from src.logger import logger

# Callback handler for inline buttons
async def callback_query_handler(update, context):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("allow_") and update.effective_user.id == ADMIN_ID:
        uid = int(data.split("_")[1])
        from src.db import approve_user
        approve_user(uid)
        await query.edit_message_text(f"User {uid} approved by admin.")

    elif data.startswith("deny_") and update.effective_user.id == ADMIN_ID:
        uid = int(data.split("_")[1])
        from src.db import deny_user
        deny_user(uid)
        await query.edit_message_text(f"User {uid} denied by admin.")


def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))

    # Admin commands
    app.add_handler(CommandHandler("allow", cmd_allow))
    app.add_handler(CommandHandler("list_pending", cmd_list_pending))

    # Scanning
    app.add_handler(CommandHandler("scan", scan_cmd))

    # Inline button callbacks
    app.add_handler(CallbackQueryHandler(callback_query_handler))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    start_bot()
