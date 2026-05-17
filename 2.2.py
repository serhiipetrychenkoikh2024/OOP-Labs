"""
Open/Closed Principle (OCP)

Система підтримує тарифи: VoiceTariff, DataTariff.
Розширити систему тарифом RoamingTariff, не змінюючи логіку розрахунку вартості.
"""
class Tariff:
    # Спільний інтерфейс розрахунку
    def calculate_cost(self, duration):
        pass

class VoiceTariff(Tariff):
    # Тариф для дзвінків
    def calculate_cost(self, duration):
        return duration * 1
    
class DataTariff(Tariff):
    # Тариф для інтернету
    def calculate_cost(self, duration):
        return duration * 0.5
    
class RoamingTariff(Tariff):
    # Новий тариф легко інтегрується як спадкоємець
    def calculate_cost(self, duration):
        return duration * 2
    
def calculate_call_cost(tariff, duration):
    # Логіка залишається незмінною для будь-яких нових тарифів
    return tariff.calculate_cost(duration)

# Тестування роботи різних тарифів
print(calculate_call_cost(VoiceTariff(), 10))
print(calculate_call_cost(DataTariff(), 10))
print(calculate_call_cost(RoamingTariff(), 10))