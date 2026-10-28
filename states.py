from aiogram import  Router, F
from aiogram.types import Message
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
    await message.answer("🆔 Введите ID книги, которую хотите удалить:")
    await state.set_state(delete_books.get_book_id)


@router.message(delete_books.get_book_id)
async def get_book_id(message: Message, state: FSMContext):

    if is_cancel(message.text):
        await message.answer("↩️ Действие отменено.")
        await state.clear()
        return
    
    if not message.text.isdigit():
        await message.answer("⚠️ ID должен быть числом. Попробуйте ещё раз.")
        await state.clear()
        return

    if not await get_book(int(message.text)):
        await message.answer("🔎 Книга с таким ID не найдена.")
        await state.clear()
        return
    if await delete_book(int(message.text)):
        await message.answer("✅ Книга успешно удалена!")
        await state.clear()
    else:
        await message.answer("⚠️ Что-то пошло не так. Попробуйте позже.")
        await state.clear()







@router.message(F.text == "✏️ Изменить книгу")
@router.message(Command("edit"))
async def update_book_start(message: Message, state: FSMContext):
    user = await profile(message.from_user.id)
    if not user["is_admin"]:
        await message.answer("⛔ Эта команда доступна только администратору.")
        return
    
    await message.answer("✏️ Введите ID книги, которую хотите изменить:")
    await state.set_state(update_books.book_id)


@router.message(update_books.book_id)
async def update_book_id(message: Message, state: FSMContext):
    if is_cancel(message.text):
        await state.clear()
        await message.answer("↩️ Изменение отменено.")
        return
    
    if not message.text.isdigit():
        await message.answer("⚠️ ID должен быть числом. Попробуйте ещё раз.")
        return

    book = await get_book(int(message.text))

    if not book:
        await message.answer("🔎 Книга с таким ID не найдена. Попробуйте ещё раз.")
        return
    
    await state.update_data(book_id = int(message.text))
    await message.answer(f"📖 Текущее название: {book['title']}\nВведите новое название:")
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
    await message.answer("✍️ Введите ID автора:")
    await state.set_state(add_books.author_id)

@router.message(add_books.author_id)
async def get_author_id(message: Message, state: FSMContext):
    author_id = message.text
    if is_cancel(message.text):
        await state.clear()
        await message.answer("↩️ Добавление книги отменено.")
        return
    if not author_id.isdigit():
        await message.answer("⚠️ ID должен быть числом. Попробуйте ещё раз.")
    else:
        if not await get_author(int(author_id)):
            await message.answer("🔎 Автор с таким ID не найден. Попробуйте ещё раз.")
        else:
            await state.update_data(author = message.text)
            await message.answer("📂 Введите ID категории:")
            await state.set_state(add_books.category_id)


@router.message(add_books.category_id)
async def get_category_id(message: Message, state: FSMContext):
    category_id = message.text
    if is_cancel(message.text):
        await state.clear()
        await message.answer("↩️ Добавление книги отменено.")
        return
    if category_id.isdigit():
        await message.answer("⚠️ ID должен быть числом. Попробуйте ещё раз.")
    else:
        if not get_category(int(category_id)):
            await message.answer("🔎 Категория с таким ID не найдена. Попробуйте ещё раз.")
        else:
            await state.update_data(category = message.text)
            data = state.get_data()
            if await add_book(data["title"], data["caption"], data["author"], data["category"]):
                await message.answer("🎉 Книга успешно добавлена в библиотеку!")
                await state.clear()
                return
            await message.answer("⚠️ Не удалось добавить книгу. Попробуйте позже.")



@router.message(Login.password)
async def login_admin(message: Message, state: FSMContext):
    password = message.text
    if is_cancel(message.text):
        await state.clear()
        await message.answer("↩️ Вход отменён.")
        return

    if password != admin_ps:
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
    await message.answer("✍️ Введите ID автора:")
    await state.set_state(search_by_ar.get_id)


@router.message(search_by_ar.get_id)
async def get_aid(message: Message, state: FSMContext):
    author_id = message.text
    if is_cancel(message.text):
        await state.clear()
        await message.answer("↩️ Поиск отменён.")
        return
    if not author_id.isdigit():
        await message.answer("⚠️ ID должен быть числом.")
        await state.clear()
        return
    if not await get_author(author_id):
        await message.answer("🔎 Автор с таким ID не найден.")
        await state.clear()
        return
    
    books = await get_book_by_author(author_id)

    if not books:
        await message.answer("📭 У этого автора пока нет книг.")
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
    await message.answer(text)
    

@router.message(F.text == "📂 По категории")
@router.message(Command("cat"))
async def book_ct(message: Message, state: FSMContext):
    await message.answer("📂 Введите ID категории:")
    await state.set_state(search_by_ct.get_ct_id)


@router.message(search_by_ct.get_ct_id)
async def book_ct_id(message: Message, state: FSMContext):
    cat_id = message.text
    if is_cancel(message.text):
        await state.clear()
        await message.answer("↩️ Поиск отменён.")
        return
    if not cat_id.isdigit():
        await message.answer("⚠️ ID должен быть числом.")
        await state.clear()
        return

    if not await get_category(cat_id):
        await message.answer("🔎 Категория с таким ID не найдена.")
        await state.clear()
        return

    books = await get_book_by_ct(cat_id)

    if not books:
        await message.answer("📭 У этого автора пока нет книг.")
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
    await message.answer(text)
