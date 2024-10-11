from __future__ import annotations
import pygame
from pygame import Rect
import sys
from static import Gate
from ui.Module import Module
from ui.UIElement import *
import ui.COLOR as COLOR
import ui.CONFIG as CONFIG

import numpy as np

class QuantumSimulatorApp:
    
    held_module_key = "I"
    held_pos = (0,0)

    def __init__(self, qbit_num):
        self.screen = pygame.display.set_mode((CONFIG.SCREEN_WIDTH, CONFIG.SCREEN_HEIGHT))
        pygame.display.set_caption("Quantum Circuit Simulator")

        fontPath = "simulator/src/D2Coding.ttf"
        self.baseFont = pygame.font.Font(fontPath, 15)
        self.moduleFont = pygame.font.Font(None, 24)

        self.max_module_per_line = 10
        self.qbit_num = qbit_num
        self.result: list[complex] = [0 for _ in range(2 ** qbit_num)]
        self.module_lines = np.full((self.max_module_per_line, qbit_num), "I")

        self.modules: dict[Module] = {
            "H": Module("H", COLOR.BLUSHRED),
            "X": Module("X", COLOR.SHADYSKY),
            "Y": Module("Y", COLOR.SHADYSKY),
            "Z": Module("Z", COLOR.SHADYSKY),
            "R": Module("R", COLOR.YELLOW),
            "C": Module("C", COLOR.GRAY)
        }

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

    def Clear(self):
        self.module_lines = np.full((self.max_module_per_line, self.qbit_num), "I")

    def AddUIElement(self, newUIElement: BaseUI):
        self.ui_elements.append(newUIElement)

    def Compute(self):
        q_value = np.zeros((2**self.qbit_num, 1), dtype=complex)
        q_value[0] = 1
        for line in self.module_lines:
            gate = Gate.Generate(line)
            q_value = np.dot(gate, q_value)
        self.result = q_value

    def AddModule(self, idx, q_idx, module_key):
        self.module_lines[idx, q_idx] = module_key
        self.Compute()

    def RemoveModule(self, idx, q_idx):
        self.module_lines[idx, q_idx] = "I"
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