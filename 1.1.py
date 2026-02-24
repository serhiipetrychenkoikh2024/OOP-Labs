"""
Single Responsibility Principle (SRP)

Є клас CallReport, який формує звіт про дзвінки та зберігає його у файл.
Розділити відповідальності відповідно до SRP.
"""
class CallReport:
    def generate(self):
        return "Звіт про дзвінок"
    
class ReportSaver:
    def save_to_file(self, report):
        print(f"Збережено: {report}")

ReportSaver().save_to_file(CallReport().generate())