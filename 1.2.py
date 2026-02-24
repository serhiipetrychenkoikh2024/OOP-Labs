"""
Single Responsibility Principle (SRP)

Клас Subscriber:
•	зберігає дані абонента
•	відправляє SMS
•	розраховує баланс
Перепроєктувати систему так, щоб кожен клас мав одну відповідальність. 
"""
class SubscriberDataSaver:
    def save_data(self):
        print("Збережено дані абонента")

class SMSSender:
    def send_sms(self):
        print("SMS відправлено")

class BalanceCalculator:
    def calculate_balance(self):
        print("Баланс розраховано")

SubscriberDataSaver().save_data()
SMSSender().send_sms()
BalanceCalculator().calculate_balance()