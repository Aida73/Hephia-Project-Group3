import numpy as np
import pandas as pd


data = pd.read_csv('../data/data.csv')
train, validate, test = np.split(data.sample(frac=1, random_state=42),
                                 [int(.6*len(data)), int(.8*len(data))]
                                )


train.to_csv('../data/training_data.csv')
validate.to_csv('../data/validating_data.csv')
test.to_csv('../data/testing_data.csv')

