from __future__ import annotations
import pygame
from app.QuantumSimulatorApp import QuantumSimulatorApp

QBIT_NUM = 3

if __name__ == "__main__":
    pygame.init()
    app = QuantumSimulatorApp(QBIT_NUM)
    app.run()