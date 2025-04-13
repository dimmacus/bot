import random
import aiohttp

phrases = {
    "greetings": [
        "Йо-хо, {name}, да ты красавчик!",
        "Привет, {name}! Пахнет тайной...",
        "Здорово, {name}. Ты вовремя!",
        "{name}, сегодня твой день!",
        "О, это же {name}! Ну держись."
    ],
    "return_pronyra": [
        "Ну ты быстро передумал!",
        "Вот это поворот!",
        "Я знал, что ты вернёшься!",
        "Проныру не так просто потерять."
    ]
}

def get_random_phrase(key):
    return random.choice(phrases.get(key, ["..."]))

async def get_holiday_today():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://date.nager.at/api/v3/PublicHolidays/2025/RU") as response:
                if response.status == 200:
                    holidays = await response.json()
                    from datetime import date
                    today = date.today().isoformat()
                    for holiday in holidays:
                        if holiday["date"] == today:
                            return holiday["localName"]
    except:
        pass
    return "Просто чудесный день!"

async def get_reason_to_drink():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.affirmations.dev/") as response:
                if response.status == 200:
                    data = await response.json()
                    return data["affirmation"]
    except:
        pass
    return "Да просто потому что можем!"

def flip_coin():
    return "heads" if random.random() < 0.95 else "tails"

def get_toast():
    toasts = [
        "За тех, кто с нами!",
        "За любовь, код и баги!",
        "Чтобы всё работало с первого раза!",
        "За проныру, мать его!",
        "Чтобы deploy был без боли!"
    ]
    return random.choice(toasts)
