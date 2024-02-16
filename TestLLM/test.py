import requests

data = {"question": "Good afternoon"}
response = requests.post("https://unsupervise--heph3-mistral7b-finetune-inference.modal.run", json=data, timeout=100.0)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the response content
    print(response.text)
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.text}")
#Vérifier si la requête a été réussie (code d'état 200)
# if response.status_code == 200:
#     # Parcourir le contenu de la réponse de manière asynchrone
#     for chunk in response.iter_content(chunk_size=128):
#         if chunk:
#             # Traiter chaque morceau de données (chunk) ici
#             print(chunk)
# else:
#     # Afficher un message d'erreur si la requête n'a pas été réussie
#     print(f"Erreur: {response.text}")