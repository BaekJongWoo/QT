import pygame
from pygame import Rect
from pygame.event import Event
from ui import COLOR, CONFIG
from app.QuantumSimulatorApp import QuantumSimulatorApp

LINEWIDTH = 2
LINESPACE = 40

class BaseUI:
    def __init__(self, rect: Rect):
        self.rect = rect

    def bind(self, app: QuantumSimulatorApp):
        self.App = app

    def Update(self, event: Event):
        pass

    def Draw(self):
        pass

    @property
    def Screen(self):
        return self.App.screen

# Quantum Circuit UI Class
class QuantumCircuitUI(BaseUI):
    def Update(self, event):
        return super().Update(event)
    
    def Draw(self):
        pygame.draw.rect(self.Screen, COLOR.WHITE, self.rect)

        circuit = self.App.qc

        for i in range(circuit.size):
            y = (i + 1) * CONFIG.LINESPACE
            text = self.App.baseFont.render(f"q[{i}]", True, COLOR.BASETEXT)  # Text rendering
            text_rect = text.get_rect(center=(25, y))
            self.Screen.blit(text, text_rect)
            pygame.draw.line(self.Screen, COLOR.BASELINE, (50, y), (CONFIG.SCREEN_WIDTH - 30, y), width=CONFIG.LINEWIDTH)

        y = (circuit.size + 1) * CONFIG.LINESPACE
        pygame.draw.line(self.Screen, COLOR.BASELINE, (50, y - 2), (CONFIG.SCREEN_WIDTH - 30, y - 2), width=CONFIG.LINEWIDTH // 2)
        pygame.draw.line(self.Screen, COLOR.BASELINE, (50, y + 2), (CONFIG.SCREEN_WIDTH - 30, y + 2), width=CONFIG.LINEWIDTH // 2)

# # Module Selector UI Class
# class ModuleSelectorUI(BaseUI):
#     def __init__(self, modules, screen, moduleFont):
#         super().__init__(screen)
#         self.modules = modules
#         self.moduleFont = moduleFont
#         self.module_rects = []
#         self.initialize_modules()

#     def initialize_modules(self):
#         for i in range(len(self.modules)):
#             xi = i % CONFIG.MODULES_PER_LINE
#             yi = i // CONFIG.MODULES_PER_LINE
#             x = 10 + xi * (10 + CONFIG.MODULE_SIZE)
#             y = CONFIG.CIRCUIT_UI_HEIGHT + 10 + yi * (10 + CONFIG.MODULES_PER_LINE)
#             self.module_rects.append(Rectangle(x, y, CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE))

#     def draw(self):
#         border_rect = pygame.Rect(5, CONFIG.CIRCUIT_UI_HEIGHT + 5, CONFIG.SCREEN_WIDTH - 10, CONFIG.MODULE_SELECTOR_HEIGHT - 10)
#         self.draw_border(border_rect)
        
#         for i, module in enumerate(self.modules):
#             rect = self.module_rects[i]
#             module.Draw(self.screen, self.moduleFont, rect)

#     def get_hovering_module_idx(self, mouse_pos):
#         for i, rect in enumerate(self.module_rects):
#             if rect.Contains(*mouse_pos):
#                 return i
#         return -1

# # Holding Module UI Class
# class HoldingModuleUI(BaseUI):
#     def __init__(self):
#         super().__init__(screen)
#         self.held_module_idx = -1
#         self.held_pos = (0, 0)

#     def update_holding(self, event, hovering_idx, module_rects):
#         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#             if hovering_idx != -1:
#                 rect = module_rects[hovering_idx]
#                 mx, my = pygame.mouse.get_pos()
#                 self.held_module_idx = hovering_idx
#                 self.held_pos = (mx - rect.x, my - rect.y)

#         elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
#             self.held_module_idx = -1

#     def draw(self):
#         border_rect = pygame.Rect(5, CONFIG.CIRCUIT_UI_HEIGHT + CONFIG.MODULE_SELECTOR_HEIGHT + 5, CONFIG.SCREEN_WIDTH - 10, CONFIG.HOLDING_MODULE_HEIGHT - 10)
#         self.draw_border(border_rect)
        
#         if self.held_module_idx != -1:
#             mx, my = pygame.mouse.get_pos()
#             rect = Rectangle(mx - self.held_pos[0], my - self.held_pos[1], CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE)
#             module = self.modules[self.held_module_idx]
#             module.Draw(self.screen, moduleFont, rect)