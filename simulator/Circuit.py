from Gate import *

class QuantumCircuit():
    def __init__(self, size):
        self.size = size
        self.value = self.getInit(size)
        self.gates = []
    
    def getInit(self, size):
        zeroket = np.array([[complex(1,0)],[complex(0,0)]])
        if size <= 1:
            return zeroket
        return np.kron(zeroket, self.getInit(size-1))

    def add(self, new_gate):
        new_gate.Generate(self)
        self.gates.append(new_gate)

    def run(self):
        for gate in self.gates:
            self.value = np.dot(gate.gate, self.value)

    def draw(self):
        pass


if __name__ == "__main__":
    qc = QuantumCircuit(3)
    qc.add(X(0))
    qc.add(Swap(0, 2))
    qc.run()
    print(qc.value)