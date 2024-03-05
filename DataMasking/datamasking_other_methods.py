import spacy
from masked_ai import masker

def anonymize_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    print(doc)
    
    anonymized_text = " ".join([token.text if token.ent_type_ == "" else f"{{{ token.ent_type_ }}}" for token in doc])
    
    return anonymized_text


def replace_token(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    print(doc)
    
    anonymized_text = " ".join([token.text if token.ent_type_ == "" else f"{{token.ent_type_[0].lower()}}" for token in doc])
    
    return anonymized_text



#Using masked_ai: a new approach to mask data using AI
def masking_text():
    data = "My name is Adam and my IP address is 8.8.8.8. Now, write a one line poem:"
    masker = masker(data)
    print('Masked: ', masker.masked_data)


#Faker: A package Python that can be used to generate fake data
#anonymizedf: a package that can be used to mask data on dataset by selecting the columns 
#PII recognizer: A function to detect pii data and anonymize the pii entity in the text. This is a paid solution
