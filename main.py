"""
Розробити клієнт RestClient для взаємодії з REST API, реалізувавши методи GET та POST.
Вимоги до виконання:
    •	Реалізуйте клас RestClient, що підтримує такі методи: 
        o	get(endpoint): виконує HTTP GET-запит та повертає отримані дані.
        o	post(endpoint, data): виконує HTTP POST-запит з переданими даними.
    •	Використовуйте бібліотеку requests для Python.
    •	Використайте відкритий REST API (наприклад, JSONPlaceholder або OpenWeatherMap), що дозволяє доступитися до розміщених там ресурсів. Для доступу до деяких API потрібно отримати API-ключ (див. інструкцію в теоретичній частині). 
    •	Продемонструйте декілька прикладів використання RestClient для запитів до обраного API. 
    •	Впевніться, що запити коректно обробляють відповіді сервера (перевірка статус-кодів, обробка помилок) та зробіть висновки.
"""
import requests # Імпортуємо бібліотеку для виконання HTTP-запитів

class RestClient:
    # Клас для зручної взаємодії з веб-сервісами (REST API)
    
    def get(self, endpoint):
        # Виконуємо HTTP-запит GET для отримання даних за вказаною адресою
        response = requests.get(endpoint)
        
        # Статус 200 означає "ОК" (запит успішний)
        if response.status_code == 200:
            return response.json() # Перетворюємо відповідь у зручний формат (словник/список Python)
        else:
            # Якщо сталася помилка, виводимо її код
            print(f"Помилка: {response.status_code}")
            return None

    def post(self, endpoint, data):
        # Виконуємо HTTP-запит POST для відправки нових даних на сервер
        response = requests.post(endpoint, json = data)
        
        # Статус 201 означає "Created" (ресурс успішно створено на сервері)
        if response.status_code == 201:
            return response.json() # Повертаємо інформацію про створений об'єкт
        else:
            print(f"Помилка: {response.status_code}")
            return None

if __name__ == "__main__":
    # Створюємо екземпляр нашого клієнта
    client = RestClient()

    # Адреса відкритого тестового API для публікацій
    url = "https://jsonplaceholder.typicode.com/posts"

    # Демонстрація GET-запиту: отримуємо список усіх постів
    data = client.get(url)
    if data:
        # Виводимо на екран лише перші 2 записи, щоб не перевантажувати консоль
        print(data[:2])

    # Словник з даними для нового поста, який ми хочемо створити
    new_post = {
        "title": "Новий пост",
        "body": "Це тестовий пост",
        "userId": 1
    }
    
    # Демонстрація POST-запиту: відправляємо дані на сервер
    created_post = client.post(url, new_post)
    if created_post:
        # Виводимо відповідь сервера (переважно це ті самі дані + унікальний ID)
        print(f"Створено пост: {created_post}")