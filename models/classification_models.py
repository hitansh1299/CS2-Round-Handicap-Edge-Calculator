import lightning as L
from torch import optim, nn, utils, Tensor, argmax
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

class BaselineClassificationModel(L.LightningModule):
    def __init__(self, model):
        super(BaselineClassificationModel, self).__init__()
        self.model = model
        self.loss = nn.functional.cross_entropy

    def plot_confusion_matrix(self, cm):
        fig, ax = plt.subplots(figsize=(20, 16))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_xlabel("Predicted labels")
        ax.set_ylabel("True labels")
        ax.set_title("Confusion Matrix")

        # Log confusion matrix to TensorBoard
        self.logger.experiment.add_figure("Confusion Matrix", fig)
        plt.close(fig)

    
    def training_step(self, batch):
        loss, x_hat = self.__common_forward_step__(batch)
        # Logging to TensorBoard (if installed) by default
        self.log("train_loss", loss)
        return loss

    def test_step(self, batch, batch_idx):
        loss, x_hat = self.__common_forward_step__(batch)
        if batch_idx == 0:
            print('Sample inference')
            y_pred = (x_hat == x_hat.max(dim=1, keepdim=True)[0]).float().cpu()
            cm = confusion_matrix(batch[1].argmax(axis=1).cpu(), y_pred.argmax(axis=1).cpu())
            self.plot_confusion_matrix(cm)
            print(cm)
            
            print('Loss: ',loss)
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

    
    
