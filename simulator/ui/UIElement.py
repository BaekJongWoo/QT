from __future__ import annotations
import pygame
from pygame import Rect, Surface
from pygame.event import Event
from ui import COLOR, CONFIG
import app.QuantumSimulatorApp as qs

class BaseUI:
    def __init__(self, app: qs.QuantumSimulatorApp, rect: Rect):
        self.App = app
        self.rect = rect

    def Update(self, event: Event):
        pass

    def Draw(self):
        pass

    @property
    def Screen(self):
        return self.App.screen

# Quantum Circuit UI Class
class QuantumCircuitUI(BaseUI):
    LINEWIDTH = 2
    LINESPACE = 40
    
    def Update(self, event):
        return super().Update(event)
    
    def Draw(self):
        circuit = self.App.qc
        for i in range(circuit.size):
            y = (i + 1) * self.LINESPACE
            text = self.App.baseFont.render(f"q[{i}]", True, COLOR.BASETEXT)  # Text rendering
            text_rect = text.get_rect(center=(25, y))
            self.Screen.blit(text, text_rect)
            pygame.draw.line(self.Screen, COLOR.BASELINE, (50, y), (CONFIG.SCREEN_WIDTH - 30, y), width=self.LINEWIDTH)

        y = (circuit.size + 1) * self.LINESPACE
        pygame.draw.line(self.Screen, COLOR.BASELINE, (50, y - 2), (CONFIG.SCREEN_WIDTH - 30, y - 2), width=self.LINEWIDTH // 2)
        pygame.draw.line(self.Screen, COLOR.BASELINE, (50, y + 2), (CONFIG.SCREEN_WIDTH - 30, y + 2), width=self.LINEWIDTH // 2)

# Module Selector UI Class
class ModuleSelectorUI(BaseUI):
    def __init__(self, app: qs.QuantumSimulatorApp, rect: Rect):
        super().__init__(app, rect)
        self.modules_per_line = self.rect.width // (CONFIG.MODULE_SIZE + 10)
        self.module_rects: list[Rect] = []
        self.initialize_modules()

        self.button_pressed = False

    def initialize_modules(self):
        for i in range(len(self.App.modules)):
            xi = i % self.modules_per_line
            yi = i // self.modules_per_line
            x = 10 + xi * (10 + CONFIG.MODULE_SIZE)
            y = self.rect.top + 10 + yi * (10 + self.modules_per_line)
            self.module_rects.append(Rect(x, y, CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE))

    def Draw(self):
        for i, module in enumerate(self.App.modules):
            rect = self.module_rects[i]
            module.Draw(self.App.screen, self.App.moduleFont, rect)

    def Update(self, event: Event):
        # if event.type == pygame.MOUSEMOTION:
        #     print(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.button_pressed == False: # clicked
                    self.App.GrabModuleIdx = self.get_hovering_module_idx(event.pos)
                self.button_pressed = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.button_pressed = 0

    def get_hovering_module_idx(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]
        for i, rect in enumerate(self.module_rects):
            if rect.contains(Rect(x,y,1,1)):
                return i
        return -1

# Holding Module UI Class
class HoldingModuleUI(BaseUI):
    def Update(self, event: Event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.App.GrabModuleIdx = -1
        
    def draw(self):
        border_rect = pygame.Rect(5, CONFIG.CIRCUIT_UI_HEIGHT + CONFIG.MODULE_SELECTOR_HEIGHT + 5, CONFIG.SCREEN_WIDTH - 10, CONFIG.HOLDING_MODULE_HEIGHT - 10)
        self.draw_border(border_rect)
        
        if self.held_module_idx != -1:
            mx, my = pygame.mouse.get_pos()
            rect = Rectangle(mx - self.held_pos[0], my - self.held_pos[1], CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE)
            module = self.modules[self.held_module_idx]
            module.Draw(self.screen, moduleFont, rect)