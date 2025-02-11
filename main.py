import pandas as pd
import lightning as L
from data import datamodules, classification_datasets, regression_datasets
from models import classification_models
from models import regression_models
from torch import nn, utils
from lightning.pytorch.callbacks.early_stopping import EarlyStopping

# dataset = datasets.ClassificationDataset('data\\master_database.db','match_data')
dataset = regression_datasets.BaselineRegressionOverfitDataset('data\\master_database.db','match_data')
sample = dataset[0:2]
input_layer_size = len(sample[0])
output_layer_size = len(sample[1])

baseline_model = nn.Sequential(
    nn.Linear(input_layer_size, 4),
    # nn.ReLU(),
    # nn.Linear(4, 2),
    nn.ReLU(),
    nn.Linear(4,output_layer_size)
)
model = regression_models.BaselineRegressionModel(baseline_model)

datamodule = datamodules.BaselineDataModule(dataset)

trainer = L.Trainer(log_every_n_steps=20, max_epochs=100)
trainer.fit(model=model, datamodule=datamodule)
trainer.test(model, dataloaders=datamodule)
