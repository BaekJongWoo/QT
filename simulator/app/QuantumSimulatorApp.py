from __future__ import annotations
import pygame
from pygame import Rect
import sys
from logic.Circuit import QuantumCircuit
from logic.Gate import *
from ui.Module import Module
from ui.UIElement import *
import ui.COLOR as COLOR
import ui.CONFIG as CONFIG

class QuantumSimulatorApp:
    def __init__(self, qbit_num):
        self.screen = pygame.display.set_mode((CONFIG.SCREEN_WIDTH, CONFIG.SCREEN_HEIGHT))
        pygame.display.set_caption("Quantum Circuit Simulator")

        fontPath = "simulator/src/D2Coding.ttf"
        self.baseFont = pygame.font.Font(fontPath, 15)
        self.moduleFont = pygame.font.Font(None, 24)

        self.qbit_num = qbit_num
        self.held_module_idx = -1
        self.held_pos = (0,0)

        self.module_lines = [[] for _ in range(qbit_num)]

        self.modules: list[Module] = [
            Module("H", COLOR.BLUSHRED),
            Module("X", COLOR.SHADYSKY),
            Module("Y", COLOR.SHADYSKY),
            Module("Z", COLOR.SHADYSKY),
        ]

        self.ui_elements: list[BaseUI] = []
        self.AddUIElement(QuantumCircuitUI(self, Rect(0,
                                                      0, 
                                                      CONFIG.SCREEN_WIDTH, 
                                                      CONFIG.SCREEN_HEIGHT * 0.5)))
        self.AddUIElement(ModuleSelectorUI(self, Rect(0,
                                                      CONFIG.SCREEN_HEIGHT * 0.5, 
                                                      CONFIG.SCREEN_WIDTH * 0.2,
                                                      CONFIG.SCREEN_HEIGHT * 0.5)))
        self.AddUIElement(HoldingModuleUI(self))

    def AddUIElement(self, newUIElement: BaseUI):
        self.ui_elements.append(newUIElement)

    def AddModule(self, module_idx, line_idx):
        self.module_lines[line_idx].append(module_idx)

    def run(self):
        while True:
            self.update()
            self.draw()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for ui_element in self.ui_elements:
                ui_element.Update(event)

    def draw(self):        
        self.screen.fill(COLOR.BACKGROUND)
        
        for ui_element in self.ui_elements:
            ui_element.Draw()

        pygame.display.flip()