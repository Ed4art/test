import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from llm_client import generate_recipe

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Send me the ingredients you have, and I'll suggest a recipe."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ingredients = update.message.text
    recipe = generate_recipe(ingredients)
    await update.message.reply_text(recipe)


def main() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    application.run_polling()


if __name__ == "__main__":
    main()
