from sklearn.model_selection import train_test_split
from torch.utils.data import random_split, DataLoader, Dataset
import torch
from torch import Tensor
import sqlite3
import pandas as pd

class BaselineDataset(Dataset):
    '''
    Baseline Baseline data set for sanity testing. 
    has limited functionality. 
    only removes all nonnumeric features.
    '''
    def __init__(self, db: str, table:str):
        self.db = db
        self.table = table
        self.db_connection = sqlite3.connect(self.db)
        self.df = pd.read_sql(f'SELECT * FROM {self.table}', con=self.db_connection)
        self.df.to_csv('temp_data.csv')
        self.df = self.df.reset_index()
        self.df = self.df.select_dtypes(include='number')
        print(self.df)
        pass

    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, index):
        return Tensor(self.df.iloc[index].values)
