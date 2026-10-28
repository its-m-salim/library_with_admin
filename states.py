from aiogram import  Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext 
from service import *
from connection import connection_db
from keyboards import *

router = Router()

class search_by_ar(StatesGroup):
    get_id = State()


class search_by_ct(StatesGroup):
    get_ct_id = State()


class delete_books(StatesGroup):
    get_book_id = State()


class Login(StatesGroup):
    password = State()



class add_books(StatesGroup):
    title = State()
    caption = State()
    author_id = State()
    category_id = State()


class update_books(StatesGroup):
    book_id = State()
    title = State()
    caption = State()


def is_cancel(type):
    return type == "cls"






@router.message(F.text == "🗑 Удалить книгу")
@router.message(Command("del"))
async def delete(message: Message, state: FSMContext):
    user = await profile(message.from_user.id)
    if not user["is_admin"]:
        await message.answer("⛔ Эта команда доступна только администратору.")
        return

    buttons = await get_books_btn()
    await message.answer("Выберите книгу, которую хотите удалить", reply_markup=buttons)
    await state.set_state(delete_books.get_book_id)


@router.callback_query(delete_books.get_book_id, F.data.startswith("book_"))
async def get_book_id(callback: CallbackQuery, state: FSMContext):

    # if is_cancel(message.text):
    #     await message.answer("↩️ Действие отменено.")
    #     await state.clear()
    #     return
    
    book_id = callback.data.split("_")[1]

    if await delete_book(book_id):
        await callback.message.answer("✅ Книга успешно удалена!")
        await state.clear()
    else:
        await callback.message.answer("⚠️ Что-то пошло не так. Попробуйте позже.")
        await state.clear()







@router.message(F.text == "✏️ Изменить книгу")
@router.message(Command("edit"))
async def update_book_start(message: Message, state: FSMContext):
    user = await profile(message.from_user.id)
    if not user["is_admin"]:
        await message.answer("⛔ Эта команда доступна только администратору.")
        return

    buttons = await get_books_btn()
    await message.answer("✏️ Выберите книгу, которую хотите изменить", reply_markup=buttons)
    await state.set_state(update_books.book_id)


@router.callback_query(update_books.book_id, F.data.startswith("book_"))
async def update_book_id(callback: CallbackQuery, state: FSMContext):

    # if is_cancel(message.text):
    #     await state.clear()
    #     await message.answer("↩️ Изменение отменено.")
    #     return
    
    book_id = callback.data.split("_")[1]

    book = await get_book(book_id)
    
    await state.update_data(book_id = book_id)
    await callback.message.answer(f"📖 Текущее название: {book['title']}\nВведите новое название:")
    await state.set_state(update_books.title)


@router.message(update_books.title)
async def update_book_title(message: Message, state: FSMContext):
    if is_cancel(message.text):
        await state.clear()
        await message.answer("↩️ Изменение отменено.")
        return
    
    await state.update_data(title=message.text)
    await message.answer("📝 Введите новое описание книги:")
    await state.set_state(update_books.caption)


@router.message(update_books.caption)
async def update_book_caption(message: Message, state: FSMContext):

    if is_cancel(message.text):
        await state.clear()
        await message.answer("↩️ Изменение отменено.")
        return
    
    data = await state.get_data()
    if await update_book(data["book_id"], data["title"], data["caption"]):
        await message.answer("✅ Информация о книге успешно обновлена!")
        await state.clear()

    else:
        await message.answer("⚠️ Не удалось обновить книгу. Попробуйте позже.")
        await state.clear()


@router.message(Command("login"))
async def login(message: Message, state: FSMContext):
    user = await profile(message.from_user.id)
    if user["is_admin"]:
        await message.answer("🛠 У вас уже есть права администратора!")
        return
    await message.answer("🔐 Введите пароль администратора для получения прав:")
    await state.set_state(Login.password)












@router.message(F.text == "➕ Добавить книгу")
@router.message(Command("add"))
async def add_book(message: Message, state: FSMContext):
    user = await profile(message.from_user.id)
    if not user["is_admin"]:
        await message.answer("⛔ Эта команда доступна только администратору.")
        return
    await message.answer("📖 Введите название книги:")
    await state.set_state(add_books.title)



