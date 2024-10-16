from __future__ import annotations
import pygame
from pygame import Rect
import sys
from static import Gate
from ui.Module import ControlledModule, Module
from ui.UIElement import *
import ui.COLOR as COLOR
import ui.CONFIG as CONFIG

import numpy as np

class QuantumSimulatorApp:
    
    held_module_key = "I"
    held_pos = (0,0)

    seleted_preset = ""

    def __init__(self, qbit_num):
        self.screen = pygame.display.set_mode((CONFIG.SCREEN_WIDTH, CONFIG.SCREEN_HEIGHT))
        pygame.display.set_caption("Quantum Circuit Simulator")

        fontPath = "simulator/src/D2Coding.ttf"
        self.baseFont = pygame.font.Font(fontPath, 15)
        self.moduleFont = pygame.font.Font(None, 24)

        self.max_module_per_line = 18
        self.qbit_num = qbit_num
        self.result: list[complex] = [0 for _ in range(2 ** qbit_num)]
        self.module_lines = np.full((self.max_module_per_line, qbit_num), "I", dtype="U2")

        self.modules: dict[str, Module] = {
            "H": Module("H", COLOR.BLUSHRED),
            "X": Module("X", COLOR.SHADYSKY),
            "T": Module("T", COLOR.YELLOW),
            "S": Module("S", COLOR.YELLOW),
            "Z": Module("Z", COLOR.SHADYSKY),
            "Y": Module("Y", COLOR.SHADYSKY),
            "C": Module("C", COLOR.GRAY),
        }

        self.presets: dict[str, PresetModule] = {
            
        }

        y_circuit = 0
        y_button = CONFIG.CIRCUITSECTIONHEIGHT
        y_util = CONFIG.BUTTONSECTIONHEIGHT + CONFIG.CIRCUITSECTIONHEIGHT

        button_margin = 10
        graph_section_percentage = 0.7

        self.module_selecor = ModuleSelectorUI(self, Rect(0,
                                                      y_util, 
                                                      CONFIG.SCREEN_WIDTH * (1-graph_section_percentage),
                                                      CONFIG.UTILITYSECTIONHRIGHT))

        self.ui_elements: list[BaseUI] = []
        self.AddUIElement(QuantumCircuitUI(self, Rect(0,
                                                      y_circuit, 
                                                      CONFIG.SCREEN_WIDTH, 
                                                      CONFIG.CIRCUITSECTIONHEIGHT)))
        self.AddUIElement(BuildButtonUI(self, Rect(
            button_margin, y_button + button_margin,
            80, CONFIG.BUTTONSECTIONHEIGHT - 2 * button_margin
            )))
        self.AddUIElement(EraseButtonUI(self, Rect(
            CONFIG.SCREEN_WIDTH - 100, y_button + button_margin, 
            80, CONFIG.BUTTONSECTIONHEIGHT - 2 * button_margin
            )))
        self.AddUIElement(self.module_selecor)
        self.AddUIElement(ProbGraphUI(self, Rect(CONFIG.SCREEN_WIDTH * (1-graph_section_percentage), y_util,
                                                 CONFIG.SCREEN_WIDTH * graph_section_percentage, CONFIG.UTILITYSECTIONHRIGHT)))
        self.AddUIElement(HoldingModuleUI(self))

        self.Compute()

    @property
    def CurrentCircuit(self):
        if self.seleted_preset in self.presets:
            return self.presets[self.seleted_preset].gates
        else:
            return self.module_lines
        
    @CurrentCircuit.setter
    def CurrentCircuit(self, value):
        if self.seleted_preset in self.presets:
            self.presets[self.seleted_preset].gates = value
        else:
            self.module_lines = value

    def Clear(self):
        self.CurrentCircuit = np.full((self.max_module_per_line, self.qbit_num), "I", dtype="U2")

    def AddUIElement(self, newUIElement: BaseUI):
        self.ui_elements.append(newUIElement)

    def Compute(self):
        q_value = np.zeros((2**self.qbit_num, 1), dtype=complex)
        q_value[0] = 1
        for line in self.module_lines:
            if line[0] in self.presets:
                for preset_line in self.presets[line[0]].gates:
                    gate = Gate.Generate(preset_line)
                    q_value = np.dot(gate, q_value)
            else:
                gate = Gate.Generate(line)
                q_value = np.dot(gate, q_value)
        self.result = q_value

    def AddModule(self, idx, q_idx, module_key):
        if module_key in self.presets:
            self.CurrentCircuit[idx] = np.full((self.qbit_num), module_key, dtype="U2")
        else:
            self.CurrentCircuit[idx, q_idx] = module_key
        self.Compute()

    def RemoveModule(self, idx, q_idx):
        if self.CurrentCircuit[idx, q_idx] in self.presets:
            self.CurrentCircuit[idx] = np.full((self.qbit_num), "I", dtype="U2")
        else:
            self.CurrentCircuit[idx, q_idx] = "I"
        self.Compute()

    def ChangeQbitNum(self, num):
        self.qbit_num = num

    def AddQbit(self):
        self.ChangeQbitNum(self.qbit_num + 1)

    def SubQbit(self):
        self.ChangeQbitNum(self.qbit_num - 1)

    def AddPreset(self, name, preset_module):
        self.presets[name] = preset_module
        self.module_selecor.UpdateModuleRects()

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