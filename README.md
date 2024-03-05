
# Hephia-Project-Group3
### Description


L'objectif de ce projet consiste à développer un **chatbot capable de répondre efficacement à des questions médicales** auxquelles les modèles de langage classiques ont du mal à répondre en suivant un certain nombre d'étapes. Dans un premier temps, on va faire un benchmark d'un certain nombre de LLMs existants tels que  **Llama-2-7b**, **Mistral-7b**, **Falcon-7b**, **Meditron-7b**, **Gpt-3.5** et **Microsoft-Phi2**. On va évaluer ces LLMs sur un ensemble de questions médicales. Ensuite, on va fine-tuner les trois meilleurs modèles issus du benchmarking avec un dataset médical. Enfin, on va déployer le modèle sur la plateforme modal et le servir sous forme d’API afin d'alimenter l'interface du chatbot à développer. On termine un Data MAsking qui permet la détection et le masquage des informations personnelles telles que les noms des personnes, leurs identifiants bancaires , et d’autres informations personnelles, avant de les envoyer au LLM; ceci pour s'assurer de la protection de la vie privée dans les textes envoyés.

![Page_Web](/screenshots/demo.gif?raw=true)

### Architecture du projet
```bash
.
├── DataMasking
│   └── __pycache__
├── Finetuning
│   ├── GPT3-5
│   ├── Mistral
│   │   ├── __pycache__
│   │   └── src
│   │       ├── __pycache__
│   │       └── mistral-finetuned-model
│   └── Phi-2
│       └── __pycache__
├── Reports
├── TestLLM
│   ├── Falcon7b
│   ├── Falcon7bMicrosoftPhi2
│   ├── data
│   ├── llamaMistral
│   └── meditronGpt3
├── UI
│   └── web
│       ├── static
│       │   └── assets
│       └── templates
├── data
└── screenshots
```

Dans le dossier `TestLLM`, nous avons un sous-dossier pour chaque LLM Testé. Il faut juste exécuter les notebooks dans ces dossiers. Le dossier `TestLLM/data` contient le mini dataset de 10 questions utilisés pour tester les LLM. Il y'a également dans `data` le dataset final contenant, pour tous les LLMs testés, les questions , les réponses fournies, les temps de réponses, ainsi que les réponses attendues. Il nous servira de base de comparaison pour choisir les meilleurs modèles.

Dans le dossier `data`, nous avons les données utilisées pour le finetuning des modeles PHI2 et Mistral.

Dans le dossier `Finetuning`, nous avons un sous-dossier pour chaque LLM finetuné:

- Pour GPT3.5, l'entrainement et l'inférence se trouve au niveau du notebook **fine_tuning_gpt3_5.ipynb**
- Pour Phi2, l'entrainement se trouve dans le notebook **phi-2-fine-tuned.ipynb** et l'inference dans le fichier **vllm_inference.py**
- Pour Mistral, l'entrainement se trouve au niveau du fichier **src/train.py** et l'inférence au niveau du fichier **src/inference.py**

Dans le dossier `DataMasking`, nous avons les codes pour la détection et le maskage des données personnelles.

Dans le dossier `UI`, nous avons le code pour le développement de l'application web du chatbot.

Dans le dossier `Reports`, nous avons un rapport bien détaillé de toutes les étapes suivies pour mener à bien ce projet.

### Lancer localement le projet

- Créer et activer un environnement virtuel à la racine du projet avec `virtualenv myenv`
- Installer toutes les dépendances nécessaires avec `pip install -r requirements.txt`
- Créer un fichier `.env` qui contient tous les tokens, clés ou endpoints
- Pour réexecuter les entrainements ou les inférences, il faut créer un compte modal et y accéder via la CLI avec `modal setup`. Une fois ceci fait, si on veut faire l'inference de Mistral par exemple, on faudra juste lancer au niveau du terminal `modal Finetuning/Mistral/src/inference.py`.


### Interface et déploiement
- Des endpoints ont été déployé sur `Modal` pour les modèles finetunés de Phi2 et Mistral. 
- Pour les tester on peut modifier le fichier `test.py`, soit en faisant un `requests.post(URL_MODEL_PHI2, json=model_data)` ou `requests.post(URL_MODEL_MISTRAL, json=model_data)` et dans la CLI: `python test.py`.
- Pour le Data masking également, un endpoint est déployé sur Modal, pour le tester on peut juste modifier le fichier `test.py` avec `requests.post(URL_MASKING, json=masking_data)` et l'exécuter via la CLI avec `python test.py`.

- Pour tester l'interface du chatbot, il faut exécuter la commande suivante `python UI/web/app.py`. C'est une application web qui est développé avec du flask et du js. 
- Les modèles utilisés pour alimenter l'interface sont paramétrables, il suffit juste de modifier le fichier `UI/web/app.py` en faisant un `requests.post(API_URL_PHI2, json={"question": json.loads(ano)['anonymized_text']})` et `process_response(response, API_URL_PHI2)` si on veut tester le modèle PHI2 ou `requests.post(API_URL_MISTRAL, json={"question": json.loads(ano)['anonymized_text']})` et `process_response(response, API_URL_PHI2)` si on veut travailler avec Mistral.

### Technologies & environnement de travail

Pour la réalisation de ce projet, nous avons utilisé les plateformes `Modal (GPU H100 2x80Go)` et `Google Colab (GPU T4)`, le langage de programmation `python` pour l'entrainement des modèles, le framework de python `flask` et du `javascript` pour développer l'interface du chatbot.


### Screenshots
![Page_Web](/screenshots/mistral.png?raw=true)

**Reponse du modèle Microsoft-PHI2 finetuné**

![Page_Web](/screenshots/phi2.png?raw=true)

**Reponse du modèle Microsoft-MISTRAL finetuné**
