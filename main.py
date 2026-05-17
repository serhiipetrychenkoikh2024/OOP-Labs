"""
1.	 Розробити MQTT клієнт MQTTClient, який дозволяє публікувати повідомлення на задану тему на реальному MQTT брокері.
Вимоги до завдання:
    •	Створити клас MQTTClient, який містить методи:
        o	connect(): для підключення до MQTT брокера.
        o	publish(topic, message): для публікації повідомлення на задану тему.
        o	disconnect(): для відключення від брокера.
    •	Використовувати реальний MQTT брокер для тестування:
        o	Наприклад, можна використовувати сервіси: 
            1.	CloudMQTT – безкоштовний MQTT брокер з обмеженням на кількість підключень.
            2.	HiveMQ – безкоштовний сервіс для тестування MQTT.
        o	Зареєструйтесь на одному з цих сервісів та отримайте необхідні дані для підключення до брокера (адреса сервера, порт, логін, пароль).
        o	Можна використати сервіси без реєстрації, наприклад broker.hivemq.com  
    •	Інструкція по підключенню до MQTT брокера:
        o	Зареєструйтесь на обраному MQTT сервісі (наприклад, CloudMQTT або HiveMQ).
        o	Отримайте наступні дані: 
            1.	Адреса сервера (наприклад, mqtt://mqtt.eclipse.org).
            2.	Порт для підключення (наприклад, 1883 для незахищеного з’єднання або 8883 для захищеного через TLS/SSL).
            3.	Тема для публікації (наприклад, home/temperature).
        o	Використовуйте ці дані для налаштування підключення в класі MQTTClient.
2.	Інтеграція всіх компонентів у єдину систему:
    •	Створіть програму, яка:
        o	Отримує дані через REST API.
        o	Передає отримані дані через WebSocket.
        o	Публікує ці дані через MQTT.
    •	Вибрані API сервіси повинні працювати разом для передачі даних у режимі реального часу.
"""
import paho.mqtt.client as mqtt
import time
import requests
import websocket
import json
import ssl

class MQTTClient:
    # Клас для керування підключенням та публікацією через протокол MQTT
    def __init__(self, broker_address, broker_port, username, password):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client()
        
        # Встановлюємо логін та пароль для авторизації на брокері
        self.client.username_pw_set(username, password)
        # Налаштовуємо безпечне з'єднання (TLS), оскільки використовується порт 8883
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS)

    def connect(self):
        # Встановлюємо з'єднання з MQTT-брокером
        self.client.connect(self.broker_address, self.broker_port, keepalive=60)
        # Запускаємо фоновий потік обробки мережевих подій
        self.client.loop_start()
        # Невелика затримка для стабілізації підключення
        time.sleep(1)

    def publish(self, topic, message):
        # Публікуємо повідомлення на задану тему (topic)
        result = self.client.publish(topic, message, qos=0, retain=False)
        # Чекаємо, поки повідомлення буде гарантовано відправлене
        result.wait_for_publish()
        print(f"Дані опубліковано в тему '{topic}'")

    def disconnect(self):
        # Затримка перед відключенням, щоб уникнути втрати останніх даних у черзі
        time.sleep(1)
        # Відключаємося від брокера та зупиняємо фоновий цикл
        self.client.disconnect()
        self.client.loop_stop()

def fetch_data_from_rest():
    # Отримуємо тестові дані за допомогою REST API (HTTP GET-запит)
    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = requests.get(url)
    
    # Перевіряємо успішність запиту (статус 200 – ОК)
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch"}

def send_via_websocket(data):
    # Відправляємо отримані дані на ехо-сервер через WebSocket
    ws_url = "wss://ws.postman-echo.com/raw"
    # Створюємо з'єднання
    ws = websocket.create_connection(ws_url)
    
    # Перетворюємо словник у рядок JSON і відправляємо на сервер
    ws.send(json.dumps(data))
    # Отримуємо відповідь від сервера
    result = ws.recv()
    
    # Закриваємо з'єднання
    ws.close()
    return result

def main():
    # Крок 1: Отримуємо дані з відкритого REST API
    print("1. Отримання даних через REST API...")
    rest_data = fetch_data_from_rest()
    
    # Крок 2: Пропускаємо отримані дані через WebSocket
    print("2. Передача отриманих даних через WebSocket...")
    ws_response = send_via_websocket(rest_data)
    
    # Крок 3: Публікуємо фінальні дані на MQTT-брокер
    print("3. Публікація даних через MQTT...")
    
    # Налаштування для підключення до хмарного брокера HiveMQ
    mqtt_broker = "8024479b0cda402485f48d0ad4a02067.s1.eu.hivemq.cloud"
    mqtt_port = 8883
    mqtt_user = "NULP_14"
    mqtt_password = "NULP_14_q"
    topic = "student/lab/mqtt/data"
    
    # Ініціалізація клієнта, підключення, відправка даних та відключення
    mqtt_client = MQTTClient(mqtt_broker, mqtt_port, mqtt_user, mqtt_password)
    mqtt_client.connect()
    mqtt_client.publish(topic, ws_response)
    mqtt_client.disconnect()
    
    print("Інтеграцію завершено успішно.")

if __name__ == "__main__":
    # Запуск головної функції
    main()