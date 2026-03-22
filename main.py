"""
Завдання 1. Підготовка даних
1.	Імпортуйте необхідні бібліотеки (sqlite3, pandas).
2.	Завантажте CSV-файл у Pandas DataFrame.
3.	Підключіться до бази даних SQLite (створіть нову, якщо вона не існує).
4.	Завантажте дані з DataFrame у таблицю SQLite (jobs).

Завдання 2. Основні запити SQL
1.	Виведіть перші 10 вакансій із таблиці.
2.	Виберіть усі вакансії з вимогою SQL у полі Required Skills.
Використайте WHERE `Required Skills` LIKE '%SQL%'
3.	Виведіть усі унікальні Location та Company.

Завдання 3. Аналітичні запити
1.	Обчисліть середню зарплату для кожного рівня досвіду (Experience Level).
Підказка: для цього доведеться спершу перетворити колонку Salary Range на числа (наприклад, мінімальна або середня зарплата).
2.	Підрахуйте кількість вакансій для кожного рівня досвіду (Experience Level).
3.	Знайдіть мінімальну та максимальну зарплату серед усіх вакансій.

Завдання 4. Використання агрегатних функцій
1.	Виберіть кількість вакансій у кожній індустрії (Industry) для вакансій із зарплатою більше £50,000.
2.	Обчисліть середню зарплату для кожної індустрії.

Завдання 5. Складніші запити
1.	Підрахуйте кількість вакансій за Location та Experience Level.
2.	Обчисліть загальну кількість вакансій у кожній індустрії (Industry) та для кожного типу роботи (Job Type).
3.	Визначте середню зарплату для вакансій за Location та Experience Level.

Завдання 6.* Додаткові запити для практики
1.	Виведіть 5 вакансій з найвищою верхньою межою зарплати.
2.	Підрахуйте кількість вакансій для кожного Required Skills (окремо для кожного ключового слова, якщо в колонці кілька навичок через коми).
3.	Визначте, які компанії розміщують найбільшу кількість вакансій у 2023 році.

Завдання 7. Закриття з'єднання через conn.close() 

Завдання 8. Висновки
На основі результатів аналізу даних зробіть висновки.
"""
import sqlite3
import pandas as pd
import re

class DatabaseSetup:
    def __init__(self, csv_file, db_file):
        self.csv_file = csv_file
        self.db_file = db_file
        self.conn = None

    def prepare_and_load_data(self):
        df = pd.read_csv(self.csv_file)
        
        df['Min Salary'] = df['Salary Range'].str.extract(r'£(\d+,?\d*)')[0].str.replace(',', '').astype(float)
        df['Max Salary'] = df['Salary Range'].str.extract(r'- £(\d+,?\d*)')[0].str.replace(',', '').astype(float)
        df['Max Salary'] = df['Max Salary'].fillna(df['Min Salary'])

        df['Date Posted'] = pd.to_datetime(df['Date Posted'])
        df['Year'] = df['Date Posted'].dt.year

        self.conn = sqlite3.connect(self.db_file)
        df.to_sql('jobs', self.conn, if_exists='replace', index=False)

        skills_df = df[['Required Skills']].copy()
        skills_df['Skill'] = skills_df['Required Skills'].astype(str).str.split(',')
        skills_df = skills_df.explode('Skill')
        skills_df['Skill'] = skills_df['Skill'].str.strip()
        skills_df.to_sql('job_skills', self.conn, if_exists='replace', index=False)

        return self.conn
    
    def close_connection(self):
        if self.conn:
            self.conn.close()

class BasicQueries:
    def __init__(self, conn):
        self.conn = conn

    def get_first_10_jobs(self):
        query = "SELECT * FROM jobs LIMIT 10"
        print(f"Перші 10 вакансій:\n{pd.read_sql_query(query, self.conn)}\n")

    def get_jobs_with_sql_skill(self):
        query = "SELECT * FROM jobs WHERE `Required Skills` LIKE '%SQL%'"
        print(f"Вакансії з навичкою SQL:\n{pd.read_sql_query(query, self.conn)}\n")

    def get_unique_locations_and_companies(self):
        query = "SELECT DISTINCT Location, Company FROM jobs"
        print(f"Унікальні Location та Company:\n{pd.read_sql_query(query, self.conn)}\n")

