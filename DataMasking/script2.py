import spacy
import re
import random
import string
from faker import Faker


fake = Faker()
nlp = spacy.load("en_core_web_sm")

def generate_random_string(length):
    # Générer une chaîne de caractères aléatoires de la même longueur
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def anonymize_phone_numbers(text):
    return re.sub(r'\b\d{2} \d{2} \d{2} \d{2} \d{2}\b', fake.phone_number(), text)

def anonymize_emails(text):
    return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', fake.email(), text)

def anonymize_nss(text):
    text = re.sub(r'\b\d{1} \d{2} \d{2} \d{2} \d{3} \d{3} \d{2}\b', fake.ssn(), text)
    return re.sub(r'\b\d{15}\b', fake.ssn(), text)

def anonymize_addresses(text):
    address_pattern = r'\b(\d+)?\s*(Avenue|Ave|Bd|Boulevard|Rue|Route)\s+[A-Za-z0-9\s\-\'éèàê]+'
    return re.sub(address_pattern, lambda x: fake.address(), text)


def anonymize_passport_visa(text):
    return re.sub(r'\b[A-Z]{1}[0-9]{8}\b', fake.passport_number(), text)

def anonymize_entities(text):
    doc = nlp(text)
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
            random_string = generate_random_string(len(ent.text))
            anonymized_text = anonymized_text[:ent.start_char] + random_string + anonymized_text[ent.end_char:]
    return anonymized_text

def anonymize(text):
    text = anonymize_entities(text)
    text = anonymize_phone_numbers(text)
    text = anonymize_emails(text)
    text = anonymize_nss(text)
    text = anonymize_passport_visa(text)
    text = anonymize_addresses(text)
    return text

original_text = """Hello Jean Dupont, your telephone number is 06 12 34 56 78 and your email address 
is aida.sow@example.com. I'm muslim.I live in Bois d'arcy. I work for Orange France I'm currently 
at 1 Avenue Pierrefitte-Sur Seinee. I'm 12. My NSS is 2 99 03 99 432 123 32. My passport number is A02134432"""
text = """Hello my name is Aida. My email address 
is aida.sow@example.com. , I live in 13 Avenue Jacques Tati A313. 
What is Diabetes?. Mon numero est le 06 12 34 56 78. My NSS is 2 99 03 99 432 123 32"""
anonymized_text = anonymize(original_text)
print("Texte anonymisé :\n", anonymized_text)

