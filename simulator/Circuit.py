from Module import *

class QuantumCircuit():
    def __init__(self, input_num, output_num):
        self.input = [Qbit() for _ in range(input_num)]
        self.output = [Qbit() for _ in range(output_num)]

        self.gates = []
    
    def add(self, new_modules):
        self.gates.append(new_modules)

    def run(self):
        for gate in self.gates:
            gate.run(self)

    def draw(self):
        pass


if __name__ == "__main__":
    qc = QuantumCircuit(1,0)
    qc.add(X(0))
    qc.add(Hadmard(0))
    qc.run()
    qc.input[0].print()
