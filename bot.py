"""Telegram-бот для генерации рецептов."""

import logging
import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from formatters import format_markdown
from llm_client import RecipeLLM, RecipeLLMError


load_dotenv()  # загрузка переменных окружения из .env


logging.basicConfig(level=logging.INFO)  # настройка логирования


INGREDIENTS, MOOD = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветствие и краткая инструкция."""

    await update.message.reply_text(
        "Привет! Используйте /recipe, чтобы получить рецепт "
        "по ингредиентам и настроению."
    )


async def recipe_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Первый шаг диалога: запрос ингредиентов."""

    await update.message.reply_text("Введите ингредиенты через запятую:")
    return INGREDIENTS


async def receive_ingredients(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Сохраняет ингредиенты и спрашивает настроение."""

    context.user_data["ingredients"] = update.message.text
    keyboard = [["simple", "fancy"]]
    await update.message.reply_text(
        "Выберите настроение:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return MOOD


async def receive_mood(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Вызывает LLM и отправляет результат пользователю."""

    ingredients = context.user_data.get("ingredients", "")
    mood = update.message.text.strip()

    try:
        recipe = RecipeLLM.generate(ingredients, mood)
        message = format_markdown(recipe)
        await update.message.reply_text(
            message, parse_mode="Markdown", reply_markup=ReplyKeyboardRemove()
        )
    except RecipeLLMError as exc:
        await update.message.reply_text(
            f"Не удалось получить рецепт: {exc}", reply_markup=ReplyKeyboardRemove()
        )

    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Позволяет прервать диалог."""

    context.user_data.clear()
    await update.message.reply_text(
        "Диалог прерван.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main() -> None:
    """Запускает приложение и регистрирует обработчики."""

    token = os.environ["TELEGRAM_TOKEN"]
    application = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("recipe", recipe_start)],
        states={
            INGREDIENTS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_ingredients)
            ],
            MOOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_mood)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
