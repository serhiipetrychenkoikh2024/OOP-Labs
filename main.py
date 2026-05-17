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

# Шлях до файлу бази даних SQLite з використанням асинхронного драйвера aiosqlite
DATABASE_URL = "sqlite+aiosqlite:///network.db"
# Базовий клас для створення моделей (структур таблиць)
Base = declarative_base()

class Node(Base):
    # Назва таблиці у базі даних
    __tablename__ = 'nodes'
    
    # Створюємо колонки таблиці
    id = Column(Integer, primary_key = True)                         # Унікальний ідентифікатор вузла
    ip_address = Column(String, unique = True, nullable = False)     # IP-адреса (унікальна, не може бути порожньою)
    status = Column(String, default = 'unknown')                     # Статус вузла (за замовчуванням 'unknown')

# Створюємо асинхронний "двигун" (engine) для підключення до БД. echo=True дозволяє бачити SQL-запити в консолі.
engine = create_async_engine(DATABASE_URL, echo = True)
# Фабрика для створення асинхронних сесій (сеансів роботи з базою)
AsyncSessionLocal = sessionmaker(engine, class_ = AsyncSession, expire_on_commit = False)

async def create_tables():
    # Асинхронно створюємо таблицю nodes у базі даних, якщо її ще не існує
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_nodes():
    # Відкриваємо сесію для додавання нових вузлів
    async with AsyncSessionLocal() as session:
        # Генеруємо 15 вузлів з IP-адресами від 192.168.1.1 до 192.168.1.15
        nodes = [Node(ip_address = f'192.168.1.{i}', status = 'active') for i in range(1, 16)]
        # Додаємо всі вузли в сесію
        session.add_all(nodes)
        # Зберігаємо (комітимо) зміни у базу даних
        await session.commit()

async def get_nodes():
    # Відкриваємо сесію для читання даних
    async with AsyncSessionLocal() as session:
        # Виконуємо запит на отримання всіх записів з таблиці Node
        result = await session.execute(select(Node))
        # Витягуємо результати у вигляді списку об'єктів
        nodes = result.scalars().all()
        
        # Виводимо інформацію про кожен вузол у консоль
        for node in nodes:
            print(f'ID: {node.id}, IP: {node.ip_address}, Status: {node.status}')

async def monitor_nodes():
    # Відкриваємо сесію для оновлення статусів
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Node))
        nodes = result.scalars().all()
        
        # Імітація моніторингу: якщо остання цифра IP-адреси парна, статус 'offline', інакше 'active'
        for node in nodes:
            node.status = 'offline' if int(node.ip_address.split('.')[-1]) % 2 == 0 else 'active'
        
        # Зберігаємо оновлені статуси в базу
        await session.commit()

async def reset_nodes():
    # Відкриваємо сесію для очищення таблиці (видалення всіх записів)
    async with AsyncSessionLocal() as session:
        await session.execute(text('DELETE FROM nodes'))
        await session.commit()

async def main():
    # 1. Створюємо таблиці
    await create_tables()
    # 2. Додаємо початкові вузли
    await add_nodes()

    print('\nВузли перед моніторингом:\n')
    # 3. Виводимо початковий стан вузлів
    await get_nodes()
    
    # 4. Проводимо "моніторинг" (змінюємо статуси)
    await monitor_nodes()

    print('\nВузли після моніторингу:\n')
    # 5. Виводимо оновлений стан вузлів
    await get_nodes()
    
    # 6. Очищаємо базу після роботи, щоб наступний запуск працював "з чистого аркуша"
    await reset_nodes()

    # Закриваємо з'єднання з базою
    await engine.dispose()

if __name__ == '__main__':
    # Запускаємо головну асинхронну функцію
    asyncio.run(main())