import lightning as L
from torch import optim, nn, utils, Tensor, argmax

class BaselineModel(L.LightningModule):
    def __init__(self, model):
        super(BaselineModel, self).__init__()
        self.model = model
    
    def training_step(self, batch, batch_idx):
        X = batch[:,:-1]
        y = batch[:,-1]
        
        x_hat = self.model(X)

        loss = nn.functional.mse_loss(x_hat, y)
        # Logging to TensorBoard (if installed) by default
        self.log("train_loss", loss)
        return loss
   
    # def test_step(self, batch, batch_idx):
    #     X = batch[:,:-1]
    #     y = batch[:,-1]

    #     # calculate acc
    #     labels_hat = argmax(out, dim=1)
    #     test_acc = sum(y == labels_hat).item() / (len(y) * 1.0)

    #     # log the outputs!
    #     self.log_dict({'test_loss': loss, 'test_acc': test_acc})

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=1e-3)
        return optimizer

