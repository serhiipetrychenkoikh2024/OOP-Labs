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
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_and_prepare_data(self):
        self.df = pd.read_csv(self.filepath)
        self.df['Average Salary'] = self.df['Salary Range'].apply(self._calculate_average)
        self.df = self.df.dropna(subset=['Average Salary'])
        self.df['Date Posted'] = pd.to_datetime(self.df['Date Posted'])
        self.df['Year'] = self.df['Date Posted'].dt.year
        return self.df

    def _calculate_average(self, salary_range):
        try:
            s = str(salary_range).lower().replace(',', '')
            s = s.replace('k', '000')
            numbers = re.findall(r'\d+', s)
            if len(numbers) >= 2:
                return (float(numbers[0]) + float(numbers[1])) / 2
            elif len(numbers) == 1:
                return float(numbers[0])
            return None
        except:
            return None

class Visualizer:
    def __init__(self, dataframe):
        self.df = dataframe

    def plot_barplot(self):
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x='Experience Level', y='Average Salary', data=self.df, hue='Experience Level', palette='viridis')
        if ax.legend_:
            ax.legend_.remove()
        plt.title('Залежність середньої зарплати від рівня досвіду')
        plt.show()

    def plot_boxplot(self):
        plt.figure(figsize=(12, 6))
        ax = sns.boxplot(x='Industry', y='Average Salary', data=self.df, hue='Industry', palette='Set2')
        if ax.legend_:
            ax.legend_.remove()
        plt.title('Розподіл зарплат за галузями')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def plot_heatmap(self):
        plt.figure(figsize=(10, 6))
        pivot_table = pd.crosstab(self.df['Experience Level'], self.df['Industry'])
        sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt='d')
        plt.title('Кількість вакансій за рівнем досвіду та галуззю')
        plt.show()

    def plot_scatterplot(self):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Year', y='Average Salary', hue='Experience Level', data=self.df, palette='deep', alpha=0.7)
        plt.title('Залежність зарплати від року публікації')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

    def plot_pairplot(self):
        g = sns.pairplot(
            self.df[['Average Salary', 'Year', 'Experience Level']], 
            hue='Experience Level', 
            palette='bright',
            diag_kind='kde'
        )
        g.figure.suptitle('Парні графіки: Зарплата, Рік та Рівень досвіду', y=1.0)
        g.figure.subplots_adjust(top=0.9)
        plt.show()

def main():
    processor = DataProcessor('Job opportunities.csv')
    df = processor.load_and_prepare_data()
    
    vis = Visualizer(df)
    vis.plot_barplot()
    vis.plot_boxplot()
    vis.plot_heatmap()
    vis.plot_scatterplot()
    vis.plot_pairplot()

if __name__ == "__main__":
    main()