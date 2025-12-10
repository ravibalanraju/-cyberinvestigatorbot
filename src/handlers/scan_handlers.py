# src/handlers/scan_handlers.py

from telegram import Update
from telegram.ext import ContextTypes
from src.db import is_approved, log_action
from src.utils.rate_limiter import rate_limiter
from src.utils.portscan import scan_ports
from src.logger import logger


async def scan_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if not is_approved(uid):
        await update.message.reply_text("Your access is pending.")
        return

    if not rate_limiter.allow(uid):
        await update.message.reply_text("Rate limit exceeded. Try later.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /scan <ip>")
        return

    ip = context.args[0]
    await update.message.reply_text("Scanning (this may take a few seconds)...")

    res = scan_ports(ip)
    if res is None:
        await update.message.reply_text("Scan failed or target forbidden.")
        return

    # Format output
    out = []
    for host, data in res.get("scan", {}).items():
        out.append(f"Host: {host}")
        ports = data.get("tcp", {})
        for p, info in ports.items():
            out.append(f"{p}/tcp — {info.get('state')} — {info.get('name')}")

    text = "\n".join(out) if out else "No open ports found."
    await update.message.reply_text(text)

    log_action(uid, f"scan {ip}")
