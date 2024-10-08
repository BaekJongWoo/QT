import pygame
import pygame.rect as Rect
import sys
from logic.Circuit import QuantumCircuit
from logic.Gate import *
from ui.Module import Module
from ui.UIElement import *
import ui.COLOR as COLOR
import ui.CONFIG as CONFIG

class QuantumSimulatorApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((CONFIG.SCREEN_WIDTH, CONFIG.SCREEN_HEIGHT))
        pygame.display.set_caption("Quantum Circuit Simulator")

        fontPath = "simulator/src/D2Coding.ttf"
        self.baseFont = pygame.font.Font(fontPath, 15)
        self.moduleFont = pygame.font.Font(None, 24)

        self.qc = QuantumCircuit(3)

        self.modules = [
            Module("H", COLOR.BLUSHRED),
            Module("X", COLOR.SHADYSKY),
            Module("Y", COLOR.SHADYSKY),
            Module("Z", COLOR.SHADYSKY),
        ]

        self.ui_elements: list[BaseUI] = []
        self.AddUIElement(QuantumCircuitUI(rect=Rect(0,0, CONFIG.SCREEN_WIDTH, CONFIG.CIRCUIT_UI_HEIGHT)))
        # self.AddUIElement(ModuleSelectorUI())
        # self.AddUIElement(HoldingModuleUI())

    def AddUIElement(self, newUIElement: BaseUI):
        newUIElement.bind(self)
        self.ui_elements.append(newUIElement)

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