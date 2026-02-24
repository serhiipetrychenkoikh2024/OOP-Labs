"""
Interface Segregation Principle (ISP)

IoT-пристрій у мережі оператора повинен лише передавати дані.
Спроєктувати систему інтерфейсів без зайвих методів.
"""
class DataTransmitter:
    def transmit_data(self):
        pass

class IoTDevice(DataTransmitter):
    def transmit_data(self):
        print("Передача даних з IoT-пристрою")

IoTDevice().transmit_data()