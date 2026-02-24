"""
Liskov Substitution Principle (LSP)

Виправити створену ієрархію, де клас SatelliteConnection порушує очікувану поведінку базового класу (супутник не може працювати як звичайне з’єднання).
"""
class NetworkConnection:
    def connect(self):
        print("Підключення до мережі")

class WifiConnection(NetworkConnection):
    def connect(self):
        print("Підключення через WiFi")

class SatelliteConnection(NetworkConnection):
    def __init__(self, object):
        self.object = object

    def connect(self):
        print(f"Підключення супутника з {self.object}")

def start_connection(connection):
    connection.connect()

start_connection(NetworkConnection())
start_connection(WifiConnection())
start_connection(SatelliteConnection("землею"))