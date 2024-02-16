import numpy as np
import pandas as pd
import json


# data = pd.read_csv('../data/data.csv')
# train, validate, test = np.split(data.sample(frac=1, random_state=42),
#                                  [int(.6*len(data)), int(.8*len(data))]
#                                 )


# train.to_csv('../data/training_data.csv')
# validate.to_csv('../data/validating_data.csv')
# test.to_csv('../data/testing_data.csv')
# def format_instruction(sample):
#         PROMPT_TEMPLATE = "[INST] <<SYS>>\nUse the Input to provide a response from a question about medical domain.\n<</SYS>>\n\nInput:\n{user} [/INST]\n\nResponse: {assistant}"
#         return {"text": PROMPT_TEMPLATE.format(user=sample["user"], assistant=sample["assistant"])}  

training_data = pd.read_csv('../data/training_data.csv')
#data = data.apply(format_instruction, axis=1)
training_data.to_json('../data/training_data.jsonl', orient='records', lines=True)
# train_dataset = pd.read_csv('../data/training_data.csv')
# val_dataset = pd.read_csv('../data/validating_data.csv')

eval_data = pd.read_csv('../data/validating_data.csv')
#data = data.apply(format_instruction, axis=1)
eval_data.to_json('../data/eval_data.jsonl', orient='records', lines=True)


# train_dataset = train_dataset.apply(format_instruction, axis=1)
# val_dataset = val_dataset.apply(format_instruction, axis=1)

# train_dataset.to_json("train_dataset.jsonl", orient='records', lines=True)
#val_dataset.to_json("val_data.jsonl",orient='records', lines=True)

