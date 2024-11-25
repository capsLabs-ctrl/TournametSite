from flask import Flask, request, jsonify, render_template
import numpy as np
import check
import os

app = Flask(__name__)

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
        username = data["name"]
        mmr = data["mmr"]
        tg = data["tgname"]
        isOk = check.sendData({"name":username, "tg_name":tg, "mmr":mmr})
        return jsonify({"executed":isOk}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/send_data', methods=['POST'])
def sendToDatabase():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid input"}), 400
        username = data["name"]
        mmr = data["mmr"]
        tg = data["tgname"]
        isOk = check.sendData({"name":username, "tg_name":tg, "mmr":mmr})
        return jsonify({"executed":isOk}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/')
def home():
    return render_template('index.html')
    
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)