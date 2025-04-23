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

# Загрузка токена из .env
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

# Стартовая кнопка "Начнём?"
async def show_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Начнём?", callback_data="start_game")],
    ]
    if update.message:
        await update.message.reply_text(
            "Готовы начать игру?", reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.callback_query.message.reply_text(
            "Готовы начать игру?", reply_markup=InlineKeyboardMarkup(keyboard)
        )

# Приветствие и правила
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message

    keyboard = [
        [InlineKeyboardButton("Принято", callback_data="rules_accepted")],
    ]
    await message.reply_text(
        "Привет! Это 'Весёлый Дозатор'.\n"
        "Здесь кидаем два кубика и выполняем весёлые задания с выпивкой.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# Показ правил
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Начать играть", callback_data="start_round")],
    ]
    rules_text = (
        "Правила игры:\n"
        "- В компании минимум 3 человека (девушки и парни).\n"
        "- Каждый по очереди нажимает 'Следующий бросок'.\n"
        "- Бросается два кубика: один решает КТО пьёт, второй — КАК пьёт.\n"
        "- Выполнил — передай ход следующему!"
    )
    await query.edit_message_text(rules_text, reply_markup=InlineKeyboardMarkup(keyboard))

# Первый бросок
async def begin_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Бросаем кубики!")
    await roll_dice(update, context)

# Бросаем два кубика
async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dice1_result = random.choice(dice1)
    dice2_result = random.choice(dice2)

    keyboard = [
        [InlineKeyboardButton("Следующий бросок", callback_data="next_roll")],
        [InlineKeyboardButton("Закончить игру", callback_data="end_game")],
    ]

    await update.callback_query.message.reply_text(
        f"Кубик 1: *{dice1_result}*", parse_mode='Markdown'
    )

    await context.application.create_task(
        delayed_second_dice(update, dice2_result, keyboard)
    )

# Второй кубик с задержкой
async def delayed_second_dice(update: Update, result: str, keyboard):
    await asyncio.sleep(5)
    await update.callback_query.message.reply_text(
        f"Кубик 2: *{result}*",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Следующий бросок
async def next_roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await roll_dice(update, context)

# Завершение игры
async def end_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_start_button(update, context)

# Основной запуск
def main():
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", show_start_button))
    app.add_handler(CallbackQueryHandler(start, pattern="start_game"))
    app.add_handler(CallbackQueryHandler(rules, pattern="rules_accepted"))
    app.add_handler(CallbackQueryHandler(begin_game, pattern="start_round"))
    app.add_handler(CallbackQueryHandler(next_roll, pattern="next_roll"))
    app.add_handler(CallbackQueryHandler(end_game, pattern="end_game"))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()