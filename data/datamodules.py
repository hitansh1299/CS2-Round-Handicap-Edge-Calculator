import pandas as pd
from torch.utils.data import random_split, DataLoader
import torch
import sqlite3
import lightning as L


class BaselineTminus1RoundDataModule(L.LightningDataModule):
    def __init__(self, db: str, table: str):
        super().__init__()
        self.db = db
        self.table = table
        self.db_connection = sqlite3.connect(self.db)
        self.df = pd.read_sql(f'SELECT * FROM {self.table}', con=self.db_connection)
        self.df = self.df.reset_index()
        self.df = self.df.select_dtypes(include='number')
        self.train, self.val, self.test = random_split(self.df, [0.8,0.1,0.1], generator=torch.Generator().manual_seed(42))
        self.BATCH_SIZE = 32

    def train_dataloader(self):
        return DataLoader(self.train, batch_size=self.BATCH_SIZE, shuffle=True)
    
    def test_dataloader(self):
        return DataLoader(self.test, batch_size=self.BATCH_SIZE, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.val, batch_size=self.BATCH_SIZE, shuffle=True)

if __name__ == "__main__":
    BaselineTminus1RoundDataModule(db = "data\\master_database.db", table="match_data")