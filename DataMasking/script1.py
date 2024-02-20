import spacy
from datetime import datetime
import re

nlp = spacy.load("en_core_web_sm")

"""
    PERSON : Personne réelle ou fictive.
    NORP : Groupe ethnique, religieux ou politique.
    FAC : Bâtiments, aéroports, autoroutes, ponts, etc.
    ORG : Entreprises, agences gouvernementales, institutions, etc.
    GPE : Pays, villes, états.
    LOC : Lieux géographiques non-GPE, par exemple des montagnes, des mers.
    PRODUCT : Objets, véhicules, aliments, etc. (non-services).
    EVENT : Événements.
    WORK_OF_ART : Titres de livres, chansons, etc.
    LAW : Lois et règlements.
    LANGUAGE : Noms de langues.
    DATE : Indicateurs de date ou de période.
    TIME : Indicateurs de temps plus petits qu'une journée.
    PERCENT : Pourcentages, y compris "%".
    MONEY : Monnaies, y compris les symboles monétaires.
    QUANTITY : Mesures, quantités, ou valeurs numériques.
    ORDINAL : "Premier", "deuxième", etc.
    CARDINAL : Numéraux cardinaux, "1", "deux", etc.
"""
def anonymize(text):
    doc = nlp(text)
    anonymized_text = text
    for ent in doc.ents:
        if ent.label_ == "PERSON":  #bien 
            anonymized_text = anonymized_text.replace(ent.text, "Name")
        elif ent.label_ == "ORG":  #bien
            anonymized_text = anonymized_text.replace(ent.text, "ORG")
        elif ent.label_ == "NORP":  #bien
            anonymized_text = anonymized_text.replace(ent.text, "X")
        elif ent.label_ == "GPE":  # bien
            anonymized_text = anonymized_text.replace(ent.text, "LIEU")
        elif ent.label_ == "FAC":  # bien
            anonymized_text = anonymized_text.replace(ent.text, "UN LIEU")
    
    anonymized_text = re.sub(r'\b\d{2} \d{2} \d{2} \d{2} \d{2}\b', 'XX XX XX XX', anonymized_text)#tel
    anonymized_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'anonyme@example.com', anonymized_text)#mail
    anonymized_text = re.sub(r'\b\d{1} \d{2} \d{2} \d{2} \d{3} \d{3} \d{2}\b', 'XXX-XX-XXXX"', anonymized_text)#NSS
    anonymized_text = re.sub(r'\b\d{15}\b', 'XXX-XX-XXXX"', anonymized_text)#NSS
    anonymized_text = re.sub(r'\b[A-Z]{1}[0-9]{8}\b', 'X"', anonymized_text)#visa or passport
    
    return anonymized_text


original_text = """Hello Jean Dupont, your telephone number is 06 12 34 56 78 and
your email address is aida.sow@example.com. I'm muslim.I live in Bois d'arcy. I work for Orange France
I'm currently at 1 Avenue Pierrefitte-Sur Seinee. I'm 12. My NSS is 2 99 03 99 432 123 32. My passport number is A02134432"""
print(datetime.now())
anonymized_text = anonymize(original_text)
print("Texte anonymisé :\n", anonymized_text)
print(datetime.now())



