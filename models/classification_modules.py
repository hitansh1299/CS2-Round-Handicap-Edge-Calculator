import lightning as L
from torch import optim, nn, utils, Tensor, argmax
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from models._modules import BasicModule
class BaselineClassificationModule(BasicModule):
    def __init__(self, model: str | nn.Module, model_name: str = 'Generic_Regression_Model'):
        super(BaselineClassificationModule, self).__init__(model, model_name)
        self.loss = nn.functional.cross_entropy

    def plot_confusion_matrix(self, cm):
        fig, ax = plt.subplots(figsize=(16, 16))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_xlabel("Predicted labels")
        ax.set_ylabel("True labels")
        ax.set_title("Confusion Matrix")

        # Log confusion matrix to TensorBoard
        self.logger.experiment.add_figure("Confusion Matrix", fig)
        plt.close(fig)

    def on_test_batch_start(self, batch, batch_idx):
        if batch_idx == 0:
            loss, x_hat = self.__common_forward_step__(batch)
            print('Sample inference')
            y_pred = (x_hat == x_hat.max(dim=1, keepdim=True)[0]).float().cpu()
            cm = confusion_matrix(batch[1].argmax(axis=1).cpu(), y_pred.argmax(axis=1).cpu())
            self.plot_confusion_matrix(cm)
            print(cm)
            print('Loss: ',loss)

    
    
