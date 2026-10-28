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
        await message.answer("👋 Добро пожаловать!\n\n📚 Здесь ты можешь находить книги и открывать для себя новые истории.", reply_markup=main_kb)
        return
    if user["is_admin"]:
        await message.answer("🛠 С возвращением, администратор!\n\nВыберите действие в меню ниже.", reply_markup=admin_kb)
        return
    
    await message.answer(f"✨ С возвращением, {usr.full_name}!\n\nЧто будем читать сегодня?")


@dp.message(F.text == "📚 Все книги")
@dp.message(Command("books"))
async def all_books(message: Message):
    books = await get_all_books()

    if not books:
        await message.answer("📭 В библиотеке пока нет книг. Загляните позже!")
        return

    text = "📚 **Каталог библиотеки**\n\nВот доступные книги:\n"

    for book in books:
        text += f"""
📖 Название: {book["title"]}
📝 Описание: {book["caption"]}
📂 Категория: {book["category"]}
✍️ Автор: {book["author"]}
🕒 Добавлена: {book["created_at"]}

"""
    await message.answer(text)




@dp.message(Command("cats"))
async def all_categories(message: Message):
    categories = await get_categories()

    if not categories:
        await message.answer("📭 Категорий пока нет.")
        return

    text = "📂 **Категории библиотеки**\n"
    for c in categories:
        text += f"""
🆔 ID: {c["id"]}
📌 Название: {c["name"]}
"""
    await message.answer(text)


@dp.message(Command("authors"))
async def all_authosr(message: Message):
    authors = await get_authors()

    if not authors:
        await message.answer("📭 Авторы пока не добавлены.")
        return

    text = "✍️ **Авторы библиотеки**\n"
    for a in authors:
        text += f"""
🆔 ID: {a["id"]}
👤 Имя автора: {a["full_name"]}
"""
    await message.answer(text)



@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("""
📚 ПОМОЩЬ ПО БИБЛИОТЕКЕ

Добро пожаловать! ✨
Здесь ты можешь искать книги и знакомиться с каталогом библиотеки.

📖 Команды читателя

/start — главное меню
/books — посмотреть все книги
/cats — список категорий
/authors — список авторов
/cat — найти книги по категории
/author — найти книги по автору
/help — показать это меню

🛠 Команды администратора

/login — получить права администратора
/add — добавить книгу
/edit — изменить книгу
/del — удалить книгу

💡 Полезно знать

• Следуй подсказкам бота после запуска команды.
• Если хочешь отменить действие, отправь cls.
• Команды администратора доступны только после входа.

🌟 Приятного чтения!
""", parse_mode="HTML")






async def main():
    print("Бот запущен")
    dp.include_router(state_router)
    await create_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    