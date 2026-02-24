"""
Dependency Inversion Principle (DIP)

Система моніторингу мережі напряму використовує FileLogger.
Перепроєктувати систему відповідно до DIP.
"""
class Logger:
    def log(self, message):
        pass

class FileLogger(Logger):
    def log(self, message):
        print(f"Запис у файл: {message}")

class App:
    def __init__(self, logger: Logger):
        self.logger = logger

    def run(self):
        self.logger.log("Додаток запущено")

app = App(FileLogger())
app.run()