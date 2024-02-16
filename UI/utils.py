import requests

def mistral_endpoint(question: str):
    try:
        data = {"question": question}
        response = requests.post("https://unsupervise--heph3-mistral7b-finetune-inference.modal.run", json=data, timeout=100.0)
        
        if response.status_code == 200:
            return response.text
        else:
            return "Network error. Please retry."
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"