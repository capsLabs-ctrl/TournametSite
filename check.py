import requests
from bs4 import BeautifulSoup
import mysql.connector
from itertools import combinations
from functools import cmp_to_key
import random

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

def getGroups():
    ##Разделение игроков на группы
    players_by_groups = []
    players_count_in_groups = [0,0,0,0]
    player_names = getPlayersNames()
    players_count = len(player_names)
    winners_points = getWinners()
    i=0
    while i<(players_count)%4:
        players_count_in_groups[i] += 1
        i += 1
    j = 0
    while j<len(players_count_in_groups):
        players_count_in_groups[j] += (players_count-i)//4
        j+=1
    i = 0
    k = 0
    while i<len(players_count_in_groups):
        j = 0
        players_by_groups.append([])
        while j<players_count_in_groups[i]:
            players_by_groups[i].append(player_names[k])
            j+=1
            k+=1
        i+=1
    ##Подсчёт очков игроков
    players_scores = []
    i=0
    while i<len(players_by_groups):
        j = 0
        players_scores.append([])
        while j<len(players_by_groups[i]):
            if players_by_groups[i][j] in winners_points:
                players_scores[i].append(winners_points[players_by_groups[i][j]])
            else:
                players_scores[i].append(0)
            j+=1
        i+=1
    while i<len(players_by_groups):
        j = 0
        while j<len(players_by_groups[i]):

            j+=1
        i+=1
    ##Сортировка игроков по очкам
    sorted_players_by_groups, sorted_players_scores = sort_players_by_scores(players_by_groups, players_scores, db_check_match)
    schedule = generate_schedule(sorted_players_by_groups)
    return sorted_players_by_groups, sorted_players_scores, schedule

def getWinners():
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
    query = f"SELECT Учасники.Имя, COUNT(*) AS Очки FROM Матчи JOIN Учасники ON Матчи.Победитель = Учасники.Код WHERE Матчи.Групповой_матч = 1 GROUP BY Учасники.Имя ORDER BY Очки DESC;"
    cursor.execute(query)
    players = cursor.fetchall()
    cursor.close()
    connection.close()
    player_points = {player[0].strip(): player[1] for player in players}
    return player_points

def generate_schedule(groups, max_matches_per_day=4, seed=42):
    schedule = []  # Список, в котором будем хранить расписание по дням
    random.seed(seed)  # Зафиксировать seed для детерминированных случайных чисел
    for group in groups:
        # Получаем все возможные пары игроков в группе
        matches = list(combinations(group, 2))
        
        # Структура для хранения матчей по дням
        group_schedule = []
        
        # Перемешиваем список матчей для равномерного распределения
        random.shuffle(matches)

        # Разбиваем матчи на дни, соблюдая лимит по матчам в день
        while matches:
            day_matches = matches[:max_matches_per_day]
            group_schedule.append(day_matches)
            matches = matches[max_matches_per_day:]
        
        schedule.append(group_schedule)
    
    return schedule


def compare_players(player1, player2, scores, db_check_match):
    """
    Сравнивает двух игроков по их очкам и результатам матчей.
    
    player1, player2: имена игроков
    scores: словарь {имя игрока: очки}
    db_check_match: функция для проверки результатов матчей в базе данных
    """
    score1 = scores[player1]
    score2 = scores[player2]
    if score1 > score2:
        return -1  # player1 выше
    elif score1 < score2:
        return 1  # player2 выше
    else:
        # Если очки равны, проверяем результат матча
        match_result = db_check_match(player1, player2)
        if match_result == player1:
            return -1  # player1 выше
        elif match_result == player2:
            return 1  # player2 выше
        else:
            return 0  # оставляем как есть, если матчей нет
        
def sort_players_by_scores(players_by_groups, players_scores, db_check_match):
    """
    Сортирует игроков в каждой группе с учётом очков и результатов матчей.

    players_by_groups: список групп с игроками
    players_scores: список очков игроков в группах
    db_check_match: функция для проверки результатов матчей в базе данных
    """
    sorted_players_by_groups = []
    sorted_players_scores = []

    for group, scores in zip(players_by_groups, players_scores):
        # Создаём словарь {имя игрока: очки} для удобства
        scores_dict = {player: score for player, score in zip(group, scores)}

        # Сортируем группу с использованием cmp_to_key
        sorted_group = sorted(
            group, 
            key=cmp_to_key(lambda x, y: compare_players(x, y, scores_dict, db_check_match))
        )
        
        # Пересобираем отсортированные очки
        sorted_scores = [scores_dict[player] for player in sorted_group]

        # Добавляем в итоговые списки
        sorted_players_by_groups.append(sorted_group)
        sorted_players_scores.append(sorted_scores)

    return sorted_players_by_groups, sorted_players_scores

def db_check_match(player1, player2):
    """
    Проверяет результаты матчей между двумя игроками в базе данных.
    Возвращает имя победителя или None, если матча нет.
    """
    try:
        # Установление соединения с базой данных
        connection = mysql.connector.connect(
            host="bhihmdlzeva9nple8r0v-mysql.services.clever-cloud.com",
            user="uluyy4kz85l4bapm",
            password="CpGIFlfBYYkDtDltZSv8",
            database="bhihmdlzeva9nple8r0v",
            port=3306
        )
        cursor = connection.cursor()

        # Параметризованный запрос для безопасности
        query = """
        SELECT Учасники.Имя
        FROM Матчи
        INNER JOIN Учасники ON Матчи.Победитель = Учасники.Код
        INNER JOIN Учасники as p1 ON p1.Код = Матчи.Игрок1 
        INNER JOIN Учасники as p2 ON p2.Код = Матчи.Игрок2
        WHERE 
            (p1.Имя = %s AND p2.Имя = %s) OR 
            (p1.Имя = %s AND p2.Имя = %s)
        """
        cursor.execute(query, (player1, player2, player2, player1))
        result = cursor.fetchone()  # Получаем только первую строку

        if result:
            return result[0]  # Возвращаем имя победителя (первый элемент кортежа)
        return None

    except mysql.connector.Error as err:
        print(f"Ошибка при работе с базой данных: {err}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# result = db_check_match("Артем Николенко", "Зевс бог МОЛНИЙ!!!!")
# if result:
#     print(f"Победитель: {result}")
# else:
#     print("Матч между игроками не найден.")
players, scores, schedule = getGroups()
# for i, group_schedule in enumerate(schedule):
#     print(f"Группа {i+1}:")
#     for day, matches in enumerate(group_schedule, 1):
#         print(f"  День {day}: {', '.join([f'{match[0]} vs {match[1]}' for match in matches])}")
#     print("\n")
# print(players)
# print(schedule)
# sendData({'steam':"1231231231", 'name':"Никита", 'tgname':"capsl"})
# sendMatchData({"player1":"Никита", "player2":"Залупенск", "winner":"Никита", "matchID":"1231231231", "date":"2024-01-01", 'group':True})