import random
import asyncio
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Загрузка токена из файла token.env
load_dotenv(dotenv_path="token.env")
token = os.getenv("BOT_TOKEN")

# Кубики
dice1 = [
    "Пьют парни",
    "Пьют все",
    "Пьют девчонки",
    "Пей до дна!",
    "Пьёт тот, кто слева",
    "Пьёт тот, кто справа",
]

dice2 = [
    "Пританцовывая",
    "Пой и пей",
    "Отожмись 3 раза и выпей",
    "С закрытыми глазами",
    "Стоя на одной ноге",
    "Без помощи рук",
]

# Приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Принято", callback_data="rules_accepted")],
    ]
    await update.message.reply_text(
        "Привет! Это 'Весёлый Дозатор'.\n"
        "Здесь кидаем два кубика и выполняем весёлые задания с выпивкой.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# Правила
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Начать играть", callback_data="start_game")],
    ]
    rules_text = (
        "Правила игры:\n"
        "- В компании минимум 3 человека (девушки и парни).\n"
        "- Каждый по очереди нажимает 'Следующий бросок'.\n"
        "- Бросается два кубика: один решает КТО пьёт, второй — КАК пьёт.\n"
        "- Выполнил — передай ход следующему!"
    )
    await query.edit_message_text(rules_text, reply_markup=InlineKeyboardMarkup(keyboard))

# Начало игры
async def begin_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Бросаем кубики!")

    await roll_dice(update, context)

# Кидание кубиков
async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dice1_result = random.choice(dice1)
    dice2_result = random.choice(dice2)

    keyboard = [
        [InlineKeyboardButton("Следующий бросок", callback_data="next_roll")],
        [InlineKeyboardButton("Закончить игру", callback_data="end_game")],
    ]

    # Показываем первый кубик
    await update.callback_query.message.reply_text(f"Кубик 1: *{dice1_result}*", parse_mode='Markdown')

    # Пауза 5 секунд, затем второй кубик
    await context.application.create_task(delayed_second_dice(update, dice2_result, keyboard))

# Задержка перед вторым кубиком
async def delayed_second_dice(update: Update, result: str, keyboard):
    await asyncio.sleep(5)
    await update.callback_query.message.reply_text(
        f"Кубик 2: *{result}*", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Следующий бросок
async def next_roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await roll_dice(update, context)

# Завершить игру
async def end_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(update, context)

# Основной запуск
def main():
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(rules, pattern="rules_accepted"))
    app.add_handler(CallbackQueryHandler(begin_game, pattern="start_game"))
    app.add_handler(CallbackQueryHandler(next_roll, pattern="next_roll"))
    app.add_handler(CallbackQueryHandler(end_game, pattern="end_game"))

    print("Бот запущен...")
    app.run_polling()

if name == "main":
    main()