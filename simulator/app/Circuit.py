import numpy as np

class QuantumCircuit():
    def __init__(self, qbit_num, line_num):
        self.circuit = np.full((line_num, qbit_num), "I", dtype="U2")
    
    @property
    def LineNum(self):
        return len(self.circuit)
    
    @property
    def QbitNum(self):
        return len(self.circuit[0])

    def AddBit(self):
        new = np.full((self.LineNum, 1), "I", dtype="U2")
        self.circuit = np.concatenate((self.circuit, new), axis=1)

    def SubBit(self):
        self.circuit = np.delete(self.circuit, -1, axis=1)

if __name__ == "__main__":
    qc = QuantumCircuit(3, 10)
    print(qc.circuit)
    qc.AddBit()
    print(qc.circuit)
    qc.SubBit()
    print(qc.circuit)