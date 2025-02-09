from sklearn.model_selection import train_test_split
from torch.utils.data import random_split, DataLoader, Dataset
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
import torch
from torch import Tensor
import sqlite3
import pandas as pd

class BaselineDataset(Dataset):
    '''
    Baseline dataset, only loads the db into a df and provides methods to get the data and length of the df
    '''
    def __init__(self, db: str, table:str):
        self.db = db
        self.table = table
        self.db_connection = sqlite3.connect(self.db)
        self.df = pd.read_sql(f'SELECT * FROM {self.table}', con=self.db_connection)
        
    
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, index):
        return Tensor(self.df.iloc[index].values)
    
def RegressionBasicDataset(BaselineDataset):
    pass


class ClassificationDataset(BaselineDataset):
    def __init__(self, db: str, table:str):
        super().__init__(db,table)
        self.df = self.prepare_data(self.df)
        
    def prepare_data(self, df: pd.DataFrame):      
        #Drop steamid and ticks as they are inconsequential
        steam_id_cols = df.columns[df.columns.str.startswith('steamid')]
        df = df.drop(columns=steam_id_cols)
        df = df.drop(columns='tick')
        

        #Convert team names into Label Encodings.
        team_clan_cols = df.columns[df.columns.str.startswith('team_clan')]
        df[team_clan_cols] = OrdinalEncoder().fit_transform(df[team_clan_cols].values)
        df = df.select_dtypes(include='number')
        # df.to_csv('temp_data.csv', index=False)
        
        #Convert round handicap to One Hot Encodings.
        column = 'round_handicap'
        one_hot = pd.get_dummies(df[column], prefix=column)
        df = df.drop(column, axis=1)
        df = pd.concat([df, one_hot], axis=1)
        return df
    
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, index):
        return Tensor(self.df.iloc[index].values)

    
if __name__ == "__main__":
    # BaselineTminus1RoundDataModule(db = "data\\master_database.db", table="match_data")
    dataset = ClassificationDataset(db = "data\\master_database.db", table="match_data")
    for i in dataset[0:5,:]:
        print(i)
