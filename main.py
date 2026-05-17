"""
1. Імпорт та первинний аналіз даних
Завантажити CSV-файл у DataFrame.
Вивести перші 5 та останні 5 рядків таблиці.
Визначити кількість рядків і стовпців.
Обчислити обсяг пам’яті, який займає датасет.

2. Аналіз структури та типів даних
Переглянути типи даних усіх стовпців.
Переконатися, чи є пропущені значення.
Зробити висновок щодо якості даних.

3.	Фільтрація вакансій за умовами
Відібрати вакансії у певній сфері (наприклад,  Cloud Computing).
Знайти вакансії з рівнем Senior.
Відібрати вакансії типу Full-Time у конкретному місті.

4.	Сортування даних за зарплатою
Відсортувати вакансії за рівнем оплати (Salary Range).
Вивести 5 вакансій з найвищою зарплатою.
Визначити, які посади є найбільш високооплачуваними.
Примітка: Salary Range подано у текстовому форматі. 

5.	Групування та агрегатні функції
Згрупувати вакансії за галузями (Industry).
Для кожної галузі визначити: 
•	кількість вакансій;
•	середню мінімальну зарплату.
Визначити галузь з найвищою середньою зарплатою.

6.	Використання apply() для створення нових ознак
Створити новий стовпець Salary Category:
•	Low - до 40 000;
•	Medium - 40 001 – 70 000;
•	High - понад 70 000.
Перевірити правильність категоризації.
Примітка: Щоб враховувати весь діапазон зарплати при категоризації, потрібно виділити максимальне значення з Salary Range і використовувати його у функції. 

7.	Часовий аналіз ринку вакансій
Перетворити колонку Date Posted у формат datetime.
Створити нову колонку Year. 
Примітка: Перетворіть стовпець Date Posted у формат дати за допомогою pd.to_datetime(). Використайте .dt.year, щоб отримати рік публікації та створити новий стовпець Year.
Проаналізувати кількість вакансій за роками та які роки були найбільш активними.
Примітка: Згрупуйте дані за роком, використовуючи groupby(). Для підрахунку кількості вакансій застосуйте метод agg() з функцією count() до стовпця Job Title.
Проаналізуйте отриману таблицю з кількістю вакансій за роками.

8.	Зробіть висновки. 
При виконанні лабораторної роботи створіть різні класи для окремих функцій (імпорт даних, фільтрування, групування тощо).
"""
import pandas as pd
import re

class DataImporter:
    # Клас для завантаження та первинного огляду даних
    def __init__(self, file_path):
        # Зчитуємо CSV-файл у DataFrame
        self.df = pd.read_csv(file_path)

    def basic_analysis(self):
        print("1. Імпорт та первинний аналіз даних\n")
        # Виводимо перші та останні 5 рядків для швидкого перегляду
        print(f"Перші 5 рядків:\n{self.df.head(5)}\n")
        print(f"Останні 5 рядків:\n{self.df.tail(5)}\n")
        
        # Отримуємо розмірність таблиці (рядки та стовпці)
        rows, columns = self.df.shape
        print(f"Кількість рядків: {rows}, кількість стовпців: {columns}\n")
        
        # Рахуємо обсяг пам'яті в байтах та переводимо в мегабайти
        memory_bytes = self.df.memory_usage(deep=True).sum()
        memory_megabytes = memory_bytes / (1024 ** 2)
        print(f"Набір даних займає: {memory_megabytes:.2f} МБ пам'яті\n")

    def structure_analysis(self):
        print("2. Аналіз структури та типів даних\n")
        # Виводимо інформацію про типи даних у кожній колонці
        print(f"Типи даних:\n{self.df.dtypes}\n")
        # Перевіряємо кількість порожніх (NaN) значень
        print(f"Пропущені значення:\n{self.df.isnull().sum()}\n")
        print("Якість даних є задовільною, оскільки немає пропущених значень.\n")
        # Повертаємо DataFrame для подальшого використання в інших класах
        return self.df


class DataFilter:
    # Клас для фільтрації записів за певними критеріями
    def __init__(self, df):
        self.df = df

    def filter_vacancies(self):
        print("3. Фільтрація вакансій за умовами\n")
        
        # Залишаємо лише ті рядки, де галузь – Cloud Computing
        cloud_vacancies = self.df[self.df['Industry'] == 'Cloud Computing']
        print(f"Вакансії у сфері Cloud Computing:\n{cloud_vacancies.head(3)}\n")
        
        # Фільтруємо вакансії за рівнем досвіду "Senior"
        senior_vacancies = self.df[self.df['Experience Level'] == 'Senior']
        print(f"Вакансії з рівнем Senior:\n{senior_vacancies.head(3)}\n")
        
        # Комбінована фільтрація: повна зайнятість ТА локація Лондон
        full_time_vacancies = self.df[(self.df['Job Type'] == 'Full-Time') & (self.df['Location'] == 'London')]
        print(f"Вакансії типу Full-Time у London:\n{full_time_vacancies.head(3)}\n")


