import pandas as pd 
import os
from pathlib import Path



def merge_data():
    list_df = []
    for file in Path('./data').iterdir():
        if Path(file).name.split('.')[0]!='data':
            list_df.append(pd.read_csv(os.path.join(('./data'),Path(file).name)))
            print(Path(file).name)
    final = pd.concat(list_df)
    final.to_csv('./data/models_results.csv',encoding='utf-8', index=False)


if __name__ == "__main__":
    merge_data()
