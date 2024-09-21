import numpy as np

class Qbit():
    def __init__(self) -> None:
        self.value = np.array([[1],[0]])

    def print(self):
        print(self.value)

if __name__ == "__main__":
    test = []
    test.append(Qbit())
    test[0].print()
    