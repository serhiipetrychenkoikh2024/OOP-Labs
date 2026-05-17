"""
Single Responsibility Principle (SRP)

Є клас CallReport, який формує звіт про дзвінки та зберігає його у файл.
Розділити відповідальності відповідно до SRP.
"""
class CallReport:
    # Цей клас відповідає виключно за генерацію звіту
    def generate(self):
        return "Звіт про дзвінок"
    
class ReportSaver:
    # Цей клас відповідає виключно за збереження звіту
    def save_to_file(self, report):
        print(f"Збережено: {report}")

# Створюємо звіт і передаємо його іншому об'єкту для збереження
ReportSaver().save_to_file(CallReport().generate())