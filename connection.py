import asyncpg
from dotenv import load_dotenv
import os


load_dotenv()

p_db = os.getenv("PASSWORD_DB")

async def connection_db():
    try:
        conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="salim",
        database="fsm_task_mn",
        password= p_db
        )
        return conn
    except Exception as error:
        print(f"{type(error)}: {error} conn.py")


async def create_tables():
    try:
        conn = await connection_db()
        await conn.execute("""
        create table if not exists users(
            id serial primary key,
            username varchar(200),
            full_name varchar(200),
            telegram_id varchar(200) unique,
            created_at timestamp default now(),
            is_admin bool default false,
            is_active bool default true
        );


        create table if not exists authors(
            id serial primary key,
            full_name varchar(200),
            age int ,
            is_active bool default true
            );

        create table if not exists category(
            id serial primary key,
            name varchar(200),
            created_at timestamp default now(),
            is_active bool default true        
        );
        
        create table if not exists books(
            id serial primary key,
            title varchar(200),
            caption text,
            author_id int references authors(id),
            publisher varchar(200),
            category_id int references category(id),
            created_at timestamp default now(),
            is_active bool default true
        );

""")
        print("tables created successfuly")
    except Exception as error:
        print(f"{type(error)}: {error} ct.py")     
    finally:
        await conn.close()   