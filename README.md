
# Hephia-Project-Group3
### Description


L'objectif de ce projet consiste à développer un **chatbot capable de répondre efficacement à des questions médicales** auxquelles les modèles de langage classiques ont du mal à répondre.

### Etapes suivies

- **Evaluer les LLM sur des questions médicales**:
    génération d'un ensemble de questions avec gpt4 et évaluation sur les modèles **Llama-2-7b**, **Mistral-7b**, **Falcon-7b**, **Meditron-7b**, **Gpt-3.5** et **Microsoft-Phi2**

- **Fine-tuning d'un LLM sur des données médicales:**
    ré-entrainement des trois meilleurs LLMs du benchmarking avec le dataset médical et choix du meilleur modèle avec la plus petite taille et les meilleurs résultats.

    - Choix du dataset médical:
    - Fine-tuner les modèles avec l'API **Trainer** et montrer que le modèle répond aux questions de l’étape 1 après le réentraînement
    - Comparer le modèle final avec LLM Méditron

- **Création de l’interface et déploiement du modèle:** 
    - Déploiement du modèle sur la plateforme modal et le servir sous forme d’API
    - Création de l'interface du chatbot 

- **Data Masking:** 
    détection et masquage des informations personnelles telles que les noms des personnes, leurs identifiants bancaires , et d’autres informations personnelles, avant de les envoyer au LLM; ceci pour s'assurer de la protection de la vie privée dans les textes envoyés.