class AnalyticalQueries:
    def __init__(self, conn):
        self.conn = conn

    def run_task_3(self):
        query = "SELECT `Experience Level`, ROUND(AVG(`Min Salary`), 2) as Avg_Salary FROM jobs GROUP BY `Experience Level`"
        print(f"Середня зарплата за рівнем досвіду:\n{pd.read_sql_query(query, self.conn)}\n")

        query = "SELECT `Experience Level`, COUNT(*) as Job_Count FROM jobs GROUP BY `Experience Level`"
        print(f"Кількість вакансій за рівнем досвіду:\n{pd.read_sql_query(query, self.conn)}\n")

        query = "SELECT MIN(`Min Salary`) as Absolute_Min, MAX(`Max Salary`) as Absolute_Max FROM jobs"
        print(f"Мінімальна та максимальна зарплата серед усіх вакансій:\n{pd.read_sql_query(query, self.conn)}\n")

    def run_task_4(self):
        query = "SELECT Industry, COUNT(*) as Job_Count FROM jobs WHERE `Min Salary` > 50000 GROUP BY Industry"
        print(f"Кількість вакансій у кожній індустрії для вакансій із зарплатою більше £50,000:\n{pd.read_sql_query(query, self.conn)}\n")

        query = "SELECT Industry, ROUND(AVG(`Min Salary`), 2) as Avg_Salary FROM jobs GROUP BY Industry"
        print(f"Середня зарплата для кожної індустрії:\n{pd.read_sql_query(query, self.conn)}\n")

class ComplexQueries:
    def __init__(self, conn):
        self.conn = conn

    def run_task_5(self):
        query = "SELECT Location, `Experience Level`, COUNT(*) as Job_Count FROM jobs GROUP BY Location, `Experience Level` LIMIT 10"
        print(f"Кількість вакансій за Location та Experience Level:\n{pd.read_sql_query(query, self.conn)}\n")

        query = "SELECT Industry, `Job Type`, COUNT(*) as Job_Count FROM jobs GROUP BY Industry, `Job Type` LIMIT 10"
        print(f"Загальна кількість вакансій у кожній індустрії та для типу роботи:\n{pd.read_sql_query(query, self.conn)}\n")

        query = "SELECT Location, `Experience Level`, ROUND(AVG(`Min Salary`), 2) as Avg_Salary FROM jobs GROUP BY Location, `Experience Level` LIMIT 10"
        print(f"Середня зарплата за Location та Experience Level:\n{pd.read_sql_query(query, self.conn)}\n")

    def run_task_6(self):
        query = "SELECT `Job Title`, Company, `Max Salary` FROM jobs ORDER BY `Max Salary` DESC LIMIT 5"
        print(f"5 вакансій з найвищию верхньою межею зарплати:\n{pd.read_sql_query(query, self.conn)}\n")

        query = "SELECT Skill, COUNT(*) as Demand FROM job_skills GROUP BY Skill ORDER BY Demand DESC LIMIT 10"
        print(f"Кількість вакансій для кожної навички:\n{pd.read_sql_query(query, self.conn)}\n")

        query = "SELECT Company, COUNT(*) as Job_Count FROM jobs WHERE Year = 2023 GROUP BY Company ORDER BY Job_Count DESC LIMIT 5"
        print(f"Компанії, що розмістили найбільше вакансій у 2023 році:\n{pd.read_sql_query(query, self.conn)}\n")

if __name__ == "__main__":
    db_setup = DatabaseSetup('Job opportunities.csv', 'Jobs.db')
    conn = db_setup.prepare_and_load_data()

    basic_queries = BasicQueries(conn)
    basic_queries.get_first_10_jobs()
    basic_queries.get_jobs_with_sql_skill()
    basic_queries.get_unique_locations_and_companies()

    analytics = AnalyticalQueries(conn)
    analytics.run_task_3()
    analytics.run_task_4()

    complex_queries = ComplexQueries(conn)
    complex_queries.run_task_5()
    complex_queries.run_task_6()

    db_setup.close_connection()