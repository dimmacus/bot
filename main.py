import logging
import asyncio
import random
import datetime
import httpx
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, ContextTypes,
    MessageHandler, filters, CallbackQueryHandler
)

# Логгирование
logging.basicConfig(level=logging.INFO)

# Хранилище пользователей
user_data = {}

# Рандомные приветствия и байки
greetings = [
    "Ну здравствуй, {name}, давненько не виделись!",
    "О, это же ты, {name}! Как жизнь?",
    "Я уж думал, ты не появишься, {name}!",
    "Привет тебе, славный воин {name}!"
]

snarky_responses = [
    "Дело конечно твое, ходи и мучайся, если надумаешь — я в таверне.",
    "Ну, тоже вариант. Я тут, покуриваю, как чё — зови.",
    "Мудро... или нет? В общем, решай сам."
]

pronyra_returns = [
    "Не так долго мне пришлось скучать-то...",
    "Быстро же ты вернулся, {name}...",
    "Я знал, что ты не устоишь, {name}!"
]

holiday_responses = [
    "Ну что, будем отмечать?",
    "Праздник ведь! {name}, не зря же он сегодня.",
    "Устроим пир в честь {holiday}, а?",
]

drink_excuses = [
    "Учёные доказали, что 50 грамм поднимают иммунитет!",
    "Пить или не пить... Конечно пить!",
    "Без рюмки ты не узнаешь, что будет дальше!"
]

drunk_jokes = [
    "— Пей до дна! — А если не нальёшь?..",
    "Я не пьян, я просто разговариваю с мебелью.",
    "Выпили немного… но часто.",
    "Главное — не закусывать проблемами!"
]

# Получение праздника из API
async def get_today_holiday():
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get("https://date.nager.at/api/v3/PublicHolidays/2025/US")
            holidays = res.json()
            today = datetime.date.today()
            for h in holidays:
                if h["date"] == today.isoformat():
                    return h["localName"]
            return "какой-то там праздник"
    except:
        return "день весёлого желудка"

# Получение тоста
async def get_toast():
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get("https://api.quotable.io/random?tags=funny")
            return res.json().get("content", "За дружбу и бутылку!")
    except:
        return "Пусть стаканы звенят, а мысли отдыхают!"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Рад приветствовать тебя, мой друг. Как тебя зовут?")
    return

# Получение имени
async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    name = update.message.text.strip()
    user_data[user_id] = {"name": name, "joke_task": None}
    greet = random.choice(greetings).format(name=name)
    await update.message.reply_text(greet)
    await asyncio.sleep(1)
    await update.message.reply_text("Я — проныра, помощник Джона Сноу. Я знаю ответ на главный вопрос бытия.")
    await asyncio.sleep(1)
    buttons = [
        [
            InlineKeyboardButton("Хочу", callback_data="wanna_know"),
            InlineKeyboardButton("Да нахер надо", callback_data="no_way")
        ]
    ]
    await update.message.reply_text("Хочешь узнать?", reply_markup=InlineKeyboardMarkup(buttons))

# Кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    name = user_data.get(user_id, {}).get("name", "друг")

    if query.data == "no_way":
        text = random.choice(snarky_responses)
        await query.edit_message_text(text)
        await asyncio.sleep(1)
        await query.message.reply_text(
            "Проныра скрылся за дверью таверны. Остался лишь шум посетителей.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Позвать проныру", callback_data="call_back")]])
        )

    elif query.data == "call_back":
        text = random.choice(pronyra_returns).format(name=name)
        await query.message.reply_text(text)
        await asyncio.sleep(1)
        buttons = [
            [
                InlineKeyboardButton("Да, давай уже, вещай", callback_data="wanna_know"),
                InlineKeyboardButton("Всё же иди нахер", callback_data="no_way")
            ]
        ]
        await query.message.reply_text("Готов узнать мой секрет?", reply_markup=InlineKeyboardMarkup(buttons))

    elif query.data == "wanna_know":
        await query.edit_message_text("Ты знаешь, какой сегодня день, " + name + "? Напиши.")
        context.user_data["awaiting_day_response"] = True

    elif query.data == "celebrate":
        await query.edit_message_text("Пить или не пить... Конечно пить!")
        await asyncio.sleep(1)
        excuse = random.choice(drink_excuses)
        await query.message.reply_text(excuse)
        await asyncio.sleep(1)
        result = "Орел" if random.random() < 0.95 else "Решка"
        if result == "Орел":
            await query.message.reply_text(f"{name}, орел! Будем пить!")
            buttons = [
                [InlineKeyboardButton("Конечно", callback_data="drink_now"),
                 InlineKeyboardButton("Нет ещё", callback_data="not_yet")]
            ]
            await query.message.reply_text("Ты уже налил?", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await query.message.reply_text(
                f"О нет, {name}, сегодня не твой день. Гадалки говорили, кто-то облажается..."
            )
            await query.message.reply_text(
                "Проныра сбежал. Позвать снова?",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Позвать проныру", callback_data="call_back")]])
            )

    elif query.data == "drink_now":
        await query.message.reply_text("Красава! Ну хлопнем...")
        buttons = [
            [InlineKeyboardButton("Выпить", callback_data="drink_more"),
             InlineKeyboardButton("Хорош", callback_data="stop_drinking")]
        ]
        await query.message.reply_text("За тебя, за меня, за всё хорошее!", reply_markup=InlineKeyboardMarkup(buttons))

    elif query.data == "not_yet":
        await query.message.reply_text("Тогда в магазин и тащи пойло!")
        await send_drunk_jokes(context, user_id)

    elif query.data == "drink_more":
        toast = await get_toast()
        await query.message.reply_text(toast)

    elif query.data == "stop_drinking":
        await query.message.reply_text("Ладно... хм... ты сегодня в завязке.")

# Обработка сообщений
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if context.user_data.get("awaiting_day_response"):
        context.user_data["awaiting_day_response"] = False
        holiday = await get_today_holiday()
        name = user_data.get(user_id, {}).get("name", "друг")
        await update.message.reply_text(f"Прости, не понял, но не важно. Сегодня — {holiday}!")
        buttons = [
            [InlineKeyboardButton("Будем", callback_data="celebrate"),
             InlineKeyboardButton("Я без тебя справлюсь", callback_data="no_way"),
             InlineKeyboardButton("Сгинь алкаш", callback_data="no_way")]
        ]
        await update.message.reply_text(random.choice(holiday_responses).format(name=name, holiday=holiday), reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await handle_name(update, context)

# Шутки каждые 5 минут
async def send_drunk_jokes(context: ContextTypes.DEFAULT_TYPE, user_id):
    async def job():
        while True:
            await context.bot.send_message(chat_id=user_id, text=random.choice(drunk_jokes))
            await asyncio.sleep(300)
    task = asyncio.create_task(job())
    user_data[user_id]["joke_task"] = task

# Запуск
async def main():
    app = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("✅ Бот запущен и ждёт...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
