from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Templates"), KeyboardButton("Add Template +")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("Головне меню:", reply_markup=reply_markup)

async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Templates"), KeyboardButton("Add Template +")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if update.message:
        await update.message.reply_text("Головне меню:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text("Головне меню:", reply_markup=reply_markup)