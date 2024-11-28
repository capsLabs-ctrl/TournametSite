from flask import Flask, request, jsonify, render_template
import numpy as np
import check
import os
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

players_by_groups, players_scores, schedule, games = check.getGroups()
def changeGroups():
    global players_by_groups, players_scores, schedule, games
    players_by_groups, players_scores, schedule, games = check.getGroups()

STEAM_API_KEY = "73A338D501B0BE6240DFB084A570AA17"
app = Flask(__name__)


@app.route('/get_match_data', methods=['GET'])
def get_match_data():
    try:
        logging.debug("Маршрут /get_match_data вызван")

        # Получаем Match ID
        match_id = request.args.get('match_id')
        if not match_id:
            logging.warning("Match ID отсутствует в запросе")
            return jsonify({"error": "Match ID is required"}), 400

        logging.info(f"Получен Match ID: {match_id}")

        # Запрос к Steam API
        steam_api_url = f"https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/?key={STEAM_API_KEY}&match_id={match_id}"
        logging.debug(f"Отправка запроса к Steam API: {steam_api_url}")
        
        response = requests.get(steam_api_url)

        if response.status_code != 200:
            logging.error(f"Ошибка от Steam API: {response.status_code}, текст: {response.text}")
            return jsonify({"error": "Failed to fetch data from Steam API"}), response.status_code

        logging.debug("Успешно получен ответ от Steam API")

        return jsonify(response.json())
    except Exception as e:
        logging.critical(f"Критическая ошибка: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/check_tg', methods=['POST'])
def checkTelegram():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid input"}), 400
        username = data["name"]
        result = check.check_telegram_username(username)
        return jsonify({"acc_exist":result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/check_tg_in_db', methods=['POST'])
def checkTelegramInDB():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid input"}), 400
        username = data["name"]
        result = check.checkNameIsUnicue(username)
        return jsonify({"acc_alright":result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get_players', methods=['POST'])
def getFromDatabaseNames():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid input"}), 400
        names = check.getPlayersNames()
        return jsonify({"players":names}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/add_match', methods=['POST'])
def sendNewMatchToDB():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid input"}), 400
        isOk = check.sendMatchData(data)
        if isOk == True:
            changeGroups()
        return jsonify({"executed":isOk}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/check_password', methods=['POST'])
def checkCorrectPassword():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid input"}), 400
        isOk = data["hash"] == "de34d10f09c2800918c27c04b3936ab25ce958de6021b846226e8c78f43207f4"
        return jsonify({"is_same":isOk}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/send_data', methods=['POST'])
def sendToDatabase():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid input"}), 400
        isOk = check.sendData(data)
        if isOk == True:
            changeGroups()
        return jsonify({"executed":isOk}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/players_division', methods=['POST'])
def playersDivision():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid input"}), 400
        return jsonify({"players_by_groups":players_by_groups, "players_scores":players_scores, "schedule":schedule, "games":games}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/grids')
def grids():
    return render_template('gridpage.html')
    
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)