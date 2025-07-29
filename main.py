import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, filters
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from handlers.menu import start
from handlers.add_template import (
    start_add_template, handle_photo, handle_template_count, handle_template_format,
    TEMPLATE_IMAGE, TEMPLATE_COUNT, TEMPLATE_FORMAT
)
from handlers.templates import templates_menu, choose_template, handle_image, CHOOSE_TEMPLATE, SEND_IMAGE


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

# Main menu
app.add_handler(CommandHandler("start", start))

# Templates Add Handlers
add_template_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & filters.Regex("^Add Template \\+$"), start_add_template)],
    states={
        TEMPLATE_IMAGE: [MessageHandler(filters.PHOTO, handle_photo)],
        TEMPLATE_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_template_count)],
        TEMPLATE_FORMAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_template_format)],
    },
    fallbacks=[],
)

# Templates selectors Handlers
template_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & filters.Regex("^Templates$"), templates_menu)],
    states={
        CHOOSE_TEMPLATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_template)],
        SEND_IMAGE: [MessageHandler(filters.PHOTO, handle_image)],
    },
    fallbacks=[],
)

app.add_handler(template_conv)

app.add_handler(add_template_conv)

print("🤖 Bot is running...")
app.run_polling()
