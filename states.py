from aiogram import  Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext 
from service import *
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


def is_cancel(type):
    return type == "cls"






@router.message(F.text == "delete book")
@router.message(Command("delete_book"))
async def delete(message: Message, state: FSMContext):
    user = await profile(message.from_user.id)
    if not user["is_admin"]:
        await message.answer("Это команад только для админа")
        return
    await message.answer("Enter book id")
    await state.set_state(delete_books.get_book_id)


@router.message(delete_books.get_book_id)
async def get_book_id(message: Message, state: FSMContext):

    if is_cancel(message.text):
        await message.answer("cancel! ")
        await state.clear()
        return
    
    if not message.text.isdigit():
        await message.answer("id must be a number!")
        await state.clear()
        return

    if not await get_book(int(message.text)):
        await message.answer("book does not exist")
        await state.clear()
        return
    if await delete_book(int(message.text)):
        await message.answer("book deleted")
        await state.clear()
    else:
        await message.answer("ooopps.. something went wrong")
        await state.clear()







@router.message(Command("login"))
async def login(message: Message, state: FSMContext):
    user = await profile(message.from_user.id)
    if user["is_admin"]:
        await message.answer("You are already admin!")
        return
    await message.answer("Ener admin password to access admin rights ")
    await state.set_state(Login.password)












@router.message(F.text == "Add book")
@router.message(Command("add_book"))
async def add_book(message: Message, state: FSMContext):
    user = await profile(message.from_user.id)
    if not user["is_admin"]:
        await message.answer("Это команад только для админа")
        return
    await message.answer("Enter title: ")
    await state.set_state(add_books.title)



@router.message(add_books.title)
async def get_title(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    await message.answer("Enter caption")
    await state.set_state(add_books.caption)


@router.message(add_books.caption)
async def get_caption(message: Message, state: FSMContext):
    if is_cancel(message.text):
        await state.clear()
        await message.answer("Добавление книги было отменено!")
        return
    await state.update_data(caption = message.text)
    await message.answer("Enter author id")
    await state.set_state(add_books.author_id)

@router.message(add_books.author_id)
async def get_author_id(message: Message, state: FSMContext):
    author_id = message.text
    if is_cancel(message.text):
        await state.clear()
        await message.answer("Добавление книги было отменено!")
        return
    if not author_id.isdigit():
        await message.answer("Id must be a number, try again")
    else:
        if not await get_author(int(author_id)):
            await message.answer("author does not exists, try again")
        else:
            await state.update_data(author = message.text)
            await message.answer("Enter category id")
            await state.set_state(add_books.category_id)


@router.message(add_books.category_id)
async def get_category_id(message: Message, state: FSMContext):
    category_id = message.text
    if is_cancel(message.text):
        await state.clear()
        await message.answer("Добавление книги было отменено!")
        return
    if category_id.isdigit():
        await message.answer("Id must be a number, try again")
    else:
        if not get_category(int(category_id)):
            await message.answer("category does not exists, try again")
        else:
            await state.update_data(category = message.text)
            data = state.get_data()
            if await add_book(data["title"], data["caption"], data["author"], data["category"]):
                await message.answer("книга успешно добавлено!")
                await state.clear()
                return
            await message.answer("oops.. something went wrong. please try later")



@router.message(Login.password)
async def login_admin(message: Message, state: FSMContext):
    password = message.text
    if is_cancel(message.text):
        await state.clear()
        await message.answer("логин был отменен!")
        return

    if password != admin_ps:
        await message.answer("""
Wrong password!
""")
        await state.clear()
        return

    if await become_admin(message.from_user.id):
        await message.answer("""
another admin 🤨!?
ok 
""", reply_markup= admin_kb)
        await state.clear()
        return
    else:
        await message.answer("Error, try later")
        await state.clear()












@router.message(F.text == "serach book by author")
@router.message(Command("s_by_author"))
async def get_book_by_author(message: Message, state: FSMContext):
    await message.answer("Enter author id")
    await state.set_state(search_by_ar.get_id)


@router.message(search_by_ar.get_id)
async def get_aid(message: Message, state: FSMContext):
    author_id = message.text
    if is_cancel(message.text):
        await state.clear()
        await message.answer("поиск был отменен!")
        return
    if not author_id.isdigit():
        await message.answer("id must be a number")
        await state.clear()
        return
    if not await get_author(author_id):
        await message.answer("There is no author by this id!")
        await state.clear()
        return
    
    books = await get_book_by_author(author_id)

    if not books:
        await message.answer("it seems this author does not have books yet")
        await state.clear()
        return

    text = f"Here is books by author {books[0]["author"]}\n"

    for b in books:
        text += f"""
ID: {b["id"]}
title: {b["title"]}
caption: {b["caption"]}
category: {b["category"]}
author: {b["author"]}
created at: {b["created_at"]}
"""
    await message.answer(text)
    

@router.message(F.text == "Search book by category")
@router.message(Command("seerch_by_ct"))
async def book_ct(message: Message, state: FSMContext):
    await message.answer("Enter category id")
    await state.set_state(search_by_ct.get_ct_id)


@router.message(search_by_ct.get_ct_id)
async def book_ct_id(message: Message, state: FSMContext):
    cat_id = message.text
    if is_cancel(message.text):
        await state.clear()
        await message.answer("поиск был отменен!")
        return
    if not cat_id.isdigit():
        await message.answer("id must be a number")
        await state.clear()
        return

    if not await get_category(cat_id):
        await message.answer("There is no category by this id!")
        await state.clear()
        return

    books = await get_book_by_ct(cat_id)

    if not books:
        await message.answer("it seems this author does not have books yet")
        await state.clear()
        return
    
    text = f"Here is books by author {books[0]["author"]}\n"
    
    for b in books:
        text += f"""
ID: {b["id"]}
title: {b["title"]}
caption: {b["caption"]}
category: {b["category"]}
author: {b["author"]}
created at: {b["created_at"]}
"""
    await message.answer(text)