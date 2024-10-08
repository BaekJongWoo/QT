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

    LINEMARGINLEFT = 50
    LINEMARGINRIGHT = 30

    MODULEMARGIN = 10

    def __init__(self, app, rect):
        super().__init__(app, rect)
        self.hovering_line_idx = -1
        self.mouse_pressed = False
    
    def Update(self, event):
        if self.App.held_module_idx != -1:
            mouse_pos = pygame.mouse.get_pos()
            self.hovering_line_idx = -1
            for i in range(self.App.qbit_num):
                min = (i + 0.5) * self.LINESPACE
                max = (i + 1.5) * self.LINESPACE
                if min < mouse_pos[1] < max:
                    self.hovering_line_idx = i
                    break
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouse_pressed = True

        if event.type == pygame.MOUSEBUTTONUP:
            if self.mouse_pressed:
                self.JustReleased()
            self.mouse_pressed = False

    def JustReleased(self):
        if self.App.held_module_idx != -1:
            self.App.AddModule(self.App.held_module_idx, self.hovering_line_idx)
        self.hovering_line_idx = -1

    def Draw(self):
        # draw base lines
        for i in range(self.App.qbit_num):
            y = (i + 1) * self.LINESPACE
            text = self.App.baseFont.render(f"q[{i}]", True, COLOR.BASETEXT)  # Text rendering
            text_rect = text.get_rect(center=(25, y))
            self.Screen.blit(text, text_rect)
            pygame.draw.line(self.Screen, COLOR.BASELINE, (self.LINEMARGINLEFT, y), (CONFIG.SCREEN_WIDTH - self.LINEMARGINRIGHT, y), width=self.LINEWIDTH)

        # draw measure line
        y = (self.App.qbit_num + 1) * self.LINESPACE
        pygame.draw.line(self.Screen, COLOR.BASELINE, (self.LINEMARGINLEFT, y - 2), (CONFIG.SCREEN_WIDTH - self.LINEMARGINRIGHT, y - 2), width=self.LINEWIDTH // 2)
        pygame.draw.line(self.Screen, COLOR.BASELINE, (self.LINEMARGINLEFT, y + 2), (CONFIG.SCREEN_WIDTH - self.LINEMARGINRIGHT, y + 2), width=self.LINEWIDTH // 2)

        # draw line modules
        for yi, line_modules in enumerate(self.App.module_lines):
            for xi, module_idx in enumerate(line_modules):
                x = self.LINEMARGINLEFT + self.MODULEMARGIN + xi * (CONFIG.MODULE_SIZE + self.MODULEMARGIN)
                y = (yi + 1) * self.LINESPACE - (CONFIG.MODULE_SIZE / 2)
                rect = Rect(x, y, CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE)
                self.App.modules[module_idx].Draw(self.Screen, self.App.moduleFont, rect)
        
        # draw hovering
        if self.hovering_line_idx != -1:
            xi = len(self.App.module_lines[self.hovering_line_idx])
            x = self.LINEMARGINLEFT + self.MODULEMARGIN + xi * (self.MODULEMARGIN + CONFIG.MODULE_SIZE)
            y = self.LINESPACE * (self.hovering_line_idx + 1) - CONFIG.MODULE_SIZE / 2
            rect = Rect(x, y, CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE)
            pygame.draw.rect(self.Screen, COLOR.WHITE, rect)

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
                    self.HeldUpdate(event)
                self.button_pressed = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.button_pressed = 0

    def HeldUpdate(self, event: Event):
        mouse_pos_rect = Rect(event.pos[0], event.pos[1], 1, 1)
        held_idx = self.get_hovering_module_idx(mouse_pos_rect)
        if held_idx != -1:
            module_rect = self.module_rects[held_idx]
            held_pos =  (mouse_pos_rect.x - module_rect.x,
                         mouse_pos_rect.y - module_rect.y)
            self.App.held_pos = held_pos
        
        self.App.held_module_idx = held_idx 

    def get_hovering_module_idx(self, mouse_pos_rect: Rect):
        for i, rect in enumerate(self.module_rects):
            if rect.contains(mouse_pos_rect):
                return i
        return -1

# Holding Module UI Class
class HoldingModuleUI(BaseUI):
    def __init__(self, app):
        super().__init__(app, None)

    def Update(self, event: Event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.App.held_module_idx = -1
    
    def Draw(self):
        if self.App.held_module_idx != -1:
            mx, my = pygame.mouse.get_pos()
            rect = Rect(mx - self.App.held_pos[0], my - self.App.held_pos[1], CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE)
            module = self.App.modules[self.App.held_module_idx]
            module.Draw(self.Screen, self.App.moduleFont, rect)