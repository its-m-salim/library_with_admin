from aiogram.types import KeyboardButton, ReplyKeyboardMarkup 
from aiogram import Bot, Dispatcher ,F
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


main_kb = ReplyKeyboardMarkup(
   keyboard=[
       [KeyboardButton(text="All Books"), KeyboardButton(text="Get book")],
       [KeyboardButton(text="Search book by category"),KeyboardButton(text="serach book by author")]
       ], resize_keyboard=True,
    
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[

        [KeyboardButton(text="delete book"), KeyboardButton(text="update book")],
        [KeyboardButton(text="All Books"), KeyboardButton(text="Add book")]
    ], resize_keyboard=True
)