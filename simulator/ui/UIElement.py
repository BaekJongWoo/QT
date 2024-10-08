from __future__ import annotations
import pygame
from pygame import Rect, Surface
from pygame.event import Event
from ui import COLOR, CONFIG
import app.QuantumSimulatorApp as qs
import app.EventHandler as EH 

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

class ButtonUI(BaseUI):
    is_hovering = False
    button_pressed = False

    def __init__(self, app, rect, text, font: pygame.font.Font,
                 color = COLOR.BLUSHRED, hoveringColor = COLOR.LIGHTRED, pressed_color = COLOR.WHITE):
        self.text = text
        self.font = font
        self.color = color
        self.hovering_color = hoveringColor
        self.pressed_color = pressed_color
        super().__init__(app, rect)

    def Update(self, event):
        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            if self.rect.contains(Rect(mx, my, 1, 1)):
                self.is_hovering = True
            else:
                self.is_hovering = False
                self.button_pressed = False

        if EH.IsLMBClicked(event) and self.is_hovering:
            self.button_pressed = True
        
        if EH.IsLMBReleased(event):
            self.button_pressed = False

    def Draw(self):
        color = self.color
        if self.button_pressed:
            color = self.pressed_color
        elif self.is_hovering:
            color = self.hovering_color
        pygame.draw.rect(self.Screen, color, self.rect)
        
        text = self.font.render(self.text, True, COLOR.BLACK)  # Text rendering
        text_rect = text.get_rect(center=self.rect.center)
        self.Screen.blit(text, text_rect)

class EraseButtonUI(ButtonUI):
    def __init__(self, app, rect):
        super().__init__(app, rect, "Erase", app.baseFont)

    def Update(self, event):
        if EH.IsLMBClicked(event) and self.is_hovering:
            self.App.module_lines = [[] for _ in range(self.App.qbit_num)]
            self.App.Compute()
        return super().Update(event)

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
                min = self.rect.y + (i + 0) * self.LINESPACE
                max = self.rect.y + (i + 1) * self.LINESPACE
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
            y = self.rect.y + (i + 0.5) * self.LINESPACE
            text = self.App.baseFont.render(f"q[{i}]", True, COLOR.BASETEXT)  # Text rendering
            text_rect = text.get_rect(center=(25, y))
            self.Screen.blit(text, text_rect)
            pygame.draw.line(self.Screen, COLOR.BASELINE, (self.LINEMARGINLEFT, y), (CONFIG.SCREEN_WIDTH - self.LINEMARGINRIGHT, y), width=self.LINEWIDTH)

        # draw measure line
        y = self.rect.y + (self.App.qbit_num + 0.5) * self.LINESPACE
        pygame.draw.line(self.Screen, COLOR.BASELINE, (self.LINEMARGINLEFT, y - 2), (CONFIG.SCREEN_WIDTH - self.LINEMARGINRIGHT, y - 2), width=self.LINEWIDTH // 2)
        pygame.draw.line(self.Screen, COLOR.BASELINE, (self.LINEMARGINLEFT, y + 2), (CONFIG.SCREEN_WIDTH - self.LINEMARGINRIGHT, y + 2), width=self.LINEWIDTH // 2)

        # draw line modules
        for yi, line_modules in enumerate(self.App.module_lines):
            for xi, module_idx in enumerate(line_modules):
                x = self.LINEMARGINLEFT + self.MODULEMARGIN + xi * (CONFIG.MODULE_SIZE + self.MODULEMARGIN)
                y = self.rect.y + (yi + 0.5) * self.LINESPACE - (CONFIG.MODULE_SIZE / 2)
                rect = Rect(x, y, CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE)
                self.App.modules[module_idx].Draw(self.Screen, self.App.moduleFont, rect)
        
        # draw hovering
        if self.hovering_line_idx != -1:
            xi = len(self.App.module_lines[self.hovering_line_idx])
            x = self.LINEMARGINLEFT + self.MODULEMARGIN + xi * (self.MODULEMARGIN + CONFIG.MODULE_SIZE)
            y = self.rect.y + self.LINESPACE * (self.hovering_line_idx + 0.5) - CONFIG.MODULE_SIZE / 2
            rect = Rect(x, y, CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE)
            pygame.draw.rect(self.Screen, COLOR.WHITE, rect)

# Module Selector UI Class
class ModuleSelectorUI(BaseUI):
    def __init__(self, app: qs.QuantumSimulatorApp, rect: Rect):
        super().__init__(app, rect)
        self.modules_per_line = self.rect.width // (CONFIG.MODULE_SIZE + 10)
        self.module_rects: list[Rect] = []
        self.initialize_modules()

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
        if EH.IsLMBClicked(event):
            self.HeldUpdate(event)

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

class ProbGraphUI(BaseUI):
    baseline_margin = 30
    graph_width = 10

    def __init__(self, app, rect):
        super().__init__(app, rect)

    def Draw(self):
        baseline_x_min = self.rect.left + self.baseline_margin
        baseline_x_max = self.rect.right - self.baseline_margin
        baseline_width = baseline_x_max - baseline_x_min
        baseline_y = self.rect.bottom - self.baseline_margin
        graph_max_height = self.rect.height - self.baseline_margin
        pygame.draw.line(self.Screen, COLOR.BASELINE, 
                         (baseline_x_min, baseline_y), 
                         (baseline_x_max, baseline_y),
                         2)
        for q_idx, value in enumerate(self.App.result):
            prob = value * value.conjugate()
            x = baseline_x_min + (q_idx + 0.5) * (baseline_width / len(self.App.result))
            
            qbit_text = format(q_idx, f'0{self.App.qbit_num}b')
            text = self.App.baseFont.render(f"|{qbit_text}⟩", True, COLOR.BASETEXT)  # Text rendering
            text_rect = text.get_rect(center=(x, self.rect.bottom - self.baseline_margin / 2))
            self.Screen.blit(text, text_rect)
            
            graph_height = graph_max_height * prob.real
            graph_top = self.rect.top + graph_max_height - graph_height
            graph_left = x - self.graph_width / 2

            pygame.draw.rect(self.Screen, COLOR.GRAPHBLUE, Rect(float(graph_left), float(graph_top),
                                                           float(self.graph_width), float(graph_height)))
            

            