from torch.utils.data import random_split, DataLoader, Dataset
import lightning as L
from datasets import *



class BaselineTminus1RoundDataModule(L.LightningDataModule):
    def __init__(self, db: str, table: str):
        super().__init__()
        dataset = BaselineDataset(db, table)
        self.train, self.test = random_split(dataset=dataset, lengths=[0.9,0.1])
        self.BATCH_SIZE = 32

    def train_dataloader(self):
        return DataLoader(self.train, batch_size=self.BATCH_SIZE, shuffle=True)
    
    def test_dataloader(self):
        return DataLoader(self.test, batch_size=self.BATCH_SIZE, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.val, batch_size=self.BATCH_SIZE, shuffle=True)

if __name__ == "__main__":
    # BaselineTminus1RoundDataModule(db = "data\\master_database.db", table="match_data")
    dataset = BaselineDataset(db = "data\\master_database.db", table="match_data")
    # for i in  