class DataAnalyzer:
    # Клас для складнішої обробки, перетворень та аналітики
    def __init__(self, df):
        self.df = df

    def sort_by_salary(self):
        print("4. Сортування даних за зарплатою\n")
        # За допомогою регулярних виразів дістаємо перше число (мінімальну зарплату),
        # видаляємо коми та перетворюємо на ціле число (int)
        self.df['Min Salary'] = self.df['Salary Range'].str.extract(r'£(\d+,?\d*)')[0].str.replace(',', '').astype(int)
        
        # Сортуємо датасет за новою колонкою від найбільшого до найменшого
        sorted_salary = self.df.sort_values(by='Min Salary', ascending=False)
        print(f"5 вакансій з найвищою зарплатою:\n{sorted_salary[['Job Title', 'Salary Range']].head(5)}\n")
        print(f"Найбільш високооплачувані посади:\n{sorted_salary['Job Title'].head(5).tolist()}\n")

    def group_by_industry(self):
        print("5. Групування та агрегатні функції\n")
        # Групуємо дані за галуззю та застосовуємо функції:
        # рахуємо кількість посад та середнє арифметичне для 'Min Salary'
        industry_group = self.df.groupby('Industry').agg(
            vacancies_count=('Job Title', 'count'),
            avg_min_salary=('Min Salary', 'mean')
        )
        print(f"Групування за галузями:\n{industry_group.round(2)}\n")
        
        # Знаходимо назву галузі, що має найвище середнє значення зарплати
        top_industry = industry_group['avg_min_salary'].idxmax()
        print(f"Галузь з найвищою середньою зарплатою: {top_industry}\n")

    def create_salary_category(self):
        print("6. Використання apply() для створення нових ознак\n")
        
        # Допоміжна функція для визначення категорії
        def categorize_salary(salary_str):
            # Знаходимо всі числа в рядку
            matches = re.findall(r'\d+,?\d*', str(salary_str))
            # Визначаємо найбільше значення з-поміж знайдених
            max_val = max([int(m.replace(',', '')) for m in matches])
            
            # Розподіляємо на категорії залежно від максимальної зарплати
            if max_val <= 40000:
                return 'Low'
            elif 40001 <= max_val <= 70000:
                return 'Medium'
            else:
                return 'High'
                
        # Застосовуємо функцію до кожного рядка колонки 'Salary Range'
        self.df['Salary Category'] = self.df['Salary Range'].apply(categorize_salary)
        print(f"Результат категоризації (перші 5 записів):\n{self.df[['Salary Range', 'Salary Category']].head()}\n")

    def time_analysis(self):
        print("7. Часовий аналіз ринку вакансій\n")
        # Перетворюємо текстові дати на спеціальний об'єкт datetime
        self.df['Date Posted'] = pd.to_datetime(self.df['Date Posted'])
        # Створюємо окрему колонку лише з роками
        self.df['Year'] = self.df['Date Posted'].dt.year
        
        # Групуємо за роком та рахуємо кількість опублікованих вакансій
        yearly_jobs = self.df.groupby('Year').agg(vacancies_count=('Job Title', 'count'))
        print(f"Кількість вакансій за роками:\n{yearly_jobs}\n")
        
        # Знаходимо рік, коли було опубліковано найбільше вакансій
        most_active_year = yearly_jobs['vacancies_count'].idxmax()
        print(f"Найбільш активний рік за кількістю вакансій: {most_active_year}\n")

    def print_conclusions(self):
        print("8. Висновки\n")
        print("Бібліотека Pandas є гнучким інструментом для роботи з табличними даними. В ході роботи дані були успішно завантажені, очищені та проаналізовані. За допомогою регулярних виразів та методу apply() створено нові ознаки для аналітики. Часовий аналіз дозволив визначити пікові періоди активності на ринку праці, а групування показало найбільш прибуткові галузі.\n")

# Головна точка входу в програму
if __name__ == "__main__":
    # Ініціалізуємо клас для імпорту
    importer = DataImporter('Job opportunities.csv')
    importer.basic_analysis()
    # Отримуємо готовий датафрейм
    df = importer.structure_analysis()
    
    # Виконуємо фільтрацію
    filterer = DataFilter(df)
    filterer.filter_vacancies()
    
    # Аналізуємо дані (сортування, групування, категоризація)
    analyzer = DataAnalyzer(df)
    analyzer.sort_by_salary()
    analyzer.group_by_industry()
    analyzer.create_salary_category()
    analyzer.time_analysis()
    # Виводимо фінальні результати
    analyzer.print_conclusions()