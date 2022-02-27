import sys
import pennylane as qml
from pennylane import numpy as np
import pennylane.optimize as optimize

DATA_SIZE = 250


def square_loss(labels, predictions):
    """Computes the standard square loss between model predictions and true labels.

    Args:
        - labels (list(int)): True labels (1/-1 for the ordered/disordered phases)
        - predictions (list(int)): Model predictions (1/-1 for the ordered/disordered phases)

    Returns:
        - loss (float): the square loss
    """

    loss = 0
    for l, p in zip(labels, predictions):
        loss = loss + (l - p) ** 2

    loss = loss / len(labels)
    return loss


def accuracy(labels, predictions):
    """Computes the accuracy of the model's predictions against the true labels.

    Args:
        - labels (list(int)): True labels (1/-1 for the ordered/disordered phases)
        - predictions (list(int)): Model predictions (1/-1 for the ordered/disordered phases)

    Returns:
        - acc (float): The accuracy.
    """

    acc = 0
    for l, p in zip(labels, predictions):
        if abs(l - p) < 1e-5:
            acc = acc + 1
    acc = acc / len(labels)

    return acc


def classify_ising_data(ising_configs, labels):
    """Learn the phases of the classical Ising model.

    Args:
        - ising_configs (np.ndarray): 250 rows of binary (0 and 1) Ising model configurations
        - labels (np.ndarray): 250 rows of labels (1 or -1)

    Returns:
        - predictions (list(int)): Your final model predictions

    Feel free to add any other functions than `cost` and `circuit` within the "# QHACK #" markers 
    that you might need.
    """

    # QHACK #

    num_wires = ising_configs.shape[1] 
    dev = qml.device("default.qubit", wires=num_wires) 

    # Define a variational circuit below with your needed arguments and return something meaningful
    @qml.qnode(dev)
    def circuit(params, ising_config):
        """ Variational quantum circuit """
        # data encoding
        qml.BasisState(ising_config, wires=range(num_wires))

        # variational quantum circuit
        for i in range(len(params)):
            for j in range(num_wires):
                qml.Rot(*params[i][j], wires=j)
            for j in range(num_wires - 1):
                qml.CNOT(wires=(j, j+1))
            qml.CNOT(wires=(num_wires-1, 0))

        # Return NN parity of entire spin chain
        # parity = [qml.PauliZ(i) for i in range(num_wires)]
        # parity = qml.operation.Tensor(*parity)
        # return qml.expval(parity)

        # return [qml.expval(qml.PauliZ(i) @ qml.PauliZ(i+1)) for i in range(num_wires-1)]
        return [qml.expval(qml.PauliZ(i)) for i in range(num_wires)]

    def variational_classifier(params, bias, ising_config):
        """ Decodes the quantum circuit output into a classification """
        magnetisation = np.sum(circuit(params, ising_config))
        return magnetisation + bias

    # Define a cost function below with your needed arguments
    def cost(params, bias, X, Y):

        # QHACK #
        
        # Insert an expression for your model predictions here
        predictions = [variational_classifier(params, bias, x) for x in X]

        # QHACK #

        return square_loss(Y, predictions) # DO NOT MODIFY this line

    # optimize your circuit here
    opt = qml.NesterovMomentumOptimizer()
    batch_size = 5 # number of ising_configs to train on in each iter
    num_layers = 3 # number of mixing layers in variational quantum circuit
    params = np.ones([num_layers, num_wires, 3]) # initial guess
    bias = np.array(0.0) # initial guess
    for i in range(100): # iteratively optimise
        batch_index = np.random.randint(0, len(labels), (batch_size,))
        X = ising_configs[batch_index]
        Y = labels[batch_index]
        params, bias, _, _ = opt.step(cost, params, bias, X, Y)
    
    # make predictions w/ optimised circuit
    predictions = []
    for ising_config in ising_configs:
        predict = variational_classifier(params, bias, ising_config)
        predictions.append(int(np.sign(predict)))

    # QHACK #

    return predictions


if __name__ == "__main__":
    inputs = np.array(
        sys.stdin.read().split(","), dtype=int, requires_grad=False
    ).reshape(DATA_SIZE, -1)
    ising_configs = inputs[:, :-1]
    labels = inputs[:, -1]
    predictions = classify_ising_data(ising_configs, labels)
    print(*predictions, sep=",")
