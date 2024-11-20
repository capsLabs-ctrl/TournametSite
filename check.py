import requests
from bs4 import BeautifulSoup
import mysql.connector

def check_telegram_username(username):
    url = f"https://t.me/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Отправляем запрос к странице
        response = requests.get(url, headers=headers)
        
        # Проверяем успешность запроса
        if response.status_code == 200:
            # Парсим HTML-контент страницы
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Ищем признаки отсутствия пользователя
            if f"If you have Telegram, you can contact @{username} right away." in soup.text or f"@{username}" not in soup.text:
                return False  # Пользователь не существует
            
            # Если текст ошибки не найден, пользователь существует
            return True
        else:
            print(f"Ошибка: страница недоступна (код {response.status_code})")
            return None
    except Exception as e:
        print(f"Ошибка соединения: {e}")
        return None

def sendData(data):
    try:
        # Устанавливаем соединение
        connection = mysql.connector.connect(
            host="bhihmdlzeva9nple8r0v-mysql.services.clever-cloud.com",
            user="uluyy4kz85l4bapm",
            password="CpGIFlfBYYkDtDltZSv8",
            database="bhihmdlzeva9nple8r0v",
            port=3306
        )
        cursor = connection.cursor()
        # Запрос на вставку
        query = "INSERT INTO Учасники (Имя, Телеграм, ММР) VALUES (%s, %s, %s)"
        values = (data["name"], data["tg_name"], data["mmr"])
        cursor.execute(query, values)

        # Подтверждаем изменения
        connection.commit()
        print(f"Inserted {cursor.rowcount} row(s).")  # Выводим количество добавленных строк

        cursor.close()
        connection.close()
        return True  # Успешная вставка данных
    except Error as e:
        print(f"Error: {e}")  # Выводим описание ошибки
        return False
print(check_telegram_username("capsLabss"))