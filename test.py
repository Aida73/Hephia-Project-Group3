import requests
import time
from dotenv import load_dotenv
import os
load_dotenv()
import json

URL_MODEL_PHI2 = os.getenv("URL_MODEL_PHI2")
URL_MODEL_MISTRAL = os.getenv("URL_MODEL_PHI2")
URL_MASKING = os.getenv("URL_MASKING")


# texte pour testé le datamasking
original_text = """Hello Mohamet Aidara, your telephone number is 06 12 34 56 78 and your email address 
is aidara.mohamet@example.com. I'm muslim.I live in Bois d'arcy. I work for Orange France I'm currently 
at 1 Avenue Pierrefitte-Sur Seinee. I'm 12. My NSS is 2 99 03 99 432 123 32. My passport number is A02134432"""

question = "Hello my name is Aida , I live in 13 Rue Jacques Tati A313. What is Alzheimer's disease?"

# pour tester un llm
model_data = {"question":question}

# pour tester le datamasking

masking_data = {"data":original_text}

t1= time.time()
response = requests.post(URL_MODEL_PHI2, json=model_data, timeout=100.0)
#response = requests.post(URL_MASKING, json=masking_data, timeout=100.0)
t2=time.time()
if response.status_code == 200:
    #t=json.loads(response.text)
    print(json.loads(response.text)['response'])
    print(t2-t1)
else:
    print(f"Error: {response.text}")

