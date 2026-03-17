from sqlalchemy import text,select,and_
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from datetime import datetime,timedelta
from typing import List,Literal
from sqlalchemy.orm import sessionmaker
import asyncpg
import os
from dotenv import load_dotenv
from payment_models import metadata_obj,table
import asyncio
import atexit
from sqlalchemy import func
#backend.database.
import uuid 


load_dotenv()


async_engine = create_async_engine(
    f"postgresql+asyncpg://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@localhost:5432/payment_db",
    pool_size=20,          
    max_overflow=50,        
    pool_recycle=3600,      
    pool_pre_ping=True,     
    echo=False
)



AsyncSessionLocal = sessionmaker(
    async_engine, 
    class_=AsyncSession,
    expire_on_commit=False
)

async def drop_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata_obj.drop_all)

async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)



async def create_payment(provider_token:str,order_id:str,price:int) -> str:
    payment_id = str(uuid.uuid4())
    async with AsyncSession(async_engine) as conn:
        async with conn.begin():
            stmt = table.insert().values(
                payment_id = payment_id ,
                order_id = order_id, 
                status = "pending",
                provider_payment_id = provider_token,
                price = price
            )
            await conn.execute(stmt)
            return payment_id


