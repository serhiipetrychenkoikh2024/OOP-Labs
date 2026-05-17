"""
Interface Segregation Principle (ISP)

Інтерфейс TelecomDevice має методи:
•	make_call()
•	send_sms()
•	connect_to_network()
Розділити інтерфейс відповідно до ISP.
"""
class CallCapable:
    # Вузькоспеціалізований інтерфейс для дзвінків
    def make_call(self):
        pass

class SMSCapable:
    # Вузькоспеціалізований інтерфейс для повідомлень
    def send_sms(self):
        pass

class NetworkCapable:
    # Вузькоспеціалізований інтерфейс для підключення до мережі
    def connect_to_network(self):
        pass

class Smartphone(CallCapable, SMSCapable, NetworkCapable):
    # Смартфон успадковує всі необхідні інтерфейси
    def make_call(self):
        print("Здійснення дзвінка")

    def send_sms(self):
        print("Відправка SMS")

    def connect_to_network(self):
        print("Підключення до мережі")
    
class IoTDevice(NetworkCapable):
    # IoT-пристрій успадковує лише те, що йому справді потрібно
    def connect_to_network(self):
        print("Підключення IoT-пристрою до мережі")

Smartphone().make_call()
Smartphone().send_sms()
Smartphone().connect_to_network()

IoTDevice().connect_to_network()