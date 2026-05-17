"""
Open/Closed Principle (OCP)

Реалізувати систему тарифікації дзвінків з базовим тарифом.
Додати новий тариф без зміни існуючого коду.
"""
class Tariff:
    # Базовий клас (інтерфейс) для всіх тарифів
    def calculate_cost(self, duration):
        pass

class BasicTariff(Tariff):
    # Конкретна реалізація базового тарифу
    def calculate_cost(self, duration):
        return duration * 1
    
class RoamingTariff(Tariff):
    # Додано новий тариф без зміни наявного коду (відкритість для розширення)
    def calculate_cost(self, duration):
        return duration * 2
    
def calculate_call_cost(tariff, duration):
    # Функція розраховує вартість незалежно від типу тарифу
    return tariff.calculate_cost(duration)    

# Виклик розрахунку для різних тарифів
print(calculate_call_cost(BasicTariff(), 10))
print(calculate_call_cost(RoamingTariff(), 10))