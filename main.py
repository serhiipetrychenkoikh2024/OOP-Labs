"""
1. Тестування виконання арифметичних операцій
Створіть клас MathTool, який реалізує основні арифметичні операції:
    •	складання чисел
    •	різниця між двома числами
    •	множення
    •	ділення з перевіркою на поділ на нуль
Реалізуйте модульні тести до кожної з цих операцій. Перевірте поведінку методу ділення у випадку, коли другий аргумент дорівнює нулю. 
2. Тестування класу LibraryItem
Створіть клас LibraryItem, який має поля: title, author, year. Додайте метод details(), який повертає рядок із повною інформацією про об'єкт.
Напишіть юніт-тест, який перевіряє, чи коректно метод details() формує інформацію для різних прикладів.
3. Тестування взаємодії класів з використанням mock
Створіть два класи: NotificationService (має метод send) та UserManager, який використовує NotificationService для надсилання повідомлень. В класі UserManager реалізуйте метод notify_user.
Створіть мок-об’єкт для NotificationService і протестуйте, що notify_user коректно викликає метод send із заданими параметрами.
4. Параметризовані тести для парності числа
Опишіть функцію check_even(number), яка повертає True, якщо число парне, і False інакше.
Створіть набір параметризованих тестів із використанням @parameterized.expand, щоб перевірити функцію на різних прикладах: позитивні числа, від’ємні, нуль, непарні значення.
"""
import unittest
from parameterized import parameterized
from unittest.mock import Mock

class MathTool:
    # Клас для виконання базових арифметичних операцій
    def add(self, a, b):
        # Складання двох чисел
        return a + b

    def sub(self, a, b):
        # Віднімання другого числа від першого
        return a - b

    def mul(self, a, b):
        # Множення двох чисел
        return a * b

    def div(self, a, b):
        # Ділення з обов'язковою перевіркою на нуль
        if b == 0:
            raise ValueError("Ділити на нуль не можна!")
        return a / b

class LibraryItem:
    # Клас, що описує елемент бібліотеки (книгу)
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def details(self):
        # Формує та повертає рядок з детальною інформацією
        return f"Книга '{self.title}', автор: {self.author}, рік видання: {self.year}"

class NotificationService:
    # Базовий сервіс для відправки повідомлень
    def send(self, message):
        pass

class UserManager:
    # Менеджер користувачів, який залежить від зовнішнього сервісу
    def __init__(self, service):
        self.service = service

    def notify_user(self, message):
        # Делегує відправку повідомлення сервісу сповіщень
        self.service.send(message)

def check_even(number):
    # Повертає True, якщо остача від ділення на 2 дорівнює нулю
    return number % 2 == 0

class TestMathTool(unittest.TestCase):
    # Набір тестів для перевірки математичних операцій
    def setUp(self):
        # Метод setUp виконується перед кожним тестом – створює свіжий екземпляр класу
        self.math = MathTool()

    def test_add(self):
        # Перевірка правильності додавання
        self.assertEqual(self.math.add(5, 3), 8)

    def test_sub(self):
        # Перевірка правильності віднімання
        self.assertEqual(self.math.sub(10, 4), 6)

    def test_mul(self):
        # Перевірка правильності множення
        self.assertEqual(self.math.mul(7, 6), 42)

    def test_div_success(self):
        # Перевірка успішного ділення (результат має бути дробовим)
        self.assertEqual(self.math.div(20, 4), 5.0)

    def test_div_by_zero(self):
        # Перевірка того, що при діленні на нуль генерується виняток ValueError
        with self.assertRaises(ValueError):
            self.math.div(10, 0)

class TestLibraryItem(unittest.TestCase):
    # Набір тестів для бібліотечного класу
    def test_details(self):
        item1 = LibraryItem("Тіні забутих предків", "Михайло Коцюбинський", 1911)
        item2 = LibraryItem("Тигролови", "Іван Багряний", 1944)
        
        # Перевіряємо, чи метод details() повертає рядок очікуваного формату
        self.assertEqual(item1.details(), "Книга 'Тіні забутих предків', автор: Михайло Коцюбинський, рік видання: 1911")
        self.assertEqual(item2.details(), "Книга 'Тигролови', автор: Іван Багряний, рік видання: 1944")

class TestUserManager(unittest.TestCase):
    # Набір тестів для перевірки взаємодії класів
    def test_notify_user(self):
        # Створюємо "мок" (імітацію) об'єкта NotificationService
        mock_service = Mock(spec=NotificationService)
        # Передаємо мок-об'єкт у менеджер
        manager = UserManager(mock_service)
        
        test_message = "Вітаємо в системі!"
        manager.notify_user(test_message)
        
        # Перевіряємо, чи викликав UserManager метод send нашого мок-об'єкта з правильним текстом
        mock_service.send.assert_called_once_with(test_message)

class TestCheckEven(unittest.TestCase):
    # Використовуємо декоратор для запуску одного тесту з різними параметрами
    @parameterized.expand([
        ("positive_even", 8, True),   # Додатне парне число
        ("positive_odd", 7, False),   # Додатне непарне число
        ("negative_even", -4, True),  # Від'ємне парне число
        ("negative_odd", -9, False),  # Від'ємне непарне число
        ("zero", 0, True),            # Нуль
    ])
    def test_check_even(self, name, val, expected):
        # Цей метод запуститься 5 разів – по одному разу для кожного рядка з масиву вище
        self.assertEqual(check_even(val), expected)

if __name__ == "__main__":
    # Запускає виконання всіх тестів, якщо файл запущено напряму
    unittest.main()