"""
Interface Segregation Principle (ISP)

IoT-пристрій у мережі оператора повинен лише передавати дані.
Спроєктувати систему інтерфейсів без зайвих методів.
"""
class DataTransmitter:
    # Інтерфейс містить лише один необхідний метод
    def transmit_data(self):
        pass

class IoTDevice(DataTransmitter):
    # Пристрій не обтяжений зайвими методами (наприклад, для дзвінків)
    def transmit_data(self):
        print("Передача даних з IoT-пристрою")

IoTDevice().transmit_data()