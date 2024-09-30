import numpy as np

from abc import ABC, abstractmethod

class Module(ABC):
    def __init__(self, idx:int, size:int) -> None:
        self.idx = idx
        self.size = size
        self.gate = self.Gate()

    @abstractmethod
    def Gate(self):
        pass
    

class X(Module):

    X = np.array([[0,1],[1,0]])
    I = np.array([[1,0],[0,1]])

    def Gate(self):
        gate = 1
        for idx in range(self.size):
            if (idx == self.idx):
                gate = np.kron(self.X , gate)
            else:
                gate = np.kron(self.I, gate)
        return gate

class Y(Module):

    Y = np.array([[0, complex(0,-1)],[complex(0,1),0]])
    I = np.array([[1,0],[0,1]])

    def Gate(self):
        gate = 1
        for idx in range(self.size):
            if (idx == self.idx):
                gate = np.kron(self.Y , gate)
            else:
                gate = np.kron(self.I, gate)
        return gate

class Z(Module):

    Z = np.array([[1,0],[0,-1]])
    I = np.array([[1,0],[0,1]])

    def Gate(self):
        gate=1
        for idx in range(self.size):
            if (idx == self.idx):
                gate = np.kron(self.Z , gate)
            else:
                gate = np.kron(self.I, gate)
        return gate

class Madamard(Module):

    H = np.array([[1,1],[1,-1]]) / np.sqrt(2)
    I = np.array([[1,0],[0,1]])

    def Gate(self):
        gate=1
        for idx in range(self.size):
            if (idx == self.idx):
                gate = np.kron(self.Z , gate)
            else:
                gate = np.kron(self.I, gate)
        return gate

if __name__ == "__main__":
    print(Y(0, 3).gate)
