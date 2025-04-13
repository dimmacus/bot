from dotenv import load_dotenv
import os
# Загружаем переменные из .env файла
load_dotenv()
import logging
import asyncio
import random
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Список забавных фраз для бота
JOKES = [
    "Когда-то я был просто строкой кода, а теперь у меня даже есть чувства... или почти!",
    "Говорят, я слишком умный. Но это всего лишь байт моего очарования!",
    "Пока вы спите, я обрабатываю пакеты данных. Романтика, правда?",
    "Был бы я человеком — пошёл бы в стендап!",
    "Программисты меня создали. Теперь я их лучший друг и ночной кошмар одновременно."
]

# Список комплиментов
COMPLIMENTS = [
    "Ты сегодня особенно шикарен! 😎",
    "Такой харизмой можно сервера заряжать!",
    "С тобой и баги не страшны!",
    "Кажется, твоя креативность зашкаливает!",
    "Ты как идеально написанный код — радуешь глаз! 💻"
]

# Простая API-проверка для внешнего вызова
async def get_joke_from_api():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://v2.jokeapi.dev/joke/Any?type=single")
            data = response.json()
            return data.get("joke", "Упс, анекдоты закончились! 😅")
    except Exception as e:
        logger.error(f"Ошибка при получении шутки: {e}")
        return random.choice(JOKES)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я твой весёлый бот-собеседник 😄\nНапиши мне что-нибудь!"
    )

# Команда /joke
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    joke = await get_joke_from_api()
    await update.message.reply_text(joke)

# Команда /compliment
async def compliment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    compliment = random.choice(COMPLIMENTS)
    await update.message.reply_text(compliment)

# Обработка всех сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.lower()

    if "анекдот" in text or "шутка" in text:
        await joke(update, context)
    elif "комплимент" in text:
        await compliment(update, context)
    else:
        reply = random.choice([
            "Ого, интересно! Расскажи ещё!",
            "Вот это да! 😲",
            "Ты умеешь удивлять!",
            "Хочешь анекдот или комплимент? Напиши! 😉",
            random.choice(COMPLIMENTS)
        ])
        await update.message.reply_text(reply)

# Главная функция запуска бота
async def main() -> None:
    from os import getenv
    TOKEN = getenv("BOT_TOKEN")

    if not TOKEN:
        raise ValueError("Переменная окружения BOT_TOKEN не установлена!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("compliment", compliment))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Бот запущен и ждёт...")
    await app.run_polling()

if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
