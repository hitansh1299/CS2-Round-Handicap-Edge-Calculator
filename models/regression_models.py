import lightning as L
from torch import optim, nn, utils, Tensor, argmax
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

class BaselineRegressionModel(L.LightningModule):
    def __init__(self, model):
        super(BaselineRegressionModel, self).__init__()
        self.model = model
        self.loss = nn.functional.mse_loss

    def plot_regression(self, y_pred, y_true):
        fig, ax = plt.subplots(figsize=(16, 16))
        sns.regplot(x=y_pred, y=y_true, ax=ax)
        ax.set_xlabel("Predicted labels")
        ax.set_ylabel("True labels")
        ax.set_title("Regression Plot")

        # Log confusion matrix to TensorBoard
        self.logger.experiment.add_figure("Regression Plot", fig)
        plt.close(fig)

    
    def training_step(self, batch):
        loss, x_hat = self.__common_forward_step__(batch)
        # Logging to TensorBoard (if installed) by default
        self.log("train_loss", loss)
        return loss

    def test_step(self, batch, batch_idx):
        loss, x_hat = self.__common_forward_step__(batch)
        if batch_idx == 0:
            y_pred  = Tensor.numpy(x_hat, force=True)
            y = Tensor.numpy(batch[1], force=True)
            self.plot_regression(y_pred=y_pred, y_true=y)
            # print('Loss: ',loss)
        # Logging to TensorBoard (if installed) by default
        self.log("test_loss", loss)
        return loss

    def validation_step(self, batch):
        loss, x_hat = self.__common_forward_step__(batch)
        # Logging to TensorBoard (if installed) by default
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

    
    
