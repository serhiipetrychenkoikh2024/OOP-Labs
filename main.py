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
    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        if b == 0:
            raise ValueError("Ділити на нуль не можна!")
        return a / b

class LibraryItem:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def details(self):
        return f"Книга '{self.title}', автор: {self.author}, рік видання: {self.year}"

class NotificationService:
    def send(self, message):
        pass

class UserManager:
    def __init__(self, service):
        self.service = service

    def notify_user(self, message):
        self.service.send(message)

def check_even(number):
    return number % 2 == 0

class TestMathTool(unittest.TestCase):
    def setUp(self):
        self.math = MathTool()

    def test_add(self):
        self.assertEqual(self.math.add(5, 3), 8)

    def test_sub(self):
        self.assertEqual(self.math.sub(10, 4), 6)

    def test_mul(self):
        self.assertEqual(self.math.mul(7, 6), 42)

    def test_div_success(self):
        self.assertEqual(self.math.div(20, 4), 5.0)

    def test_div_by_zero(self):
        with self.assertRaises(ValueError):
            self.math.div(10, 0)

class TestLibraryItem(unittest.TestCase):
    def test_details(self):
        item1 = LibraryItem("Тіні забутих предків", "Михайло Коцюбинський", 1911)
        item2 = LibraryItem("Тигролови", "Іван Багряний", 1944)
        
        self.assertEqual(item1.details(), "Книга 'Тіні забутих предків', автор: Михайло Коцюбинський, рік видання: 1911")
        self.assertEqual(item2.details(), "Книга 'Тигролови', автор: Іван Багряний, рік видання: 1944")

class TestUserManager(unittest.TestCase):
    def test_notify_user(self):
        mock_service = Mock(spec=NotificationService)
        manager = UserManager(mock_service)
        
        test_message = "Вітаємо в системі!"
        manager.notify_user(test_message)
        
        mock_service.send.assert_called_once_with(test_message)

class TestCheckEven(unittest.TestCase):
    @parameterized.expand([
        ("positive_even", 8, True),
        ("positive_odd", 7, False),
        ("negative_even", -4, True),
        ("negative_odd", -9, False),
        ("zero", 0, True),
    ])
    def test_check_even(self, name, val, expected):
        self.assertEqual(check_even(val), expected)

if __name__ == "__main__":
    unittest.main()