@router.message(add_books.title)
async def get_title(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    await message.answer("📝 Введите описание книги:")
    await state.set_state(add_books.caption)


@router.message(add_books.caption)
async def get_caption(message: Message, state: FSMContext):
    if is_cancel(message.text):
        await state.clear()
        await message.answer("↩️ Добавление книги отменено.")
        return
    await state.update_data(caption = message.text)

    buttons = await get_author_btn()
    await message.answer("Выберите автора", reply_markup=buttons)
    await state.set_state(add_books.author_id)



@router.callback_query(add_books.author_id, F.data.startswith("author_"))
async def get_author_id(callback: CallbackQuery, state: FSMContext):
    author_id = callback.data.split("_")[1]
    await state.update_data(author = author_id)
    await callback.answer("Автор выбран")
    buttons = get_category_btn()
    await callback.message.answer("📂 Выберите категорию:", reply_markup=buttons)
    await state.set_state(add_books.category_id)




@router.callback_query(add_books.category_id, F.data.startswith("category_"))
async def get_category_id(callback: CallbackQuery, state: FSMContext):

    category_id = callback.data.split("_")[1]
    # if is_cancel(message.text):
    #     await state.clear()
    #     await message.answer("↩️ Добавление книги отменено.")
    #     return
    
    await state.update_data(category = category_id)
    await callback.answer("Категория выбран")

    data = state.get_data()
    if await add_book(data["title"], data["caption"], data["author"], data["category"]):
        await callback.message.answer("🎉 Книга успешно добавлена в библиотеку!")
        await state.clear()
        return
    await callback.message.answer("⚠️ Не удалось добавить книгу. Попробуйте позже.")



@router.message(Login.password)
async def login_admin(message: Message, state: FSMContext):
    user = await profile(message.from_user.id)
    password = message.text
    if is_cancel(message.text):
        await state.clear()
        await message.answer("↩️ Вход отменён.")
        return

    if password != user["password"]:
        await message.answer("❌ Неверный пароль администратора.")
        await state.clear()
        return

    if await become_admin(message.from_user.id):
        await message.answer("""
🎉Ещё один админ 🤨
Хотя ладно, добро пожаловать! 😏
🛠 Теперь тебе доступны инструменты управления библиотекой.
""", reply_markup = admin_kb)
        await state.clear()
        return
    else:
        await message.answer("⚠️ Не удалось выдать права администратора. Попробуйте позже.")
        await state.clear()












@router.message(F.text == "✍️ По автору")
@router.message(Command("author"))
async def get_book_by_author(message: Message, state: FSMContext):
    buttons = await get_author_btn()
    await message.answer("✍️ Выберите автора", reply_markup=buttons)
    await state.set_state(search_by_ar.get_id)


@router.callback_query(search_by_ar.get_id, F.data.startswith("author_"))
async def get_aid(callback: CallbackQuery, state: FSMContext):
    author_id = callback.data.split("_")[1]

    # if is_cancel(message.text):
    #     await state.clear()
    #     await message.answer("↩️ Поиск отменён.")
    #     return
    
    
    books = await get_book_by_authr(author_id)

    if not books:
        await callback.message.answer("📭 У этого автора пока нет книг.")
        await state.clear()
        return

    text = f"📚 Книги автора: {books[0]['author']}\n"

    for b in books:
        text += f"""
🆔 ID: {b["id"]}
📖 Название: {b["title"]}
📝 Описание: {b["caption"]}
📂 Категория: {b["category"]}
✍️ Автор: {b["author"]}
🕒 Добавлена: {b["created_at"]}
"""
    await callback.message.answer(text)
    

@router.message(F.text == "📂 По категории")
@router.message(Command("cat"))
async def book_ct(message: Message, state: FSMContext):

    buttons = await get_category_btn()
    await message.answer("📂 Выберите категорию", reply_markup=buttons)
    await state.set_state(search_by_ct.get_ct_id)


@router.callback_query(search_by_ct.get_ct_id, F.data.startswith("category_"))
async def get_aid(callback: CallbackQuery, state: FSMContext):
    cat_id = callback.data.split("_")[1]

    # if is_cancel(message.text):
    #     await state.clear()
    #     await message.answer("↩️ Поиск отменён.")
    #     return
    

    books = await get_book_by_ct(cat_id)

    if not books:
        await callback.message.answer("📭 У этого автора пока нет книг.")
        await state.clear()
        return
    
    text = "📂 Книги в выбранной категории:\\n"
    
    for b in books:
        text += f"""
🆔 ID: {b["id"]}
📖 Название: {b["title"]}
📝 Описание: {b["caption"]}
📂 Категория: {b["category"]}
✍️ Автор: {b["author"]}
🕒 Добавлена: {b["created_at"]}
"""
    await callback.message.answer(text)
