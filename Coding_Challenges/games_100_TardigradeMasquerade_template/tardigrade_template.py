import sys
import pennylane as qml
from pennylane import numpy as np


def second_renyi_entropy(rho):
    """Computes the second Renyi entropy of a given density matrix."""
    # DO NOT MODIFY anything in this code block
    rho_diag_2 = np.diagonal(rho) ** 2.0
    return -np.real(np.log(np.sum(rho_diag_2)))


def compute_entanglement(theta):
    """Computes the second Renyi entropy of circuits with and without a tardigrade present.

    Args:
        - theta (float): the angle that defines the state psi_ABT

    Returns:
        - (float): The entanglement entropy of qubit B with no tardigrade
        initially present
        - (float): The entanglement entropy of qubit B where the tardigrade
        was initially present
    """

    dev = qml.device("default.qubit", wires=3)

    # QHACK #

    @qml.qnode(dev)
    def circuit_without_tardigrade():
        """ Circuit without Tardigrade
        Prepares |010> + |100>
        """
        qml.Hadamard(wires=0)
        qml.PauliX(wires=1)
        qml.CNOT(wires=(0, 1))
        return qml.density_matrix(wires=1)

    @qml.qnode(dev)
    def circuit_with_tardigrade(theta):
        """ Circuit with Tardigrade 
        Prepares cos(theta/2) |010> + sin(theta/2) |001> + |100>
        """
        qml.Hadamard(wires=0)
        qml.CRY(np.pi + theta, wires=(0, 1))
        qml.CNOT(wires=(0,2))
        qml.CNOT(wires=(1,2))
        qml.PauliX(wires=0)
        return qml.density_matrix(wires=1)

    return (second_renyi_entropy(circuit_without_tardigrade()),
        second_renyi_entropy(circuit_with_tardigrade(theta)))

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    theta = np.array(sys.stdin.read(), dtype=float)

    S2_without_tardigrade, S2_with_tardigrade = compute_entanglement(theta)
    print(*[S2_without_tardigrade, S2_with_tardigrade], sep=",")
