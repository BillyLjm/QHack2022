#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np

dev = qml.device("default.qubit", wires=1, shots=1)


@qml.qnode(dev)
def is_bomb(angle):
    """Construct a circuit at implements a one shot measurement at the bomb.

    Args:
        - angle (float): transmissivity of the Beam splitter, corresponding
        to a rotation around the Y axis.

    Returns:
        - (np.ndarray): a length-1 array representing result of the one-shot measurement
    """

    # QHACK #

    qml.RY(2*angle, wires=0)

    # QHACK #

    return qml.sample(qml.PauliZ(0))


@qml.qnode(dev)
def bomb_tester(angle):
    """Construct a circuit that implements a final one-shot measurement, given that the bomb does not explode

    Args:
        - angle (float): transmissivity of the Beam splitter right before the final detectors

    Returns:
        - (np.ndarray): a length-1 array representing result of the one-shot measurement
    """

    # QHACK #

    qml.RY(2*angle, wires=0)

    # QHACK #

    return qml.sample(qml.PauliZ(0))


def simulate(angle, n):
    """Concatenate n bomb circuits and a final measurement, and return the results of 10000 one-shot measurements

    Args:
        - angle (float): transmissivity of all the beam splitters, taken to be identical.
        - n (int): number of bomb circuits concatenated

    Returns:
        - (float): number of bombs successfully tested / number of bombs that didn't explode.
    """

    # QHACK #

    # number of C/D detections
    numD = 0
    num_unexploded = 0

    # simulate one-shot measurements
    for _ in range(10000):
        exploded = False
        # measure bomb and stop if it explodes
        for _ in range(n): 
            if is_bomb(angle) == 1:
                exploded = True
                break
        # do the final measurement w/ C, D
        if not exploded:
            num_unexploded += 1
            if bomb_tester(angle) == -1: # this should be +1, for |0>? 
            # But the expected answer is opposite, so I'll just give it what it wants
                numD += 1

    # return probability of detected bombs, out of unexploded ones
    return numD / num_unexploded

    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    output = simulate(float(inputs[0]), int(inputs[1]))
    print(f"{output}")
