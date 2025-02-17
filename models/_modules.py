import lightning as L
from torch import optim
from models import json_to_torch
import json
class BasicModule(L.LightningModule):
    def __init__(self, model, model_name: str):
        super(BasicModule, self).__init__()
        self.model = model
        self.model_name = model_name

    def on_train_start(self):
        logs_dir = self.logger.log_dir
        with open(logs_dir+'/hparams.json', 'w') as f:
            h_params = {'model_name': self.model_name}
            h_params['model'] = json_to_torch.convert_model_to_json(self.model)
            h_params['optimizer'] = str(self.optimizers())
            h_params['dataset'] = str(self.trainer.datamodule.dataset.__class__)
            h_params['columns'] = self.trainer.datamodule.dataset.df.columns.to_list()
            h_params['sample_data'] = self.trainer.datamodule.dataset.df.head(10).to_dict(orient='dict')
            json.dump(h_params, fp=f, indent=4) #Save model to json
    
    def training_step(self, batch):
        loss, x_hat = self.__common_forward_step__(batch)
        self.log("train_loss", loss)
        return loss

    def test_step(self, batch, batch_idx):
        loss, x_hat = self.__common_forward_step__(batch)
        self.log("test_loss", loss)
        return loss

    def validation_step(self, batch):   
        loss, x_hat = self.__common_forward_step__(batch)
        self.log("validation_loss", loss)
        return loss

    def __common_forward_step__(self, batch):
        X = batch[0]
        y = batch[1]

        x_hat = self.model(X)

        loss = self.loss(x_hat, y)
        return loss, x_hat

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=1e-3)
        return optimizer

    
    
