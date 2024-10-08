import numpy as np

class Qbit():
    Zeroket = [[complex(1,0)],[complex(0,0)]]
    OneKet = [[complex(1,0)],[complex(0,0)]]
    def __init__(self) -> None:
        self.value = np.array([[complex(1,0)],[complex(0,0)]])

    def print(self):
        print(self.value)

if __name__ == "__main__":
    test = []
    test.append(Qbit())
    test[0].print()
    