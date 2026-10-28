from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from service import*











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



async def get_author_btn():
    data = await get_authors()
    keyboards = []

    for author in data:
        keyboards.append([InlineKeyboardButton(text=author['full_name'], callback_data=f"author_{author["id"]}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard



async def get_category_btn():
    data = await get_categories()
    keyboards = []

    for ct in data:
        keyboards.append([InlineKeyboardButton(text=ct['name'], callback_data=f"category_{ct["id"]}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard




async def get_books_btn():
    data = await get_all_books()
    keyboards = []

    for index, book in enumerate(data, start=1):
        keyboards.append([InlineKeyboardButton(text=f"{index}.{book['title']}", callback_data=f"book_{book["id"]}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard