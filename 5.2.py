"""
Dependency Inversion Principle (DIP)

Реалізувати можливість підключення:
•	FileLogger
•	ServerLogger
•	ConsoleLogger
Без зміну у коді класу NetworkMonitor.
"""
class Logger:
    def log(self, message):
        pass

class FileLogger(Logger):
    def log(self, message):
        print(f"Запис у файл: {message}")

class ServerLogger(Logger):
    def log(self, message):
        print(f"Запис на сервер: {message}")

class ConsoleLogger(Logger):
    def log(self, message):
        print(f"Вивід на консоль: {message}")

class NetworkMonitor:
    def __init__(self, logger: Logger):
        self.logger = logger

    def monitor(self):
        self.logger.log("Моніторинг мережі")

monitor = NetworkMonitor(FileLogger())
monitor.monitor()
monitor = NetworkMonitor(ServerLogger())
monitor.monitor()
monitor = NetworkMonitor(ConsoleLogger())
monitor.monitor()