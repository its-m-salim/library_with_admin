from aiogram.types import KeyboardButton, ReplyKeyboardMarkup 
from aiogram import Bot, Dispatcher ,F
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


main_kb = ReplyKeyboardMarkup(
   keyboard=[
       [KeyboardButton(text="📚 Все книги"), KeyboardButton(text="🔎 Найти книгу")],
       [KeyboardButton(text="📂 По категории"),KeyboardButton(text="✍️ По автору")]
       ], resize_keyboard=True,
    
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[

        [KeyboardButton(text="🗑 Удалить книгу"), KeyboardButton(text="✏️ Изменить книгу")],
        [KeyboardButton(text="📚 Все книги"), KeyboardButton(text="➕ Добавить книгу")]
    ], resize_keyboard=True
)