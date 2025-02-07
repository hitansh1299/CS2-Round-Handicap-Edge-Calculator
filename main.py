import pandas as pd
import lightning as L
from data import datamodules, datasets
from models import lightning_baseline
from torch import nn, utils

baseline_model = nn.Sequential(
    nn.Linear(82, 32),
    nn.ReLU(),
    nn.Linear(32,16),
    nn.ReLU(),
    nn.Linear(16,1)
)

model = lightning_baseline.BaselineModel(baseline_model)
dataset = datasets.BaselineDataset2('data\\master_database.db','match_data')
datamodule = datamodules.BaselineDataModule(dataset)


train_loader = utils.data.DataLoader(datamodule)
trainer = L.Trainer(limit_train_batches=100, max_epochs=5, log_every_n_steps=1)
trainer.fit(model=model, train_dataloaders=datamodule)
