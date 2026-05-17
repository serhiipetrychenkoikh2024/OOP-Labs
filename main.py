"""
Розробити WebSocket-клієнт WebSocketClient, який дозволяє підключатися до сервера, надсилати повідомлення та отримувати відповіді в асинхронному режимі.
Вимоги до виконання:
    •	Реалізувати клас WebSocketClient, що містить такі асинхронні методи: 
        o	connect(url): встановлює WebSocket-з'єднання за вказаною адресою.
        o	send_message(message): надсилає повідомлення серверу.
        o	receive_message(): отримує повідомлення від сервера.
        o	close_connection(): закриває WebSocket-з'єднання.
    •	Використовувати реальний WebSocket-сервер для тестування.
    •	Реалізувати логіку обробки помилок, якщо сервер не відповідає або з'єднання перервано.
    •	Надати приклад використання класу WebSocketClient, що демонструє відправку та отримання повідомлень в асинхронному режимі.
"""
import websockets # Бібліотека для роботи з протоколом WebSocket
import asyncio    # Бібліотека для керування асинхронними функціями

class WebSocketClient:
    # Клас для зручного керування WebSocket-з'єднанням
    def __init__(self):
        # Початковий стан: об'єкт створено, але підключення ще немає
        self.websocket = None

    async def connect(self, url):
        # Асинхронний метод для підключення до сервера за вказаною адресою
        try:
            self.websocket = await websockets.connect(url)
            print("З'єднання встановлено.")
        except Exception as e:
            # Перехоплюємо та виводимо помилку, якщо підключитися не вдалося
            print(f"Помилка підключення: {e}")

    async def send_message(self, message):
        # Перевіряємо, чи існує активне з'єднання перед відправкою
        if self.websocket:
            try:
                # Надсилаємо повідомлення на сервер
                await self.websocket.send(message)
            except Exception as e:
                # Перехоплюємо помилку, якщо мережа раптово обірвалася
                print(f"Помилка надсилання повідомлення: {e}")

    async def receive_message(self):
        # Перевіряємо, чи існує активне з'єднання перед читанням
        if self.websocket:
            try:
                # Очікуємо на вхідне повідомлення від сервера та повертаємо його
                return await self.websocket.recv()
            except Exception as e:
                # Перехоплюємо помилку, якщо під час очікування щось пішло не так
                print(f"Помилка отримання повідомлення: {e}")
        return None

    async def close_connection(self):
        # Безпечно закриваємо з'єднання, якщо воно було відкрите
        if self.websocket:
            await self.websocket.close()
            print("З'єднання закрито.")

# Адреса відкритого тестового сервера (він просто повертає надіслане йому повідомлення)
url = "wss://ws.postman-echo.com/raw"

async def main():
    # Створюємо екземпляр нашого клієнта
    client = WebSocketClient()
    
    # Спробуємо підключитися до тестового сервера
    await client.connect(url)

    # Якщо підключення пройшло успішно, починаємо обмін даними
    if client.websocket:
        # Надсилаємо тестове повідомлення
        await client.send_message("Це тестове повідомлення.")
        
        # Чекаємо на відповідь від сервера
        response = await client.receive_message()
        print(f"Отримано відповідь: {response}")
        
        # Завершуємо роботу сеансу
        await client.close_connection()

if __name__ == "__main__":
    # Запускаємо головний асинхронний цикл подій для виконання програми
    asyncio.run(main())