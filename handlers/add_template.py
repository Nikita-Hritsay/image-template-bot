import os
from telegram import Update
from telegram.ext import ContextTypes
from pathlib import Path

TEMPLATE_IMAGE, TEMPLATE_COUNT, TEMPLATE_FORMAT = range(3)

# Тимчасове збереження станів користувача
user_states = {}

async def start_add_template(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Надішли перше фото шаблону")
    return TEMPLATE_IMAGE


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    photo = update.message.photo[-1]
    file = await photo.get_file()

    user_folder = Path(f"user_templates/{user_id}")
    user_folder.mkdir(parents=True, exist_ok=True)

    img_path = user_folder / f"template_first.jpg"
    await file.download_to_drive(str(img_path))

    user_states[user_id] = {
        "img_path": str(img_path),
        "formats": []
    }

    await update.message.reply_text("Скільки буде варіантів повернення фото?")
    return TEMPLATE_COUNT

async def handle_template_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        count = int(update.message.text)
    except ValueError:
        await update.message.reply_text("Будь ласка, введи число (кількість шаблонів)")
        return TEMPLATE_COUNT

    user_states[user_id]["expected_count"] = count
    user_states[user_id]["current_index"] = 0

    await update.message.reply_text(f"Введи шаблон у форматі: ширинаxвисота align (наприклад: 50x100 top-center)")
    return TEMPLATE_FORMAT

async def handle_template_format(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    state = user_states[user_id]
    print(text)
    try:
        size_part, align = text.split()
        width, height = map(int, size_part.lower().split('x'))
        state["formats"].append({
            "width": width,
            "height": height,
            "align": align
        })
    except:
        await update.message.reply_text("Формат неправильний. Спробуй ще раз: 50x100 top-center")
        return TEMPLATE_FORMAT

    state["current_index"] += 1

    if state["current_index"] < state["expected_count"]:
        await update.message.reply_text(f"Введи шаблон {state['current_index'] + 1} у форматі: 50x100 center")
        return TEMPLATE_FORMAT
    else:
        # Зберігаємо шаблон у файл
        import json
        template_path = Path(f"user_templates/{user_id}/template_{len(os.listdir(f'user_templates/{user_id}'))}.json")
        with open(template_path, "w") as f:
            json.dump(state, f, indent=2)

        await update.message.reply_text("Шаблон успішно збережено ✅")
        return ConversationHandler.END
