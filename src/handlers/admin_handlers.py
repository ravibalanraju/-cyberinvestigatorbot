# src/handlers/admin_handlers.py

from telegram import Update
from telegram.ext import ContextTypes
from src.config import ADMIN_ID
from src.db import approve_user, deny_user, list_pending, log_action
from src.logger import logger


async def cmd_allow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_user.id
    if sender_id != ADMIN_ID:
        return

    args = context.args
    if not args:
        await update.message.reply_text("Usage: /allow <user_id>")
        return

    uid = int(args[0])
    approve_user(uid)
    log_action(sender_id, f"allowed {uid}")
    await update.message.reply_text(f"User {uid} approved.")


async def cmd_list_pending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    pend = list_pending()
    if not pend:
        await update.message.reply_text("No pending users.")
        return

    text = "\n".join([f"{u[0]} — {u[1]} — {u[2]}" for u in pend])
    await update.message.reply_text(text)
