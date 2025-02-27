#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml

graph = {
    0: [1],
    1: [0, 2, 3, 4],
    2: [1],
    3: [1],
    4: [1, 5, 7, 8],
    5: [4, 6],
    6: [5, 7],
    7: [4, 6],
    8: [4],
}


def n_swaps(cnot):
    """Count the minimum number of swaps needed to create the equivalent CNOT.

    Args:
        - cnot (qml.Operation): A CNOT gate that needs to be implemented on the hardware
        You can find out the wires on which an operator works by asking for the 'wires' attribute: 'cnot.wires'

    Returns:
        - (int): minimum number of swaps
    """

    # QHACK #
    # initialisation
    start, end = cnot.wires
    nswaps = 0 # number of swaps
    qubits = set(graph[start]) # number of qubits reachable with nswaps

    # breadth-first search
    while len(qubits) != 0:
        if end in qubits: # if qubit reached, return nswaps
            return nswaps
        else: # else, add another swap & see which qubits you reach
            for qubit in qubits.copy():
                qubits.update(graph[qubit])
            nswaps += 2 # swap back and forth

    # if impossible to link
    return None

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    output = n_swaps(qml.CNOT(wires=[int(i) for i in inputs]))
    print(f"{output}")
