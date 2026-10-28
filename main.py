from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext 
from keyboards import *
from states import router as state_router
from states import *
from service import *
from connection import *


import os
import asyncio


load_dotenv()

token_bot = os.getenv("BOT_TOKEN")

bot = Bot(token=token_bot)
dp = Dispatcher()



@dp.message(Command("start"))
async def start_bot(message: Message):
    usr = message.from_user
    user = await profile(message.from_user.id)
    if not user:
        await create_user(usr.username, usr.full_name, usr.id)
        await message.answer("Hello my friend ", reply_markup=main_kb)
        return
    if user["is_admin"]:
        await message.answer("Welcome back, admin!", reply_markup=admin_kb)
        return
    
    await message.answer(f"Welcome back, {usr.full_name}")


@dp.message(F.text == "All Books")
@dp.message(Command("books"))
async def all_books(message: Message):
    books = await get_all_books()

    if not books:
        await message.answer("No books yet")
        return

    text = "Вот все доступные униги:\n"

    for book in books:
        text += f"""
Имя: {book["title"]}
Описание: {book["caption"]}
Категория: {book["category"]}
Автор: {book["author"]}
Добавлено: {book["created_at"]}

"""
    await message.answer(text)




@dp.message(Command("categories"))
async def all_categories(message: Message):
    categories = await get_categories()

    if not categories:
        await message.answer("It seems there is no categories yet")
        return

    text = "Here is all the categories\n"
    for c in categories:
        text += f"""
ID: {c["id"]}
Name: {c["name"]}
"""
    await message.answer(text)


@dp.message(Command("authors"))
async def all_authosr(message: Message):
    authors = await get_categories()

    if not authors:
        await message.answer("It seems there is no authors yet")
        return

    text = "Here is all the authors\n"
    for a in authors:
        text += f"""
ID: {a["id"]}
Full Name: {a["full_name"]}
"""
    await message.answer(text)







async def main():
    print("Bot started")
    dp.include_router(state_router)
    await create_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    