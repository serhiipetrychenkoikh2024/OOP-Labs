"""
1.	Створити базу даних та таблицю nodes, яка зберігатиме інформацію про мережеві вузли (ID, IP-адресу, статус). 
2.	Реалізувати асинхронну функцію для отримання списку вузлів із бази. 
3.	Реалізувати асинхронну систему збору статусів вузлів (імітація мережевих запитів). 
4.	Зберігати отримані дані у базі за допомогою SQLAlchemy. 
5.	Продемонструвати та пояснити результати виконання програми (створення таблиці, додавання 10-15 вузлів, моніторинг з оновленням статусу, виведення списку вузлів до та після оновлення і т.д.).
"""
import asyncio
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select

DATABASE_URL = "sqlite+aiosqlite:///network.db"
Base = declarative_base()

class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key = True)
    ip_address = Column(String, unique = True, nullable = False)
    status = Column(String, default = 'unknown')

engine = create_async_engine(DATABASE_URL, echo = True)
AsyncSessionLocal = sessionmaker(engine, class_ = AsyncSession, expire_on_commit = False)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_nodes():
    async with AsyncSessionLocal() as session:
        nodes = [Node(ip_address = f'192.168.1.{i}', status = 'active') for i in range(1, 16)]
        session.add_all(nodes)
        await session.commit()

async def get_nodes():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Node))
        nodes = result.scalars().all()
        for node in nodes:
            print(f'ID: {node.id}, IP: {node.ip_address}, Status: {node.status}')

async def monitor_nodes():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Node))
        nodes = result.scalars().all()
        for node in nodes:
            node.status = 'offline' if int(node.ip_address.split('.')[-1]) % 2 == 0 else 'active'
        await session.commit()

async def reset_nodes():
    async with AsyncSessionLocal() as session:
        await session.execute(text('DELETE FROM nodes'))
        await session.commit()

async def main():
    await create_tables()
    await add_nodes()

    print('\nВузли перед моніторингом:\n')
    await get_nodes()
    await monitor_nodes()

    print('\nВузли після моніторингу:\n')
    await get_nodes()
    await reset_nodes()

    await engine.dispose()

if __name__ == '__main__':
    asyncio.run(main())