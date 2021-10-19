import asyncio
import logging
import os
import requests


from pathlib import Path
from aiogram import Bot, Dispatcher, executor, types

from settings.config import API_TOKEN

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA = os.path.join(BASE_DIR, "TGBot/media/")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

url = "https://webnewbie.pythonanywhere.com/"
gl_products = {}


def get_products(is_exist=False):
    if is_exist:
        res = requests.get(f"{url}getactive/").json().get("data")
    else:
        res = requests.get(f"{url}getinactive/").json().get("data")
    products = dict()
    for i in res:
        products[i["name"]] = i["key"]
    return products


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("Привет!")


@dp.message_handler(commands=["exist", "notExist"])
async def exist_products(message: types.Message):
    if message.text == "/exist":
        products = get_products(True)
    else:
        products = get_products(False)
    text = str()
    for key, item in products.items():
        text = f"{text} {item} {key}\n"
    msg = await message.reply(text)
    await asyncio.sleep(60)
    await msg.delete()
    await message.delete()

@dp.message_handler()
async def check_message(message: types.Message):
    global gl_products
    gl_products = get_products()
    for key, value in gl_products.items():
        if value.lower() in str(message.text).lower():
            await message.answer(f"❌ {key} - нет в наличии ❌")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
