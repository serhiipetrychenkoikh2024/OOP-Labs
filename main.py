"""
1.	 Розробити MQTT клієнт MQTTClient, який дозволяє публікувати повідомлення на задану тему на реальному MQTT брокері.
Вимоги до завдання:
    •	Створити клас MQTTClient, який містить методи:
        o	connect(): для підключення до MQTT брокера.
        o	publish(topic, message): для публікації повідомлення на задану тему.
        o	disconnect(): для відключення від брокера.
    •	Використовувати реальний MQTT брокер для тестування:
        o	Наприклад, можна використовувати сервіси: 
            1.	CloudMQTT — безкоштовний MQTT брокер з обмеженням на кількість підключень.
            2.	HiveMQ — безкоштовний сервіс для тестування MQTT.
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
    def __init__(self, broker_address, broker_port, username, password):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS)

    def connect(self):
        self.client.connect(self.broker_address, self.broker_port, keepalive=60)
        self.client.loop_start()
        time.sleep(1)

    def publish(self, topic, message):
        result = self.client.publish(topic, message, qos=0, retain=False)
        result.wait_for_publish()
        print(f"Дані опубліковано в тему '{topic}'")

    def disconnect(self):
        time.sleep(1)
        self.client.disconnect()
        self.client.loop_stop()

def fetch_data_from_rest():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch"}

def send_via_websocket(data):
    ws_url = "wss://ws.postman-echo.com/raw"
    ws = websocket.create_connection(ws_url)
    ws.send(json.dumps(data))
    result = ws.recv()
    ws.close()
    return result

def main():
    print("1. Отримання даних через REST API...")
    rest_data = fetch_data_from_rest()
    
    print("2. Передача отриманих даних через WebSocket...")
    ws_response = send_via_websocket(rest_data)
    
    print("3. Публікація даних через MQTT...")
    
    mqtt_broker = "8024479b0cda402485f48d0ad4a02067.s1.eu.hivemq.cloud"
    mqtt_port = 8883
    mqtt_user = "NULP_14"
    mqtt_password = "NULP_14_q"
    topic = "student/lab/mqtt/data"
    
    mqtt_client = MQTTClient(mqtt_broker, mqtt_port, mqtt_user, mqtt_password)
    mqtt_client.connect()
    mqtt_client.publish(topic, ws_response)
    mqtt_client.disconnect()
    
    print("Інтеграцію завершено успішно.")

if __name__ == "__main__":
    main()