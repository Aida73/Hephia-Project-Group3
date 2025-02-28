

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="/screenshots/bot.gif" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">IA Générative</h3>

  <p align="center">
    Fine Tunning LLMs: Mistral, Phi2 & GP3
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    &middot;
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project
The aim of this project is to develop a **chatbot capable of efficiently answering medical questions** that conventional language models have difficulty answering, by following a number of steps. First, we will benchmark a number of existing LLMs, such as **Llama-2-7b**, **Mistral-7b**, **Falcon-7b**, **Meditron-7b**, **Gpt-3.5** and **Microsoft-Phi2**. We'll evaluate these LLMs on a set of medical questions. Then, we'll fine-tune the three best models from the benchmarking with a medical dataset. Finally, we'll deploy the model on the modal platform and serve it as an API to feed the chatbot interface to be developed. We'll finish off with data masking, which detects and masks personal information such as people's names, bank details and other personal data, before sending it to the LLM; this is to ensure that privacy is protected in the texts sent.

<!-- GETTING STARTED -->
## Getting Started

Notice the architecture of the project after cloned looks like this:
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
<!-- ![Page_Web](/screenshots/demo.gif?raw=true) -->

### Architecture du projet


In the `TestLLM` folder, we have a subfolder for each LLM tested. Just run the notebooks in these folders. The `TestLLM/data` folder contains the 10-question mini-dataset used to test the LLMs. Also in `data` is the final dataset containing, for all LLMs tested, the questions, answers given, response times and expected answers. This will serve as a basis for comparison when selecting the best models.

In the `data` folder, we have the data used for finetuning the PHI2 and Mistral models.

In the `Finetuning` folder, we have a subfolder for each LLM finetuned:

- For GPT3.5, training and inference can be found in the notebook **fine_tuning_gpt3_5.ipynb**.
- For Phi2, training is in the notebook **phi-2-fine-tuned.ipynb** and inference in the file **vllm_inference.py**.
- For Mistral, training is in the file **src/train.py** and inference in the file **src/inference.py**.

In the `DataMasking` folder, we have the codes for detecting and masking personal data.

In the `UI` folder, we have the code for developing the chatbot's web application.

In the `Reports` folder, we have a detailed report of all the steps taken to complete this project.

### Prerequisites

You must have Python, Pip, Virtualenv & Modal installed on your computer to run this project.


### Installation

1. Clone the repo
   ```sh
    git clone https://github.com/Aida73/Hephia-Project-Group3.git
   ```
2. Create and activate a virtualenv at the root of the project
    ```sh
    python3 -m venv tutorial_env
    source venv/bin/activate
    ```
3. Install all necessary dependencies 
    ```sh
    pip install -r requirements.txt
    ```
4. Create a `.env` file that will contain all tokens, keys & endpoints

5. To execute the training or access to web page, you must create an modal account et access via CLI:
    ```sh
    modal setud
    ```
5. Once this done, if you want to do inference with Mistral, you can run on the CLI:
    ```sh
    modal Finetuning/Mistral/src/inference.py
    ```
6. To lauch the Chatbot web app, execute the following command:
    ```sh
    python UI/web/app.py
    ```


### Interface & deployment
- Des endpoints ont été déployé sur `Modal` pour les modèles finetunés de Phi2 et Mistral. 
- Pour les tester on peut modifier le fichier `test.py`, soit en faisant un `requests.post(URL_MODEL_PHI2, json=model_data)` ou `requests.post(URL_MODEL_MISTRAL, json=model_data)` et dans la CLI: `python test.py`.
- Pour le Data masking également, un endpoint est déployé sur Modal, pour le tester on peut juste modifier le fichier `test.py` avec `requests.post(URL_MASKING, json=masking_data)` et l'exécuter via la CLI avec `python test.py`.
- Par défaut, c'est Mistral qui est utilisé pour alimenter l'interface. Toutefois, le modèle à utiliser reste paramétrable. En effet, il suffit juste de modifier le fichier `UI/web/app.py` en faisant un `requests.post(API_URL_PHI2, json={"question": json.loads(ano)['anonymized_text']})` et `process_response(response, API_URL_PHI2)` si on veut tester le modèle PHI2 ou `requests.post(API_URL_MISTRAL, json={"question": json.loads(ano)['anonymized_text']})` et `process_response(response, API_URL_PHI2)` si on veut travailler avec Mistral.

### Build with

For this project, we used:
* [Modal (GPU H100 2x80Go)](https://modal.com/docs/guide/gpu)
* [Google Colab (GPU T4)](https://colab.research.google.com/)
* [Flask](https://flask.palletsprojects.com/en/stable/)
* [Javascript](https://developer.mozilla.org/fr/docs/Web/JavaScript)


<!-- `Modal (GPU H100 2x80Go)` and `Google Colab (GPU T4)` platforms, the `python` programming language for model training, the `flask` python framework and `javascript` to develop the chatbot interface.
 -->

## Usage
![Page_Web](/screenshots/mistral.png?raw=true)

**Microsoft-PHI2 finetuned response**

![Page_Web](/screenshots/phi2.png?raw=true)

**Microsoft-MISTRAL finetuned response**
