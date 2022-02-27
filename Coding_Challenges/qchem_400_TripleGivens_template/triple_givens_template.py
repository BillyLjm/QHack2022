import sys
import pennylane as qml
from pennylane import numpy as np

NUM_WIRES = 6


def triple_excitation_matrix(gamma):
    """The matrix representation of a triple-excitation Givens rotation.

    Args:
        - gamma (float): The angle of rotation

    Returns:
        - (np.ndarray): The matrix representation of a triple-excitation
    """

    # QHACK #

    i, j = 7, 56 # index for |000111>, |111000>
    matrix = np.eye(2**6) # make matrix
    matrix[i,i] = np.cos(gamma/2)
    matrix[j,j] = np.cos(gamma/2)
    matrix[i,j] = -np.sin(gamma/2)
    matrix[j,i] = np.sin(gamma/2)
    return matrix

    # QHACK #


dev = qml.device("default.qubit", wires=6)


@qml.qnode(dev)
def circuit(angles):
    """Prepares the quantum state in the problem statement and returns qml.probs

    Args:
        - angles (list(float)): The relevant angles in the problem statement in this order:
        [alpha, beta, gamma]

    Returns:
        - (np.tensor): The probability of each computational basis state
    """

    # QHACK #

    # Prepare -|001011>
    qml.PauliX(wires=2)
    qml.PauliX(wires=4)
    qml.PauliX(wires=5)
    qml.PauliZ(wires=2)

    # Exchange excitations
    qml.SingleExcitation(angles[0], wires=(1,4)) # Rotate |001011> -> |011001>
    qml.DoubleExcitation(3*np.pi + angles[1], wires=(0,1,4,5)) # Rotate |001011> -> |111000>
    qml.QubitUnitary(triple_excitation_matrix(angles[2]), wires=(0,1,2,3,4,5)) # Rotate |111000> -> |000111>

    # QHACK #

    return qml.probs(wires=range(NUM_WIRES))


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = np.array(sys.stdin.read().split(","), dtype=float)
    probs = circuit(inputs).round(6)
    print(*probs, sep=",")
