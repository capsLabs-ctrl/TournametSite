from flask import Flask, request, jsonify, render_template
import numpy as np
from check import check_telegram_username, sendData
import os

app = Flask(__name__)

@app.route('/check_tg', methods=['POST'])
def checkTelegram():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid input"}), 400
        username = data["name"]
        mmr = data["mmr"]
        tg = data["tgname"]
        result = check_telegram_username(username)
        return jsonify({"acc_exist":result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/send_data', methods=['POST'])
def sendToDatabase():
    try:
        data = request.get_json()
        if not data or "inputs" not in data:
            return jsonify({"error": "Invalid input"}), 400
        username = data["inputs"]
        isOk = sendData()
        return jsonify({"executed":isOk}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/', methods=['POST'])
def home():
    return render_template('index.html')
    
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)