from torch import optim, nn, Tensor
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from models._modules import BasicModule
class BaselineRegressionModule(BasicModule):
    def __init__(self, model: str | nn.Module, model_name: str = 'Generic_Regression_Model'):
        super(BaselineRegressionModule, self).__init__(model, model_name)
        self.loss = nn.functional.mse_loss

    def plot_regression(self, y_pred, y_true):
        fig, ax = plt.subplots(figsize=(16, 16))
        sns.regplot(x=y_pred, y=y_true, ax=ax)
        ax.set_xlabel("Predicted labels")
        ax.set_ylabel("True labels")
        ax.set_title("Regression Plot")

        # Log confusion matrix to TensorBoard
        self.logger.experiment.add_figure("Regression Plot", fig)
        # plt.savefig('test_fig.png')
        fig.savefig('test_fig.png')
        plt.close(fig)

    def on_test_batch_start(self, batch, batch_idx):
        if batch_idx == 0:
            loss, x_hat = self.__common_forward_step__(batch)
            y_pred  = Tensor.numpy(x_hat, force=True)
            y = Tensor.numpy(batch[1], force=True)
            print(np.column_stack((y_pred,y)))
            self.plot_regression(y_pred=y_pred, y_true=y)
            print('Loss: ',loss)
    
