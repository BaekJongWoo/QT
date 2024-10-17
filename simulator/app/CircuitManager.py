import numpy as np

I = np.array([[1,0],[0,1]], dtype=complex)
ZERO = np.array([[1, 0], [0, 0]], dtype=complex)  # |0><0| projector
ONE = np.array([[0, 0], [0, 1]], dtype=complex)   # |1><1| projector

GATES = {
    "X": np.array([[0,1],[1,0]]),
    "T": np.array([[1,0],[0, np.exp(complex(0,1)*np.pi/4)]]), # 45
    "S":np.array([[1,0],[0,complex(0,1)]]), # 90
    "Z": np.array([[1,0],[0,-1]]), #180
    "Y": np.array([[0, complex(0,-1)],[complex(0,1),0]]), # 270
    "H": np.array([[1,1],[1,-1]]) / np.sqrt(2),
}


""" circuit example
I X I P0 I X
I I I  1 T C
I C H  2 C C
I I I I  I I
"""

def find_power_of_two(n):
    if n <= 0:
        return -1  # 2의 거듭제곱이 아니면 -1 반환
    count = 0
    while n > 1:
        if n % 2 != 0:
            return -1  # 2로 나누어지지 않으면 2의 거듭제곱이 아님
        n //= 2
        count += 1
    return count

class CircuitManager:
    def __init__(self, preset: dict[str, np.ndarray] = {}) -> None:
        self.packed_gate = preset
        self.circuit = np.array([["I"]], dtype="U2")

    def AddNewPack(self):
        new_pack_key = f"P{len(self.packed_gate)}"
        self.packed_gate[new_pack_key] = np.array([["I"]], dtype="U2")

    def GetLen(self, pack_key = "") -> int:
        if pack_key == "":
            return len(self.circuit)
        elif self.IsPackedGate(pack_key):
            return len(self.packed_gate[pack_key])
        else:
            raise KeyError(pack_key)

    def GetQbitNum(self, pack_key=""):
        if pack_key == "":
            return len(self.circuit[0])
        elif self.IsPackedGate(pack_key):
            return len(self.packed_gate[pack_key][0])
        else:
            raise KeyError(pack_key)

    def IsBaseGate(self, key: str) -> bool:
        return key in GATES

    def IsPackedGate(self, key:str) -> bool:
        return key in self.packed_gate

    def IsValidGateKey(self, key:str) -> bool:
        if self.IsBaseGate(key) or self.IsPackedGate(key) or key == 'C':
            return True
        else:
            return False

    def IsSubQbitValid(self, pack_key = ""):
        if pack_key == "":
            return len(self.circuit[0]) > 1 and np.all(self.circuit[:,-1] == "I")
        elif self.IsPackedGate(pack_key):
            return len(self.packed_gate[pack_key][0]) > 1 and np.all(self.packed_gate[pack_key][:,-1] == "I")
        else:
            raise KeyError(pack_key)

    def SubQbit(self, pack_key = ""):
        if pack_key == "":
            self.circuit = self.circuit[:,:-1]
        elif self.IsPackedGate(pack_key):
            self.packed_gate[pack_key] = self.packed_gate[pack_key][:,:-1]
        else:
            raise KeyError(pack_key)
    
    def AddQbit(self, pack_key = ""):
        if pack_key == "":
            new = np.full((self.GetLen(pack_key), 1), "I")
            self.circuit = np.concatenate((self.circuit, new), axis=1)
        elif self.IsPackedGate(pack_key):
            new = np.full((self.GetLen(pack_key), 1), "I")
            self.packed_gate[pack_key] = np.concatenate((self.packed_gate[pack_key], new), axis=1)
        else:
            raise KeyError(pack_key)

    def Generate(self, pack_key = ""):
        ret = 1
        circuit = self.circuit
        if self.IsPackedGate(pack_key):
            circuit = self.packed_gate[pack_key]
        for line in circuit:
            base = np.eye(2**len(line), dtype=complex)

            mask = 1
            gate = 1
            for key in line:
                if key == "I":
                    mask = np.kron(I, mask)
                    gate = np.kron(I, gate)
                elif key == "C":
                    mask = np.kron(ONE, mask)
                    gate = np.kron(ONE, gate)
                elif self.IsPackedGate(key):
                    mask = np.kron(I,mask)
                    sub_gate = self.Generate(key)
                    gate = np.kron(sub_gate, gate)
                elif key.isdigit():
                    mask = np.kron(I,mask)
                else:
                    mask = np.kron(I, mask)
                    gate = np.kron(GATES[key], gate)
            ret = np.dot((base - mask + gate), ret)
        return ret

if __name__ == "__main__":
    cm = CircuitManager()
    c = [
        ["H"],
        ["I"]
    ]
    cm.circuit = np.array(c)
    gate = cm.Generate()
    print(gate)

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