from __future__ import annotations
import pygame
from pygame import Rect
import sys

from static import COLOR, CONFIG

from app.CircuitManager import * 
from ui.UIElement import *
from ui.ButtonUI import *
from ui.BaseUI import BaseUI

import numpy as np

class QuantumSimulatorApp:
    
    held_module_key = ""
    held_pos = (0,0)

    seleted_pack_key = ""

    def __init__(self, qbit_num):
        self.screen = pygame.display.set_mode((CONFIG.SCREEN_WIDTH, CONFIG.SCREEN_HEIGHT))
        pygame.display.set_caption("Quantum Circuit Simulator")

        fontPath = "simulator/src/D2Coding.ttf"
        self.baseFont = pygame.font.Font(fontPath, 15)
        self.moduleFont = pygame.font.Font(None, 24)

        self.max_module_per_line = 18
        self.qbit_num = qbit_num
        self.result: list[complex] = [0 for _ in range(2 ** qbit_num)]

        self.cm = CircuitManager()
        y_circuit = 0
        y_button = CONFIG.CIRCUITSECTIONHEIGHT
        y_util = CONFIG.BUTTONSECTIONHEIGHT + CONFIG.CIRCUITSECTIONHEIGHT

        button_margin = 10
        graph_section_percentage = 0.7

        quantum_circuit = QuantumCircuitUI(self, Rect(0,
                                                      y_circuit, 
                                                      CONFIG.SCREEN_WIDTH, 
                                                      CONFIG.CIRCUITSECTIONHEIGHT))
        self.module_selector = ModuleSelectorUI(self, Rect(0,
                                                      y_util, 
                                                      CONFIG.SCREEN_WIDTH * (1-graph_section_percentage),
                                                      CONFIG.UTILITYSECTIONHRIGHT))

        add_preset_button = AddPresetButtonUI(self, Rect(
            button_margin, y_button + button_margin,
            80, CONFIG.BUTTONSECTIONHEIGHT - 2 * button_margin
            ))

        erase_button = EraseButtonUI(self, Rect(
            CONFIG.SCREEN_WIDTH - 100, y_button + button_margin, 
            80, CONFIG.BUTTONSECTIONHEIGHT - 2 * button_margin
            ))
        qbit_minus_button = QbitMinusButton(self, Rect(
            CONFIG.SCREEN_WIDTH / 2 - (button_margin + 40), y_button + button_margin,
            40, CONFIG.BUTTONSECTIONHEIGHT - 2 * button_margin
        ), "-")
        qbit_plus_button = QbitPlusButton(self, Rect(
            CONFIG.SCREEN_WIDTH / 2 + button_margin, y_button + button_margin,
            40, CONFIG.BUTTONSECTIONHEIGHT - 2 * button_margin
        ), "+")
        prob_graph = ProbGraphUI(self, Rect(CONFIG.SCREEN_WIDTH * (1-graph_section_percentage), y_util,
                                                 CONFIG.SCREEN_WIDTH * graph_section_percentage, CONFIG.UTILITYSECTIONHRIGHT))

        holding_module = HoldingModuleUI(self)

        self.ui_elements: list[BaseUI] = [
            quantum_circuit,
            add_preset_button,
            qbit_minus_button,
            qbit_plus_button,
            erase_button,
            self.module_selector,
            prob_graph,
            holding_module
        ]
        self.Compute()

    @property
    def CurrentCircuit(self):
        if self.seleted_pack_key == "":
            return self.cm.circuit
        else:
            return self.cm.packed_gate[self.seleted_pack_key]

    def Compute(self):
        q_value = np.zeros((2**self.cm.QbitNum, 1), dtype=complex)
        q_value[0] = 1
        gate = self.cm.Generate()
        self.result = gate * q_value
        print(f"=== Result === \n{self.result}")


    def AddModule(self, line_idx, q_idx, key):
        

    def RemoveModule(self, line_idx, q_idx):


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