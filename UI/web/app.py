from flask import Flask, render_template, request, jsonify
import requests
from unidecode import unidecode

app = Flask(__name__)
API_URL = "https://unsupervise--heph3-mistral7b-finetune-inference.modal.run"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    
    user_message = request.json.get('question')
    print(user_message)
    try:
        response = requests.post(API_URL, json={"question": user_message})
        
        if response.status_code == 200:
            bot_response = unidecode(response.json())
            bot_response = response.json()
            print(bot_response)
            return jsonify({'response': bot_response})
        else:
            return jsonify({'response': "Erreur lors de l'appel à l'API du modèle."}), 500
    
    except requests.exceptions.RequestException as e:
        return jsonify({'response': f"Erreur de requête : {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
