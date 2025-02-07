from torch.utils.data import random_split, DataLoader, Dataset
import lightning as L

class BaselineDataModule(L.LightningDataModule):
    def __init__(self, dataset: Dataset):
        super().__init__()
        self.train, self.test = random_split(dataset=dataset, lengths=[0.9,0.1])
        self.BATCH_SIZE = 32

    def train_dataloader(self):
        return DataLoader(self.train, batch_size=self.BATCH_SIZE, shuffle=True)
    
    def test_dataloader(self):
        return DataLoader(self.test, batch_size=self.BATCH_SIZE, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.val, batch_size=self.BATCH_SIZE, shuffle=True)
