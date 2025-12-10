# src/handlers/user_handlers.py

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from src.db import add_or_update_request, is_approved, log_action
from src.config import ADMIN_ID
from src.logger import logger


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name

    if is_approved(uid):
        await update.message.reply_text("Welcome back! Use /help to see commands.")
        return

    add_or_update_request(uid, username)
    await update.message.reply_text("Your access is pending. Please wait for admin approval.")

    # Notify admin
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("Approve", callback_data=f"allow_{uid}"),
         InlineKeyboardButton("Deny", callback_data=f"deny_{uid}")]
    ])

    await context.bot.send_message(
        ADMIN_ID,
        f"New user requested access: {username} ({uid})",
        reply_markup=kb
    )

    log_action(uid, "requested_access")


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_approved(update.effective_user.id):
        await update.message.reply_text("Your access is pending.")
        return

    text = (
        "/email <email>\n"
        "/username <name>\n"
        "/phone <number>\n"
        "/domain <domain>\n"
        "/scan <ip>\n"
        "/top100 <ip>\n"
        "/ports <ip> <comma_ports>"
    )

    await update.message.reply_text(text)
