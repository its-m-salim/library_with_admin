from aiogram import  Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext 
from service import *



router = Router()

class search_by_ar(StatesGroup):
    get_id = State()


class search_by_ct(StatesGroup):
    get_ct_id = State()


class delete_book(StatesGroup):
    get_book_id = State()



@router.message(Command("s_by_author"))
async def get_book(message: Message, state: FSMContext):
    await message.answer("Enter author id")
    await state.set_state(search_by_ar.get_id)


@router.message(search_by_ar.get_id)
async def get_aid(message: Message, state: FSMContext):
    author_id = message.text
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
    


@router.message(Command("seerch_by_ct"))
async def book_ct(message: Message, state: FSMContext):
    await message.answer("Enter category id")
    await state.set_state(search_by_ct.get_ct_id)


@router.message(search_by_ct.get_ct_id)
async def book_ct_id(message: Message, state: FSMContext):
    cat_id = message.text
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