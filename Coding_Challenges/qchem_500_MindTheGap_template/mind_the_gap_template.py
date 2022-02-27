import sys
import pennylane as qml
from pennylane import numpy as np
from pennylane import hf

def ground_state_VQE(H):
    """Perform VQE to find the ground state of the H2 Hamiltonian.

    Args:
        - H (qml.Hamiltonian): The Hydrogen (H2) Hamiltonian

    Returns:
        - (float): The ground state energy
        - (np.ndarray): The ground state calculated through your optimization routine
    """

    # QHACK #

    dev = qml.device("default.qubit", wires=4)

    def ansatz(params):
        """ Prepares a ansatz
        Typical hardware-efficient ansatz
        Rotation on all qubits, and a ring CNOT for entangling
        """
        for i in range(4):
            qml.Rot(*params[i], wires=i)
        qml.CNOT(wires=(0,1))
        qml.CNOT(wires=(1,2))
        qml.CNOT(wires=(2,3))
        qml.CNOT(wires=(3,0))

    @qml.qnode(dev)
    def energy(params):
        """ Evaluate energy of ansatz """
        ansatz(params)
        return qml.expval(H)

    # Return state created
    @qml.qnode(dev)
    def state(params):
        """ Returns prepared ansatz """
        ansatz(params)
        return qml.state()

    # Minimise energy eigenvalue
    opt = qml.NesterovMomentumOptimizer()
    params = np.ones([4, 3])
    for _ in range(500):
        params, E = opt.step_and_cost(energy, params)

    return E, state(params)

    # QHACK #


def create_H1(ground_state, beta, H):
    """Create the H1 matrix, then use `qml.Hermitian(matrix)` to return an observable-form of H1.

    Args:
        - ground_state (np.ndarray): from the ground state VQE calculation
        - beta (float): the prefactor for the ground state projector term
        - H (qml.Hamiltonian): the result of hf.generate_hamiltonian(mol)()

    Returns:
        - (qml.Observable): The result of qml.Hermitian(H1_matrix)
    """

    # QHACK #

    H1_matrix = qml.utils.sparse_hamiltonian(H).toarray()
    H1_matrix += beta * np.outer(ground_state, np.conjugate(ground_state))
    return qml.Hermitian(H1_matrix, wires=range(4))

    # QHACK #


def excited_state_VQE(H1):
    """Perform VQE using the "excited state" Hamiltonian.

    Args:
        - H1 (qml.Observable): result of create_H1

    Returns:
        - (float): The excited state energy
    """

    # QHACK #

    dev = qml.device("default.qubit", wires=4)

    def ansatz(params):
        """ Prepares a ansatz
        Typical hardware-efficient ansatz
        Rotation on all qubits, and a ring CNOT for entangling
        """
        for i in range(4):
            qml.Rot(*params[i], wires=i)
        qml.CNOT(wires=(0,1))
        qml.CNOT(wires=(1,2))
        qml.CNOT(wires=(2,3))
        qml.CNOT(wires=(3,0))

    @qml.qnode(dev)
    def energy(params):
        """ Evaluate energy of ansatz """
        ansatz(params)
        return qml.expval(H1)

    # Return state created
    @qml.qnode(dev)
    def state(params):
        """ Returns prepared ansatz """
        ansatz(params)
        return qml.state()

    # Minimise energy eigenvalue
    opt = qml.NesterovMomentumOptimizer()
    params = np.ones([4, 3])
    for _ in range(500):
        params, E = opt.step_and_cost(energy, params)

    return E

    # QHACK #


if __name__ == "__main__":
    coord = float(sys.stdin.read())
    symbols = ["H", "H"]
    geometry = np.array([[0.0, 0.0, -coord], [0.0, 0.0, coord]], requires_grad=False)
    mol = hf.Molecule(symbols, geometry)

    H = hf.generate_hamiltonian(mol)()
    E0, ground_state = ground_state_VQE(H)

    beta = 15.0
    H1 = create_H1(ground_state, beta, H)
    E1 = excited_state_VQE(H1)

    answer = [np.real(E0), E1]
    print(*answer, sep=",")
