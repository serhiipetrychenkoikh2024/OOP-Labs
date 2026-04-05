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
import requests

class RestClient:
    def get(self, endpoint):
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Помилка: {response.status_code}")
            return None

    def post(self, endpoint, data):
        response = requests.post(endpoint, json = data)
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Помилка: {response.status_code}")
            return None

if __name__ == "__main__":
    client = RestClient()

    url = "https://jsonplaceholder.typicode.com/posts"

    data = client.get(url)
    if data:
        print(data[:2])

    new_post = {
        "title": "Новий пост",
        "body": "Це тестовий пост",
        "userId": 1
    }
    created_post = client.post(url, new_post)
    if created_post:
        print(f"Створено пост: {created_post}")