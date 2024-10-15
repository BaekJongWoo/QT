import numpy as np

I = np.array([[1,0],[0,1]], dtype=complex)
ZERO = np.array([[1, 0], [0, 0]], dtype=complex)  # |0><0| projector
ONE = np.array([[0, 0], [0, 1]], dtype=complex)   # |1><1| projector

GATES = {
    "I": np.array([[1,0],[0,1]], dtype=complex),
    "X": np.array([[0,1],[1,0]]),
    "T": np.array([[1,0],[0, np.exp(complex(0,1)*np.pi/4)]]), # 45
    "S":np.array([[1,0],[0,complex(0,1)]]), # 90
    "Z": np.array([[1,0],[0,-1]]), #180
    "Y": np.array([[0, complex(0,-1)],[complex(0,1),0]]), # 270
    "H": np.array([[1,1],[1,-1]]) / np.sqrt(2),
    "R": np.array([[1,0],[0,1]])
}

def Generate(gate_keys):
    base = np.eye(2**len(gate_keys))

    mask = 1
    gate = 1
    for gate_key in gate_keys:
        if gate_key == "C":
            mask = np.kron(ONE, mask)
            gate = np.kron(ONE, gate)
        else:
            mask = np.kron(I, mask)
            gate = np.kron(GATES[gate_key], gate)
    
    return base - mask + gate
    
if __name__ == "__main__":
    print(Generate("XC"))


# class Swap(Gate):
#     def __init__(self, i, j) -> None:
#         self.i = i if i < j else j
#         self.j = j if i < j else i

#     def Generate(self, qc):
#         LOW = [
#             np.array([[1,0],[0,0]]),
#             np.array([[0,0],[1,0]]),
#             np.array([[0,1],[0,0]]),
#             np.array([[0,0],[0,1]]),
#         ]
#         HIGH = [
#             np.array([[1,0],[0,0]]),
#             np.array([[0,1],[0,0]]),
#             np.array([[0,0],[1,0]]),
#             np.array([[0,0],[0,1]]),
#         ]
#         I = np.array([[1,0],[0,1]])

#         gate = 0
#         for phase in range(4):
#             quater_gate = 1
#             for idx in range(qc.size):
#                 if (idx == self.i):
#                     quater_gate = np.kron(LOW[phase], quater_gate)
#                 elif (idx == self.j):
#                     quater_gate = np.kron(HIGH[phase], quater_gate)
#                 else:
#                     quater_gate = np.kron(I, quater_gate)
#             gate += quater_gate

#         self.gate = gate