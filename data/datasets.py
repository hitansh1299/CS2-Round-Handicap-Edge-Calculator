from torch.utils.data import Dataset
import sqlite3
import pandas as pd
import torch
class BasicDataset(Dataset):
    '''
    Baseline dataset, only loads the db into a df and provides methods to get length of the df
    '''
    def __init__(self, db: str, table:str):
        self.db = db
        self.table = table
        self.db_connection = sqlite3.connect(self.db)
        self.df: pd.DataFrame = pd.read_sql(f'SELECT * FROM {self.table}', con=self.db_connection)
        self.df = self.prepare_data(self.df)
        self.n_target = len(self.df.columns[self.df.columns.str.startswith('round_handicap')]) #TODO: Very shoddy solution, please fix to something more stable
        self.n_features = self.df.shape[1] - self.n_target #TODO: Again a very shabby solution, please create something more concrete
        self.n_rows = self.df.shape[0]

        
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, index):
        #NOTE Can be further optiimzed for better performance
        if not type(index) is slice:
            index = slice(index,index + 1)
        df = self.df.iloc[index]
        y_cols = df.columns[df.columns.str.startswith('round_handicap')]
        df_y = df[y_cols]
        df_X = df.drop(columns=y_cols)
        return torch.from_numpy(df_X.values[0]).to(torch.float32), torch.from_numpy(df_y.values[0]).to(torch.float32)
    