import requests
import time
from dotenv import load_dotenv
import os
load_dotenv()
import json

URL_MODEL = os.getenv("URL_MODEL")
URL_MASKING = os.getenv("URL_MASKING")


original_text = """Hello Jean Dupont, your telephone number is 06 12 34 56 78 and your email address 
is aida.sow@example.com. I'm muslim.I live in Bois d'arcy. I work for Orange France I'm currently 
at 1 Avenue Pierrefitte-Sur Seinee. I'm 12. My NSS is 2 99 03 99 432 123 32. My passport number is A02134432"""
data = {"text":original_text}

t1= time.time()
response = requests.post(URL_MASKING, json=data, timeout=100.0)
t2=time.time()
if response.status_code == 200:
    #t=json.loads(response.text)
    print(response.text)
    print(t2-t1)
else:
    print(f"Error: {response.text}")
