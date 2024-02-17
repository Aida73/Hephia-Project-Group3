import numpy as np
import pandas as pd
import json



def format_instruction(sample):
        PROMPT_TEMPLATE = "[INST] <<SYS>>\nUse the Input to provide a response from a question about medical domain.\n<</SYS>>\n\nInput:\n{user} [/INST]\n\nResponse: {assistant}"
        return {"text": PROMPT_TEMPLATE.format(user=sample["user"], assistant=sample["assistant"])}  

# train_dataset = train_dataset.apply(format_instruction, axis=1)
# val_dataset = val_dataset.apply(format_instruction, axis=1)

data = pd.read_csv('../data/data.csv')
data = data.apply(format_instruction, axis=1)

training_data = pd.read_csv('../data/training_data.csv')
training_data.to_json('../data/training_data.jsonl', orient='records', lines=True)

eval_data = pd.read_csv('../data/validating_data.csv')
eval_data.to_json('../data/eval_data.jsonl', orient='records', lines=True)

