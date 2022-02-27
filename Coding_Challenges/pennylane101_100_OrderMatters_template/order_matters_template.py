#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


def compare_circuits(angles):
    """Given two angles, compare two circuit outputs that have their order of operations flipped: RX then RY VERSUS RY then RX.

    Args:
        - angles (np.ndarray): Two angles

    Returns:
        - (float): | < \sigma^x >_1 - < \sigma^x >_2 |
    """

    # QHACK #

    # circuit 1: RX(1) -> RY(2) -> <X>
    dev1 = qml.device("default.qubit", wires=1)
    @qml.qnode(dev1)
    def circ1(params):
        qml.RX(params[0], wires=0)
        qml.RY(params[1], wires=0)
        return qml.expval(qml.PauliX(0))

    # circuit 2: RY(2) -> RX(1) -> <X>
    dev2 = qml.device("default.qubit", wires=1)
    @qml.qnode(dev2)
    def circ2(params):
        qml.RY(params[1], wires=0)
        qml.RX(params[0], wires=0)
        return qml.expval(qml.PauliX(0))

    # return difference
    return np.abs(circ1(angles) - circ2(angles))

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    angles = np.array(sys.stdin.read().split(","), dtype=float)
    output = compare_circuits(angles)
    print(f"{output:.6f}")
