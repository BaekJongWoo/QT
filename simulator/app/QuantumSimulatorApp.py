from __future__ import annotations
import pygame
from pygame import Rect
import sys
from logic.Circuit import QuantumCircuit
import logic.Gate as Gate
from ui.Module import Module
from ui.UIElement import *
import ui.COLOR as COLOR
import ui.CONFIG as CONFIG

class QuantumSimulatorApp:
    
    held_module_idx = -1
    held_pos = (0,0)

    def __init__(self, qbit_num):
        self.screen = pygame.display.set_mode((CONFIG.SCREEN_WIDTH, CONFIG.SCREEN_HEIGHT))
        pygame.display.set_caption("Quantum Circuit Simulator")

        fontPath = "simulator/src/D2Coding.ttf"
        self.baseFont = pygame.font.Font(fontPath, 15)
        self.moduleFont = pygame.font.Font(None, 24)

        self.qbit_num = qbit_num
        self.result: list[complex] = [0 for _ in range(2 ** qbit_num)]
        self.module_lines = [[] for _ in range(qbit_num)]

        self.modules: list[Module] = [
            Module("H", COLOR.BLUSHRED, Gate.H),
            Module("X", COLOR.SHADYSKY, Gate.X),
            Module("Y", COLOR.SHADYSKY, Gate.Y),
            Module("Z", COLOR.SHADYSKY, Gate.Z),
        ]

        y_button = 0
        y_circuit = CONFIG.BUTTONSECTIONHEIGHT
        y_util = CONFIG.BUTTONSECTIONHEIGHT + CONFIG.CIRCUITSECTIONHEIGHT

        button_margin = 10
        graph_section_percentage = 0.7

        self.ui_elements: list[BaseUI] = []
        self.AddUIElement(EraseButtonUI(self, Rect(button_margin, button_margin, 
                                                   80, CONFIG.BUTTONSECTIONHEIGHT - 2 * button_margin)))
        self.AddUIElement(QuantumCircuitUI(self, Rect(0,
                                                      y_circuit, 
                                                      CONFIG.SCREEN_WIDTH, 
                                                      CONFIG.CIRCUITSECTIONHEIGHT)))
        self.AddUIElement(ModuleSelectorUI(self, Rect(0,
                                                      y_util, 
                                                      CONFIG.SCREEN_WIDTH * (1-graph_section_percentage),
                                                      CONFIG.UTILITYSECTIONHRIGHT)))
        self.AddUIElement(ProbGraphUI(self, Rect(CONFIG.SCREEN_WIDTH * (1-graph_section_percentage), y_util,
                                                 CONFIG.SCREEN_WIDTH * graph_section_percentage, CONFIG.UTILITYSECTIONHRIGHT)))
        self.AddUIElement(HoldingModuleUI(self))

        self.Compute()

    def AddUIElement(self, newUIElement: BaseUI):
        self.ui_elements.append(newUIElement)

    def Compute(self):
        qc = QuantumCircuit(self.qbit_num)
        for line_idx, line in enumerate(self.module_lines):
            for module_idx in line:
                module:Module = self.modules[module_idx]
                qc.add(module.gate(line_idx))
        self.result = qc.run()                

    def AddModule(self, module_idx, line_idx):
        self.module_lines[line_idx].append(module_idx)
        self.Compute()

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