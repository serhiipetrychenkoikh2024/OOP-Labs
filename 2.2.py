"""
Open/Closed Principle (OCP)

Система підтримує тарифи: VoiceTariff, DataTariff.
Розширити систему тарифом RoamingTariff, не змінюючи логіку розрахунку вартості.
"""
class Tariff:
    def calculate_cost(self, duration):
        pass

class VoiceTariff(Tariff):
    def calculate_cost(self, duration):
        return duration * 1
    
class DataTariff(Tariff):
    def calculate_cost(self, duration):
        return duration * 0.5
    
class RoamingTariff(Tariff):
    def calculate_cost(self, duration):
        return duration * 2
    
def calculate_call_cost(tariff, duration):
    return tariff.calculate_cost(duration)

print(calculate_call_cost(VoiceTariff(), 10))
print(calculate_call_cost(DataTariff(), 10))
print(calculate_call_cost(RoamingTariff(), 10))