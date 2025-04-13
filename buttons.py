from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_stage_buttons(stage: int):
    if stage == 2:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Хочу", callback_data="yes")],
            [InlineKeyboardButton("Да нахер надо", callback_data="no")]
        ])
    elif stage == 3:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Позвать проныру", callback_data="call_pronyra")]
        ])
    elif stage == 4:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Будем", callback_data="drink")],
            [InlineKeyboardButton("Я без тебя справлюсь", callback_data="nope")],
            [InlineKeyboardButton("Сгинь алкаш", callback_data="bye")]
        ])
    elif stage == 6:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Выпить", callback_data="drink")],
            [InlineKeyboardButton("Хорош", callback_data="stop")]
        ])
    elif stage == 7:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("Позвать проныру", callback_data="call_pronyra")]
        ])
    return None
