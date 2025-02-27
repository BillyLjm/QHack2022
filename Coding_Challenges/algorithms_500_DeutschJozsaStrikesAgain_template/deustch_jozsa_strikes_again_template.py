#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def deutsch_jozsa(fs):
    """Function that determines whether four given functions are all of the same type or not.

    Args:
        - fs (list(function)): A list of 4 quantum functions. Each of them will accept a 'wires' parameter.
        The first two wires refer to the input and the third to the output of the function.

    Returns:
        - (str) : "4 same" or "2 and 2"
    """

    # QHACK #

    dev = qml.device("default.qubit", wires=5, shots=1)

    @qml.qnode(dev)
    def circuit():
        """Implements the modified Deutsch Jozsa algorithm
        Checks if fs[1] is of similar type to fs[2] and fs[3]
        by applying each pair of oracles together
        """

        # Insert any pre-oracle processing here
        qml.PauliX(4)
        for i in range(5):
            qml.Hadamard(i)

        # Apply oracle pairs
        fs[1](wires=(0,1,4)) # 1st pair
        fs[2](wires=(0,1,4))
        fs[1](wires=(2,3,4)) # 2nd pair
        fs[3](wires=(2,3,4))

        # Insert any post-oracle processing here
        for i in range(4):
            qml.Hadamard(i)
        return qml.sample(wires=range(4))

    sample = circuit()
    if np.any(sample): # if any non-zeros
        return "2 and 2"
    else:
        return "4 same"

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    numbers = [int(i) for i in inputs]

    # Definition of the four oracles we will work with.

    def f1(wires):
        qml.CNOT(wires=[wires[numbers[0]], wires[2]])
        qml.CNOT(wires=[wires[numbers[1]], wires[2]])

    def f2(wires):
        qml.CNOT(wires=[wires[numbers[2]], wires[2]])
        qml.CNOT(wires=[wires[numbers[3]], wires[2]])

    def f3(wires):
        qml.CNOT(wires=[wires[numbers[4]], wires[2]])
        qml.CNOT(wires=[wires[numbers[5]], wires[2]])
        qml.PauliX(wires=wires[2])

    def f4(wires):
        qml.CNOT(wires=[wires[numbers[6]], wires[2]])
        qml.CNOT(wires=[wires[numbers[7]], wires[2]])
        qml.PauliX(wires=wires[2])

    output = deutsch_jozsa([f1, f2, f3, f4])
    print(f"{output}")
