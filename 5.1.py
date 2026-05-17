"""
Dependency Inversion Principle (DIP)

Система моніторингу мережі напряму використовує FileLogger.
Перепроєктувати систему відповідно до DIP.
"""
class Logger:
    # Абстракція логера (високорівневий інтерфейс)
    def log(self, message):
        pass

class FileLogger(Logger):
    # Деталь реалізації (низькорівневий модуль)
    def log(self, message):
        print(f"Запис у файл: {message}")

class App:
    # Додаток залежить від абстракції (Logger), а не від конкретного FileLogger
    def __init__(self, logger: Logger):
        self.logger = logger

    def run(self):
        self.logger.log("Додаток запущено")

# Впровадження залежності під час створення об'єкта
app = App(FileLogger())
app.run()