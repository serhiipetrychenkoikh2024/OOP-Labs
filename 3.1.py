"""
Liskov Substitution Principle (LSP)

Є базовий клас NetworkConnection.
Реалізувати підкласи LTEConnection, WiFiConnection, які можна взаємозамінно використовувати.
"""
class NetworkConnection:
    # Загальний контракт для підключення
    def connect(self):
        print("Підключення до мережі")

class LTEConnection(NetworkConnection):
    # Коректно реалізує підключення через мобільну мережу
    def connect(self):
        print("Підключення через LTE")

class WiFiConnection(NetworkConnection):
    # Коректно реалізує підключення через Wi-Fi
    def connect(self):
        print("Підключення через WiFi")

def start_connection(connection):
    # Функція без проблем працює з будь-яким спадкоємцем NetworkConnection
    connection.connect()

# Демонстрація взаємозамінності об'єктів
start_connection(NetworkConnection())
start_connection(LTEConnection())
start_connection(WiFiConnection())