"""
Interface Segregation Principle (ISP)

Інтерфейс TelecomDevice має методи:
•	make_call()
•	send_sms()
•	connect_to_network()
Розділити інтерфейс відповідно до ISP.
"""
class CallCapable:
    def make_call(self):
        pass

class SMSCapable:
    def send_sms(self):
        pass

class NetworkCapable:
    def connect_to_network(self):
        pass

class Smartphone(CallCapable, SMSCapable, NetworkCapable):
    def make_call(self):
        print("Здійснення дзвінка")

    def send_sms(self):
        print("Відправка SMS")

    def connect_to_network(self):
        print("Підключення до мережі")
    
class IoTDevice(NetworkCapable):
    def connect_to_network(self):
        print("Підключення IoT-пристрою до мережі")

Smartphone().make_call()
Smartphone().send_sms()
Smartphone().connect_to_network()

IoTDevice().connect_to_network()