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
import websockets
import asyncio

class WebSocketClient:
    def __init__(self):
        self.websocket = None

    async def connect(self, url):
        try:
            self.websocket = await websockets.connect(url)
            print("З'єднання встановлено.")
        except Exception as e:
            print(f"Помилка підключення: {e}")

    async def send_message(self, message):
        if self.websocket:
            try:
                await self.websocket.send(message)
            except Exception as e:
                print(f"Помилка надсилання повідомлення: {e}")

    async def receive_message(self):
        if self.websocket:
            try:
                return await self.websocket.recv()
            except Exception as e:
                print(f"Помилка отримання повідомлення: {e}")
        return None

    async def close_connection(self):
        if self.websocket:
            await self.websocket.close()
            print("З'єднання закрито.")

url = "wss://ws.postman-echo.com/raw"

async def main():
    client = WebSocketClient()
    await client.connect(url)

    if client.websocket:
        await client.send_message("Це тестове повідомлення.")
        response = await client.receive_message()
        print(f"Отримано відповідь: {response}")
        await client.close_connection()

if __name__ == "__main__":
    asyncio.run(main())