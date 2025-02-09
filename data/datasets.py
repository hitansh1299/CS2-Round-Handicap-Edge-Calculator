from sklearn.model_selection import train_test_split
from torch.utils.data import random_split, DataLoader, Dataset
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
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
        # print(self.df)

    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, index):
        return Tensor(self.df.iloc[index].values)

class BaselineDataset2(Dataset):
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
        self.df = self.prepare_data(self.df)
        

    def prepare_data(self, df: pd.DataFrame):      
        steam_id_cols = df.columns[df.columns.str.startswith('steamid')]
        
        df = df.drop(columns=steam_id_cols)
        df = df.drop(columns='tick')
        team_clan_cols = df.columns[df.columns.str.startswith('team_clan')]
        
        df[team_clan_cols] = OrdinalEncoder().fit_transform(df[team_clan_cols].values)
        df = df.select_dtypes(include='number')
        df.to_csv('temp_data.csv', index=False)
        return df
    
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, index):
        return Tensor(self.df.iloc[index].values)
    
if __name__ == "__main__":
    # BaselineTminus1RoundDataModule(db = "data\\master_database.db", table="match_data")
    dataset = BaselineDataset(db = "data\\master_database.db", table="match_data")
    # for i in dataset:
    #     print(i)
    # for i in  
