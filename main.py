import pandas as pd
import lightning as L
from data import datamodules, classification_datasets, regression_datasets
from models.json_to_torch import get_model
from models import classification_modules
from models import regression_modules
from torch import nn, utils, manual_seed
from lightning.pytorch.callbacks.early_stopping import EarlyStopping

def run():
    # dataset = datasets.ClassificationDataset('data\\master_database.db','match_data')
    dataset = regression_datasets.TMinusOneFullDataset('data\\master_database.db','match_data')
    datamodule = datamodules.BaselineDataModule(dataset)
    model = regression_modules.L1RegularizationRegressor(get_model(model_name="RegressionModelSmall", 
                                                                  models_file='models\\models.json', 
                                                                  input_dim=dataset.n_features, 
                                                                  output_dim=dataset.n_target))


    trainer = L.Trainer(log_every_n_steps=20, callbacks=EarlyStopping('validation_loss', min_delta=1e-5, patience=3))
    trainer.fit(model=model, datamodule=datamodule)
    trainer.test(model, dataloaders=datamodule)

if __name__ == '__main__':
    manual_seed(123)
    run()