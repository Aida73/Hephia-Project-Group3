from flask import Flask, render_template, request, jsonify
import requests
from unidecode import unidecode
from dotenv import load_dotenv
import os
import json
load_dotenv()

app = Flask(__name__)
API_URL_MISTRAL = os.getenv("URL_MODEL_MISTRAL")
API_URL_PHI2 = os.getenv("URL_MODEL_PHI2")
API_URL_MASKING = os.getenv("URL_MASKING")

def process_response(response, API_URL):
    if API_URL == API_URL_MISTRAL:
        bot_response = unidecode(response.json())
        bot_response = response.json()
    elif API_URL == API_URL_PHI2:
        bot_response = json.loads(response.text)
        bot_response = bot_response['response']
    return bot_response



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    
    user_message = request.json.get('question')
    print(user_message)
    try:
        masking_response = requests.post(API_URL_MASKING, json={"text": user_message})
        if masking_response.status_code==200:
            ano = masking_response.text
            print(json.loads(ano)['anonymized_text'])
            response = requests.post(API_URL_PHI2, json={"question": json.loads(ano)['anonymized_text']})
            if response.status_code == 200:
                bot_response = process_response(response, API_URL_PHI2)
                return jsonify({'response': bot_response})
            else:
                return jsonify({'response': "An error occurs"}), 500
        else:
            return jsonify({'response': "An error occurs"}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({'response': f"An error occurs: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
