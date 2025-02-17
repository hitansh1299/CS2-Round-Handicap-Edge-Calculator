import pandas as pd
import lightning as L
from data import datamodules, classification_datasets, regression_datasets
from models.json_to_torch import get_model
from models import classification_modules
from models import regression_modules
from torch import nn, utils
from lightning.pytorch.callbacks.early_stopping import EarlyStopping

# dataset = datasets.ClassificationDataset('data\\master_database.db','match_data')
dataset = regression_datasets.BaselineRegressionOverfitDataset('data\\master_database.db','match_data')
sample = dataset[0:2]
input_layer_size = len(sample[0])
output_layer_size = len(sample[1])

model = regression_modules.BaselineRegressionModule(get_model(model_name="SimpleModel2", filename='models\\models.json'))

datamodule = datamodules.BaselineDataModule(dataset)

trainer = L.Trainer(log_every_n_steps=20, max_epochs=10)
trainer.fit(model=model, datamodule=datamodule)
trainer.test(model, dataloaders=datamodule)
