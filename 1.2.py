"""
Single Responsibility Principle (SRP)

Клас Subscriber:
•	зберігає дані абонента
•	відправляє SMS
•	розраховує баланс
Перепроєктувати систему так, щоб кожен клас мав одну відповідальність. 
"""
class SubscriberDataSaver:
    # Відповідає тільки за збереження даних
    def save_data(self):
        print("Збережено дані абонента")

class SMSSender:
    # Відповідає тільки за відправку повідомлень
    def send_sms(self):
        print("SMS відправлено")

class BalanceCalculator:
    # Відповідає тільки за фінансові розрахунки
    def calculate_balance(self):
        print("Баланс розраховано")

# Кожна дія виконується відповідним спеціалізованим класом
SubscriberDataSaver().save_data()
SMSSender().send_sms()
BalanceCalculator().calculate_balance()