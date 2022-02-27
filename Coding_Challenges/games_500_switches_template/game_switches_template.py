#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def switch(oracle):
    """Function that, given an oracle, returns a list of switches that work by executing a
    single circuit with a single shot. The code you write for this challenge should be completely
    contained within this function between the # QHACK # comment markers.

    Args:
        - oracle (function): oracle that simulates the behavior of the lights.

    Returns:
        - (list(int)): List with the switches that work. Example: [0,2].
    """

    dev = qml.device("default.qubit", wires=[0, 1, 2, "light"], shots=1)

    @qml.qnode(dev)
    def circuit():

        # QHACK #

        # initialise superposition of states
        for i in range(3):
            qml.Hadamard(wires=i)

        # You are allowed to place operations before and after the oracle without any problem.
        oracle()

        # interfere output into |0000> + |1101>, where (1) switches work
        for i in range(3):
            qml.Hadamard(wires=i)
        qml.Hadamard(wires="light")

        # QHACK #
        return qml.sample(wires=[0, 1, 2, "light"])

    # repeat circuit until ancilla "light" is 1
    sample = circuit()
    while sample[-1] == 0:
        sample = circuit()

    # QHACK #

    # Process the received sample and return the requested list.
    switches = []
    for i in range(3):
        if sample[i] == 1:
            switches.append(i)
    return switches

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    numbers = [int(i) for i in inputs]

    def oracle():
        for i in numbers:
            qml.CNOT(wires=[i, "light"])

    output = switch(oracle)
    print(*output, sep=",")
