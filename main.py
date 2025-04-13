import asyncio
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from dotenv import load_dotenv
import os

from handlers import start_handler, button_handler, message_handler

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")

    if not TOKEN:
        raise ValueError("Переменная окружения BOT_TOKEN не установлена!")

    app = Application.builder().token(TOKEN).build()

    # Хендлеры
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    logger.info("✅ Бот запущен...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
