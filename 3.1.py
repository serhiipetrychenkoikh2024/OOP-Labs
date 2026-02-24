"""
Liskov Substitution Principle (LSP)

Є базовий клас NetworkConnection.
Реалізувати підкласи LTEConnection, WiFiConnection, які можна взаємозамінно використовувати.
"""
class NetworkConnection:
    def connect(self):
        print("Підключення до мережі")

class LTEConnection(NetworkConnection):
    def connect(self):
        print("Підключення через LTE")

class WiFiConnection(NetworkConnection):
    def connect(self):
        print("Підключення через WiFi")

def start_connection(connection):
    connection.connect()

start_connection(NetworkConnection())
start_connection(LTEConnection())
start_connection(WiFiConnection())