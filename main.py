"""
1.	Підготовка середовища та завантаження даних
    1.1.	Імпортуйте необхідні бібліотеки.
    1.2.	Завантажте файл Job opportunities.csv
    1.3.	Оскільки Salary Range - текстове поле, створіть числову колонку Average Salary
2.	Створення стовпчастої діаграми (Barplot)
    2.1.	Побудуйте діаграму, яка показує залежність середньої зарплати (Average Salary) від рівня досвіду (Experience Level).
    2.2.	Дайте відповідь на запитання про те, як змінюється середня зарплата залежно від рівня досвіду.
3.	Створення діаграми розмаху (Boxplot)
    3.1.	Створіть діаграму розмаху для відображення розподілу зарплат (Average Salary) за галузями (Industry).
    Підказка: Щоб підписи по осі X не накладалися, можна використати:
    plt.figure(figsize=(12, 6))   -  більше місця для діаграми;
    plt.xticks(rotation=45, ha='right') - ha='right' запобігає накладанню тексту;
    plt.tight_layout() - автоматично підлаштовує відступи.
    3.2.	Зробіть висновок про те, у яких галузях спостерігається вищий рівень зарплат і більший розкид значень порівняно з іншими.
4.	Створення теплової карти (Heatmap)
    4.1.	Створіть теплову карту для аналізу кількості вакансій за рівнем досвіду (Experience Level) та галуззю (Industry). 
    Підказка: Можна припустити, що кількість вакансій рівна кількості рядків у датафреймі. Тоді скористатися crosstab(), що підрахує кількість рядків у датафреймі df, які одночасно мають певний рівень досвіду та відносяться до певної галузі:
    pivot_table = pd.crosstab(df['Experience'], df['Industry'])
    Або ж використати groupby()   
    4.2.	Зробіть висновок про те, де спостерігається найбільша кількість вакансій.
5.	Створення точкової діаграми (Scatterplot)
    5.1.	Відобразіть залежність зарплати (Average Salary) від року публікації вакансії (Year, треба витягнути з Date Posted). Точки на графіку пофарбуйте за рівнем досвіду (hue='Experience Level').
    5.2.	Зробіть висновки коли спостерігається тенденція до зростання зарплат, для вакансій з яким рівнем досвіду.
6.	 Парні графіки (Pairplot)
    6.1.	Створіть парні графіки для аналізу взаємозв’язків між зарплатою, роком та рівнем досвіду.
    6.2.	Зробіть висновки з отриманих залежностей та в чому полягає відмінність точкової діаграми від парних графіків.
7.	Зробіть загальні висновки про роботу
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

class DataProcessor:
    # Клас для завантаження та попередньої обробки даних
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_and_prepare_data(self):
        # Завантажуємо дані з CSV-файлу
        self.df = pd.read_csv(self.filepath)
        
        # Застосовуємо функцію для створення нової числової колонки із середньою зарплатою
        self.df['Average Salary'] = self.df['Salary Range'].apply(self._calculate_average)
        
        # Видаляємо рядки, де не вдалося розрахувати зарплату (порожні значення)
        self.df = self.df.dropna(subset=['Average Salary'])
        
        # Перетворюємо текстову дату у формат datetime та витягуємо рік у нову колонку
        self.df['Date Posted'] = pd.to_datetime(self.df['Date Posted'])
        self.df['Year'] = self.df['Date Posted'].dt.year
        
        return self.df

    def _calculate_average(self, salary_range):
        # Допоміжний метод для обчислення середньої зарплати з тексту
        try:
            # Переводимо в нижній регістр та видаляємо коми
            s = str(salary_range).lower().replace(',', '')
            # Замінюємо 'k' на тисячі
            s = s.replace('k', '000')
            
            # Шукаємо всі числа в рядку
            numbers = re.findall(r'\d+', s)
            
            # Якщо знайдено два числа (мінімум і максимум) – рахуємо середнє
            if len(numbers) >= 2:
                return (float(numbers[0]) + float(numbers[1])) / 2
            # Якщо знайдено лише одне число – повертаємо його
            elif len(numbers) == 1:
                return float(numbers[0])
            return None
        except:
            # У разі помилки обробки повертаємо порожнє значення
            return None

class Visualizer:
    # Клас для побудови різних типів графіків за допомогою seaborn та matplotlib
    def __init__(self, dataframe):
        self.df = dataframe

    def plot_barplot(self):
        # Побудова стовпчастої діаграми
        plt.figure(figsize=(10, 6))
        # Відображаємо середню зарплату для кожного рівня досвіду
        ax = sns.barplot(x='Experience Level', y='Average Salary', data=self.df, hue='Experience Level', palette='viridis')
        
        # Прибираємо зайву легенду, оскільки підписи вже є на осі X
        if ax.legend_:
            ax.legend_.remove()
            
        plt.title('Залежність середньої зарплати від рівня досвіду')
        plt.show()

    def plot_boxplot(self):
        # Побудова діаграми розмаху
        plt.figure(figsize=(12, 6))
        # Аналізуємо розподіл зарплат у розрізі різних індустрій
        ax = sns.boxplot(x='Industry', y='Average Salary', data=self.df, hue='Industry', palette='Set2')
        
        if ax.legend_:
            ax.legend_.remove()
            
        plt.title('Розподіл зарплат за галузями')
        # Повертаємо підписи на осі X на 45 градусів, щоб вони не накладалися
        plt.xticks(rotation=45, ha='right')
        # Автоматично підлаштовуємо відступи
        plt.tight_layout()
        plt.show()

    def plot_heatmap(self):
        # Побудова теплової карти
        plt.figure(figsize=(10, 6))
        # Створюємо зведену таблицю: підраховуємо кількість вакансій за досвідом та галуззю
        pivot_table = pd.crosstab(self.df['Experience Level'], self.df['Industry'])
        
        # Малюємо теплову карту, виводимо значення всередині клітинок (annot=True)
        sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt='d')
        plt.title('Кількість вакансій за рівнем досвіду та галуззю')
        plt.show()

    def plot_scatterplot(self):
        # Побудова точкової діаграми
        plt.figure(figsize=(10, 6))
        # Відображаємо залежність зарплати від року, розфарбовуємо точки за досвідом
        sns.scatterplot(x='Year', y='Average Salary', hue='Experience Level', data=self.df, palette='deep', alpha=0.7)
        
        plt.title('Залежність зарплати від року публікації')
        # Виносимо легенду за межі графіка
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

    def plot_pairplot(self):
        # Побудова парних графіків
        # Аналізуємо взаємозв'язки між зарплатою, роком та досвідом
        g = sns.pairplot(
            self.df[['Average Salary', 'Year', 'Experience Level']], 
            hue='Experience Level', 
            palette='bright',
            diag_kind='kde' # Графіки на діагоналі відображатимуться як лінії щільності розподілу
        )
        
        # Налаштовуємо загальний заголовок для всієї сітки графіків
        g.figure.suptitle('Парні графіки: Зарплата, Рік та Рівень досвіду', y=1.0)
        g.figure.subplots_adjust(top=0.9)
        plt.show()

def main():
    # Головна функція програми
    # Ініціалізуємо клас обробки даних та готуємо дані
    processor = DataProcessor('Job opportunities.csv')
    df = processor.load_and_prepare_data()
    
    # Ініціалізуємо клас візуалізації з підготовленим датафреймом
    vis = Visualizer(df)
    
    # Викликаємо методи для малювання кожного графіка
    vis.plot_barplot()
    vis.plot_boxplot()
    vis.plot_heatmap()
    vis.plot_scatterplot()
    vis.plot_pairplot()

if __name__ == "__main__":
    # Точка входу в програму
    main()