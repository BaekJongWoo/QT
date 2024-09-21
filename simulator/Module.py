from Qbit import Qbit
from Circuit import QuantumCircuit
import numpy as np

class Module():
    def __init__(self, idx:int) -> None:
        self.idx = idx

    def run(self, circuit: QuantumCircuit):
        qbit = circuit.input[self.idx]
        qbit.value = np.dot(self.gate, qbit.value)

class ControlledModule(Module):
    def __init__(self, control_idx:int, idx:int) -> None:
        self.control_idx = control_idx
        super().__init__(idx)

    def run(self, circuit: QuantumCircuit):
        control_qbit = circuit.input[self.control_idx]
        qbit = circuit.input[self.idx]
        
        value = np.dot(self.gate, np.concatenate(control_qbit.value, qbit.value))
        control_qbit.value, qbit.value = np.split(value, 2)

class X(Module):
    def __init__(self, idx: int) -> None:
        super().__init__(idx)
        self.gate = np.array([[0,1],[1,0]])

class Z(Module):
    def __init__(self, idx: int) -> None:
        super().__init__(idx)
        self.gate = np.array([[1,0],[0,-1]])

class Hadmard(Module):
    def __init__(self, idx: int) -> None:
        super().__init__(idx)
        self.gate = np.array([[1,1],[1,-1]]) / np.sqrt(2)

class CX(ControlledModule):
    def __init__(self, control_idx: int, idx: int) -> None:
        super().__init__(control_idx, idx)
        self.gate = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
        
class CZ(ControlledModule):
    def __init__(self, control_idx: int, idx: int) -> None:
        super().__init__(control_idx, idx)
        self.gate = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,-1]])