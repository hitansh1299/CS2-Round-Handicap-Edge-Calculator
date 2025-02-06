import lightning as L
from torch import optim, nn, utils, Tensor

class BaselineModel(L.LightningModule):
    def __init__(self, model):
        super(BaselineModel, self).__init__()
        self.model = model
    
    def training_step(self, batch, batch_idx):
        X = batch[:,:-1]
        y = batch[:,-1]
        
        x_hat = self.model(X)

        loss = nn.functional.mse_loss(x_hat, X)
        # Logging to TensorBoard (if installed) by default
        self.log("train_loss", loss)
        return loss

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=1e-3)
        return optimizer

