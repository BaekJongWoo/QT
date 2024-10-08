import numpy as np

class Gate():
    I = np.array([[1,0],[0,1]], dtype=complex)
    def __init__(self, index, pauli) -> None:
        self.index = index
        self.pauli = pauli

    def Generate(self, qc):
        gate = 1
        for idx in range(qc.size):
            if (idx == self.index):
                gate = np.kron(self.pauli , gate)
            else:
                gate = np.kron(self.I, gate)
        
        self.gate = gate

class X(Gate):
    def __init__(self, index) -> None:
        X = np.array([[0,1],[1,0]])
        super().__init__(index, X)

class Y(Gate):
    def __init__(self, index) -> None:
        Y = np.array([[0, complex(0,-1)],[complex(0,1),0]])
        super().__init__(index, Y)

class Z(Gate):
    def __init__(self, index) -> None:
        Z = np.array([[1,0],[0,-1]])
        super().__init__(index, Z)

class H(Gate):
    def __init__(self, index) -> None:
        H = np.array([[1,1],[1,-1]]) / np.sqrt(2)
        super().__init__(index, H)

class R(Gate):
    def __init__(self, index, phase) -> None:
        G = np.array([[1, 0], [0, np.exp(phase*complex(0,1))]])
        super().__init__(index, G)

class S(Gate): 
    def __init__(self, index) -> None:
        S = np.array([[1,0],[0,complex(0,1)]]) 
        super().__init__(index, S)

class T(Gate): 
    def __init__(self, index) -> None:
        T = np.array([[1,0],[0, np.exp(complex(0,1)*np.pi/4)]]) 
        super().__init__(index, T)

class ControlledGate(Gate):
    ZERO = np.array([[1, 0], [0, 0]], dtype=complex)  # |0><0| projector
    ONE = np.array([[0, 0], [0, 1]], dtype=complex)   # |1><1| projector
    def __init__(self, control_index, target_index, pauli) -> None:
        self.control_index = [control_index] if isinstance(control_index, int) else control_index
        self.target_index = target_index
        self.pauli = pauli
    
    def Generate(self, qc):
        base = np.eye(2**qc.size)

        mask = 1
        gate = 1
        for idx in range(qc.size):
            if (idx in self.control_index):
                mask = np.kron(self.ONE, mask)
                gate = np.kron(self.ONE, gate)
            elif (idx == self.target_index):
                mask = np.kron(self.I, mask)
                gate = np.kron(self.pauli, gate)
            else:
                mask = np.kron(self.I, mask)
                gate = np.kron(self.I, gate)
        
        self.gate = base - mask + gate

class CX(ControlledGate):
    def __init__(self, control_index, target_index) -> None:
        X = np.array([[0,1],[1,0]])
        super().__init__(control_index, target_index, X)

class CY(ControlledGate):
    def __init__(self, control_index, target_index) -> None:
        Y = np.array([[0, complex(0,-1)],[complex(0,1),0]])
        super().__init__(control_index, target_index, Y)

class CZ(ControlledGate):
    def __init__(self, control_index, target_index) -> None:
        Z = np.array([[1,0],[0,-1]])
        super().__init__(control_index, target_index, Z)


class Swap(Gate):
    def __init__(self, i, j) -> None:
        self.i = i if i < j else j
        self.j = j if i < j else i

    def Generate(self, qc):
        LOW = [
            np.array([[1,0],[0,0]]),
            np.array([[0,0],[1,0]]),
            np.array([[0,1],[0,0]]),
            np.array([[0,0],[0,1]]),
        ]
        HIGH = [
            np.array([[1,0],[0,0]]),
            np.array([[0,1],[0,0]]),
            np.array([[0,0],[1,0]]),
            np.array([[0,0],[0,1]]),
        ]
        I = np.array([[1,0],[0,1]])

        gate = 0
        for phase in range(4):
            quater_gate = 1
            for idx in range(qc.size):
                if (idx == self.i):
                    quater_gate = np.kron(LOW[phase], quater_gate)
                elif (idx == self.j):
                    quater_gate = np.kron(HIGH[phase], quater_gate)
                else:
                    quater_gate = np.kron(I, quater_gate)
            gate += quater_gate

        self.gate = gate