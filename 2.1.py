"""
Open/Closed Principle (OCP)

Реалізувати систему тарифікації дзвінків з базовим тарифом.
Додати новий тариф без зміни існуючого коду.
"""
class Tariff:
    def calculate_cost(self, duration):
        pass

class BasicTariff(Tariff):
    def calculate_cost(self, duration):
        return duration * 1
    
class RoamingTariff(Tariff):
    def calculate_cost(self, duration):
        return duration * 2
    
def calculate_call_cost(tariff, duration):
    return tariff.calculate_cost(duration)    

print(calculate_call_cost(BasicTariff(), 10))
print(calculate_call_cost(RoamingTariff(), 10))