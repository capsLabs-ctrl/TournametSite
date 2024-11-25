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
        query = "INSERT INTO Учасники (Имя, Телеграм, Цифры_стима) VALUES (%s, %s, %s)"
        values = (data["name"], data["tgname"], data["steam"])
        cursor.execute(query, values)

        # Подтверждаем изменения
        connection.commit()
        print(f"Inserted {cursor.rowcount} row(s).")  # Выводим количество добавленных строк

        cursor.close()
        connection.close()
        return True  # Успешная вставка данных
    except mysql.connector.Error as e:
        print(f"Error: {e}")  # Выводим описание ошибки
        return False
    

def sendMatchData(data):
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

        # Получаем коды игроков по их именам
        query_get_code = "SELECT Код FROM Учасники WHERE Имя = %s"

        # Получаем Код для Игрок1
        cursor.execute(query_get_code, (data["player1"],))
        player1_code = cursor.fetchone()
        if player1_code is None:
            raise ValueError(f"Игрок с именем {data['player1']} не найден в таблице Учасники")
        player1_code = player1_code[0]

        # Получаем Код для Игрок2
        cursor.execute(query_get_code, (data["player2"],))
        player2_code = cursor.fetchone()
        if player2_code is None:
            raise ValueError(f"Игрок с именем {data['player2']} не найден в таблице Учасники")
        player2_code = player2_code[0]

        # Получаем Код для Победителя
        cursor.execute(query_get_code, (data["winner"],))
        winner_code = cursor.fetchone()
        if winner_code is None:
            raise ValueError(f"Игрок с именем {data['winner']} не найден в таблице Учасники")
        winner_code = winner_code[0]

        # Вставляем данные в таблицу Матчи
        query_insert_match = """
            INSERT INTO Матчи (Игрок1, Игрок2, Победитель, idМатча, Дата, Групповой_матч)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (player1_code, player2_code, winner_code, data["matchID"], data["date"], data["group"])
        cursor.execute(query_insert_match, values)

        # Подтверждаем изменения
        connection.commit()
        print(f"Матч добавлен: {cursor.rowcount} строка(и).")

        cursor.close()
        connection.close()
        return True
    except mysql.connector.Error as e:
        print(f"Ошибка: {e}")
        return False
    except ValueError as e:
        print(f"Ошибка: {e}")
        return False
    
def checkNameIsUnicue(name):
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
        query = F"SELECT * FROM Учасники WHERE Телеграм = '{name}'"
        cursor.execute(query)
# Получение всех строк
        cursor.fetchall()
# Количество строк, которые вернул запрос
        row_count = cursor.rowcount 
        cursor.close()
        connection.close()
        return row_count==0

def getPlayersNames():
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
        query = F"SELECT Имя FROM Учасники"
        cursor.execute(query)
# Получение всех строк
        players = cursor.fetchall()
# Количество строк, которые вернул запрос
        cursor.close()
        connection.close()
        player_names = [player[0].rstrip() for player in players]
        return player_names

# sendData({'steam':"1231231231", 'name':"Никита", 'tgname':"capsl"})
# sendMatchData({"player1":"Никита", "player2":"Залупенск", "winner":"Никита", "matchID":"1231231231", "date":"2024-01-01", 'group':True})