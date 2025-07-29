import os
import json
from pathlib import Path
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

from services.image_processor import process_template

from handlers.menu import send_main_menu

CHOOSE_TEMPLATE, SEND_IMAGE = range(2)
user_template_state = {}

async def templates_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_folder = Path(f"user_templates/{user_id}")
    if not user_folder.exists():
        await update.message.reply_text("У тебе ще немає шаблонів 🙁")
        return ConversationHandler.END

    templates = [f.name for f in user_folder.glob("*.json")]
    if not templates:
        await update.message.reply_text("Немає шаблонів 🙁")
        return ConversationHandler.END

    context.user_data["template_list"] = templates

    # Додаємо кнопку "⬅️ Назад"
    keyboard = [[KeyboardButton(name)] for name in templates]
    keyboard.append([KeyboardButton("⬅️ Назад")])

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Вибери шаблон:", reply_markup=reply_markup)
    return CHOOSE_TEMPLATE

async def choose_template(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "⬅️ Назад":
        await send_main_menu(update, context)
        return ConversationHandler.END

    user_id = update.effective_user.id
    user_folder = Path(f"user_templates/{user_id}")
    template_path = user_folder / text

    if not template_path.exists():
        await update.message.reply_text("Цей шаблон не знайдено.")
        return ConversationHandler.END

    context.user_data["selected_template_path"] = template_path
    await update.message.reply_text("Надішли фото, яке потрібно обробити ✂️")
    return SEND_IMAGE

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()

    temp_path = Path("user_data")
    temp_path.mkdir(exist_ok=True)
    input_path = temp_path / f"input_{update.effective_user.id}.jpg"
    await file.download_to_drive(str(input_path))

    # Завантажуємо шаблон
    with open(context.user_data["selected_template_path"], "r") as f:
        template_data = json.load(f)

    output_info = process_template(input_path, template_data)

    for info in output_info:
        path = info["path"]
        width = info["width"]
        height = info["height"]
        align = info["align"]

        caption = f"📐 {width}x{height}\n🧭 {align}"
        await update.message.reply_photo(photo=open(path, "rb"), caption=caption)

    return ConversationHandler.END
