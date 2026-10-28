from connection import *

admin_ps = "admin12"


async def get_all_books():
    try:
        conn = await connection_db()
        books = await conn.fetch("""
        select authors.full_name as author, books.id, category.name as category, books.title, books.caption, books.created_at from books
        left join authors on authors.id = books.author_id
        left join category on category.id = books.category_id
""")
        return books
    except Exception as error:
        print(f"{type(error)}: {error} sgb.py")     
    finally:
        await conn.close()   


async def get_book(b_id):
    try:
        conn = await connection_db()
        book = await conn.fetchrow("""
        select authors.full_name as author, books.id, category.name as category, books.title, books.caption, books.created_at from books
        left join authors on authors.id = books.author_id
        left join category on category.id = books.category_id
        where books.id = $1
""", int(b_id))
        return book
    except Exception as error:
        print(f"{type(error)}: {error} sgb.py")  
        return False   
    finally:
        await conn.close()   





async def create_user(username, full_name, tg_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into users(username, full_name, telegram_id) values
            ($1, $2, $3)
""", username, full_name, str(tg_id))
        return True
    except Exception as error:
        print(f"{type(error)}: {error} su.py")     
    finally:
        await conn.close()   



async def profile(tg_id):
    try:
        conn = await connection_db()
        user = await conn.fetchrow("""
        select * from users where telegram_id = $1
""", str(tg_id))
        return user
    except Exception as error:
        print(f"{type(error)}: {error} sp.py")    
        return False 
    finally:
        await conn.close()   


async def add_book(title, caption, author_id, category_id):
    try:
        conn = await connection_db()
        result = await conn.execute("""
        insert into books(title, caption, author_id, category_id) values
            ($1, $2, $3, $4)
""", title, caption, int(author_id),  int(category_id))
        if result == "UPDATE 1":
            return True
    except Exception as error:
        print(f"{type(error)}: {error} sab.py")     
        return False
    finally:
        await conn.close()   


async def get_book_by_author(author_id):
    try:
        conn = await connection_db()
        books = await conn.fetch("""
        select authors.full_name as author, books.id, category.name as category, books.title, books.caption, books.created_at from books
        join authors on authors.id = books.author_id
        join category on category.id = books.category_id
        where author_id  = $1
""", int(author_id))

        return books
    except Exception as error:
        print(f"{type(error)}: {error} sgba.py")     
    finally:
        await conn.close()   


async def get_book_by_ct(category_id):
    try:
        conn = await connection_db()
        books = await conn.fetch("""
        select authors.full_name as author, books.id, category.name as category, books.title, books.caption, books.created_at from books
        join category on category.id = books.category_id
        join authors on authors.id = books.author_id
        where category_id  = $1
""", int(category_id))

        return books
    except Exception as error:
        print(f"{type(error)}: {error} sgbc.py")     
    finally:
        await conn.close()   



async def is_admin(tg_id):
    try:
        conn = await connection_db()
        admin = await conn.fetchrow("""
        select * from users
        where telegram_id = $1
        and is_admin = true
""", str(tg_id))
        return admin
    except Exception as error:
        print(f"{type(error)}: {error} sid.py")     
    finally:
        await conn.close()   


async def get_author(author_id):
    try:
        conn = await connection_db()
        author = await conn.fetchrow("""
        select * from authors
        where id = $1
""", int(author_id))

        return author
    except Exception as error:
        print(f"{type(error)}: {error} sga.py")     
    finally:
        await conn.close()   


async def get_category(cat_id):
    try:
        conn = await connection_db()
        category = await conn.fetchrow("""
        select * from category
        where id = $1
""", int(cat_id))

        return category
    except Exception as error:
        print(f"{type(error)}: {error} sgc.py")     
        return False
    finally:
        await conn.close()   



async def get_authors():
    try:
        conn = await connection_db()
        authors = await conn.fetch("""
        select * from authors
""")
        return authors
    except Exception as error:
        print(f"{type(error)}: {error} sgas.py")     
        return False
    finally:
        await conn.close()   




async def become_admin(tg_id):
    try:
        conn = await connection_db()
        admin = await conn.fetchrow("""
        update users
        set is_admin = true
        where telegram_id = $1
        returning id
""", str(tg_id))

        if not admin:
            return False

        return True
    except Exception as error:
        print(f"{type(error)}: {error} sba.py")     
    finally:
        await conn.close()   



async def get_categories():
    try:
        conn = await connection_db()
        category = await conn.fetch("""
        select * from category
""")
        return category
    except Exception as error:
        print(f"{type(error)}: {error} sgcs.py")     
        return False
    finally:
        await conn.close()   



async def delete_book(b_id):
    try:
        conn = await connection_db()
        result = await conn.fetchrow("""
        delete from books where
        id = $1
""", b_id)
        return result
    except Exception as error:
        print(f"{type(error)}: {error} sdb.py")     
        return False
    finally:
        await conn.close()   

        