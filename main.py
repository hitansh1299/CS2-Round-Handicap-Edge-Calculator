import pandas as pd
import lightning as L
from data import datamodules, datasets
from models import lightning_baseline
from torch import nn, utils
from lightning.pytorch.callbacks.early_stopping import EarlyStopping

baseline_model = nn.Sequential(
    nn.Linear(81, 32),
    nn.ReLU(),
    nn.Linear(32,16),
    nn.ReLU(),
    nn.Linear(16,1)
)

model = lightning_baseline.BaselineModel(baseline_model)
dataset = datasets.BaselineDataset2('data\\master_database.db','match_data')

datamodule = datamodules.BaselineDataModule(dataset)

# early_stop_callback = EarlyStopping(monitor="validation_loss", min_delta=0.005, patience=3, verbose=False, mode="max")


train_loader = utils.data.DataLoader(datamodule)
trainer = L.Trainer(limit_train_batches=100, log_every_n_steps=1, max_epochs=20)
trainer.fit(model=model, datamodule=datamodule)
trainer.test(model, dataloaders=datamodule)
