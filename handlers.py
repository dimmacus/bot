from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from buttons import get_stage_buttons
from utils import get_random_phrase, get_holiday_today, get_reason_to_drink, flip_coin, get_toast

users = {}

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Как тебя зовут?")
    users[update.effective_chat.id] = {"stage": 1}

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data = users.get(chat_id, {})

    if user_data.get("stage") == 1:
        name = update.message.text.strip()
        users[chat_id]["name"] = name
        users[chat_id]["stage"] = 2

        greeting = get_random_phrase("greetings").format(name=name)
        await update.message.reply_text(greeting)
        await update.message.reply_text("Я помощник Джона Сноу. Я знаю ответ на главный вопрос жизни...", reply_markup=get_stage_buttons(2))

    elif user_data.get("stage") == 6:
        if update.message.text.lower() == "выпить":
            toast = get_toast()
            await update.message.reply_text(toast)
        elif update.message.text.lower() == "хорош":
            await update.message.reply_text("Ну всё, хватит. Проныра ушёл спать.")
            users[chat_id]["stage"] = 999

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    user_data = users.get(chat_id, {})
    name = user_data.get("name", "друг")

    stage = user_data.get("stage", 0)
    data = query.data

    if stage == 2:
        if data == "yes":
            users[chat_id]["stage"] = 4
            await query.message.reply_text("Ты знаешь, какой сегодня день?")
            holiday = await get_holiday_today()
            await query.message.reply_text(f"А это: {holiday}")
            await query.message.reply_text("Будем отмечать?", reply_markup=get_stage_buttons(4))
        elif data == "no":
            await query.message.reply_text("Дело конечно твоё... *Проныра уходит в туман...*", reply_markup=get_stage_buttons(3))
            users[chat_id]["stage"] = 3

    elif stage == 3:
        if data == "call_pronyra":
            phrase = get_random_phrase("return_pronyra")
            await query.message.reply_text(phrase)
            await query.message.reply_text("Ну что, вернулся за тайной?", reply_markup=get_stage_buttons(2))
            users[chat_id]["stage"] = 2

    elif stage == 4:
        if data == "drink":
            users[chat_id]["stage"] = 5
            await query.message.reply_text("Извечный вопрос: пить или не пить... Конечно пить!")
            reason = await get_reason_to_drink()
            await query.message.reply_text(f"Причина: {reason}")
            result = flip_coin()
            if result == "heads":
                await query.message.reply_text("Выпал орёл — Будем, ептыть!", reply_markup=get_stage_buttons(6))
                users[chat_id]["stage"] = 6
            else:
                await query.message.reply_text("Выпала решка... Проныра сбежал 🏃‍♂️", reply_markup=get_stage_buttons(7))
                users[chat_id]["stage"] = 7
        else:
            await query.message.reply_text("Ну... твой выбор. Я пошёл бухать один.")

    elif stage == 6:
        # handled in message_handler
        pass

    elif stage == 7:
        if data == "call_pronyra":
            phrase = get_random_phrase("return_pronyra")
            await query.message.reply_text(phrase)
            await query.message.reply_text("Ну что, вернулся за тайной?", reply_markup=get_stage_buttons(2))
            users[chat_id]["stage"] = 2
