from modal import Stub, web_endpoint, Image
import spacy
import re
import random
import string
from pydantic import BaseModel
from faker import Faker

image = Image.debian_slim().pip_install("spacy","Faker").run_commands(
        "python -m spacy download 'en_core_web_sm'"
    )
stub = Stub("heph3-pi-mask",image=image)


nlp = spacy.load("en_core_web_sm")
fake = Faker()
nlp = spacy.load("en_core_web_sm")

# Générer une chaîne de caractères aléatoires de la même longueur
def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

# Détecter les numeros de téléphone présents dans le texte et les remplacer par des faux avec faker
def anonymize_phone_numbers(text):
    return re.sub(r'\b\d{2} \d{2} \d{2} \d{2} \d{2}\b', fake.phone_number(), text)

# Détecter les adresses mail présentes dans le texte et les remplacer par des faux avec faker
def anonymize_emails(text):
    return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', fake.email(), text)

# Détecter les numeros de sécurité social présents dans le texte et les remplacer par des faux avec faker
def anonymize_nss(text):
    text = re.sub(r'\b\d{1} \d{2} \d{2} \d{2} \d{3} \d{3} \d{2}\b', fake.ssn(), text)
    return re.sub(r'\b\d{15}\b', fake.ssn(), text)

# Détecter les autres types d'adresses( comme 1 Ave etc) présents dans le texte et les remplacer par des faux avec faker
def anonymize_addresses(text):
    address_pattern = r'\b(\d+)?\s*(Avenue|Ave|Av.|Av|Bd|Boulevard|Rue|Route)\s+[A-Za-z0-9\s\-\'éèàê]+'
    return re.sub(address_pattern, lambda x: fake.address(), text)

# Détecter les numeros de passport présents dans le texte et les remplacer par des faux avec faker
def anonymize_passport_visa(text):
    return re.sub(r'\b[A-Z]{1}[0-9]{8}\b', fake.passport_number(), text)


def anonymize_entities(text):
    doc = nlp(text)
    # les objets à détecter dans le texte de l'utilisateur
    replacements = {
        "PERSON": "Name",
        "ORG": "Organization",
        "NORP": "Group",
        "GPE": "Location",
        "FAC": "Facility",
        "LOC": "Address"
    }
    anonymized_text = text
    for ent in reversed(doc.ents):
        if ent.label_ in replacements:
            # Utiliser la fonction de génération de texte aléatoire pour anonymiser les données sensibles détectées
            random_string = generate_random_string(len(ent.text))
            anonymized_text = anonymized_text[:ent.start_char] + random_string + anonymized_text[ent.end_char:]
    return anonymized_text

# Ajouter un objet json pour le body du endpoint
class Data(BaseModel):
    text: str

# Publier un endpoint pour utiliser le datamasking
@stub.function(gpu="h100")
@web_endpoint(method="POST")
def anonymize(data: Data):
    text = data.text
    text = anonymize_entities(text)
    text = anonymize_phone_numbers(text)
    text = anonymize_emails(text)
    text = anonymize_nss(text)
    text = anonymize_passport_visa(text)
    return {"anonymized_text": text}