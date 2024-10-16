from __future__ import annotations
import pygame
from pygame import Rect, Surface
from pygame.event import Event
from pygame.font import Font

from ui.BaseUI import BaseUI
from static import COLOR, CONFIG
import app.QuantumSimulatorApp as qs
import static.EventHandler as EH 

import numpy as np

def DrawModule(surface: Surface, key: str, topLeftPos, font: Font, size: int = 1):
    color = COLOR.WHITE
    if key == "":
        color = COLOR.HOVERING_COLOR
    if key in COLOR.MODULE_COLOR:
        color = COLOR.MODULE_COLOR[key]
    size = (CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE * size)
    rect = Rect(topLeftPos, size)
    pygame.draw.rect(surface, color, rect)

    if key != "":
        text = font.render(key, True, COLOR.BLACK)  # Text rendering
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)

# Quantum Circuit UI Class
class QuantumCircuitUI(BaseUI):
    LINEWIDTH = 2
    LINESPACE = 40

    LINEMARGINLEFT = 50
    LINEMARGINRIGHT = 30

    MODULEMARGIN = 10

    def __init__(self, app, rect):
        super().__init__(app, rect)
        self.hovering_coord = (-1, -1)
        self.mouse_pressed = False
    
    def Update(self, event):

        mouse_pos = pygame.mouse.get_pos()
        target_pos = (mouse_pos[0] - self.App.held_pos[0] + CONFIG.MODULE_SIZE / 2, mouse_pos[1] - self.App.held_pos[1] + CONFIG.MODULE_SIZE / 2)

        for (xi,yi), value in np.ndenumerate(self.App.CurrentCircuit):
            x = self.rect.left + self.LINEMARGINLEFT + self.MODULEMARGIN + xi * (CONFIG.MODULE_SIZE + self.MODULEMARGIN)
            y = self.rect.top + (yi + 0.5) * self.LINESPACE - self.LINESPACE / 2
            rect = Rect(x, y, CONFIG.MODULE_SIZE + self.MODULEMARGIN, self.LINESPACE)
            if rect.contains(Rect(target_pos[0], target_pos[1], 1 ,1)):
                self.hovering_coord = (xi, yi)
                break
        else:
            self.hovering_coord = (-1, -1)
        
        if EH.IsLMBReleased(event):
            self.JustReleased()

        if EH.IsRMBClicked(event):
            self.DeleteHover()


    def JustReleased(self):
        if self.App.held_module_key != "" and self.hovering_coord != (-1, -1):
            self.App.AddModule(self.hovering_coord[0], self.hovering_coord[1], self.App.held_module_key)
        self.hovering_line_idx = ""
        self.hovering_coord = (-1, -1)

    def DeleteHover(self):
        if self.hovering_coord != (-1, -1):
            self.App.RemoveModule(self.hovering_coord[0], self.hovering_coord[1])

    def Draw(self):

        if self.App.seleted_pack_key != "":
            pygame.draw.rect(self.Screen, COLOR.WHITE, self.rect, 4)

        # draw base lines
        for i in range(self.CM.GetQbitNum()):
            y = self.rect.y + (i + 0.5) * self.LINESPACE
            text = self.App.baseFont.render(f"q[{i}]", True, COLOR.BASETEXT)  # Text rendering
            text_rect = text.get_rect(center=(25, y))
            self.Screen.blit(text, text_rect)
            pygame.draw.line(self.Screen, COLOR.BASELINE, (self.LINEMARGINLEFT, y), (CONFIG.SCREEN_WIDTH - self.LINEMARGINRIGHT, y), width=self.LINEWIDTH)

        # draw measure line
        y = self.rect.y + (self.App.qbit_num + 0.5) * self.LINESPACE
        pygame.draw.line(self.Screen, COLOR.BASELINE, (self.LINEMARGINLEFT, y - 2), (CONFIG.SCREEN_WIDTH - self.LINEMARGINRIGHT, y - 2), width=self.LINEWIDTH // 2)
        pygame.draw.line(self.Screen, COLOR.BASELINE, (self.LINEMARGINLEFT, y + 2), (CONFIG.SCREEN_WIDTH - self.LINEMARGINRIGHT, y + 2), width=self.LINEWIDTH // 2)

        # control line
        for xi, line in enumerate(self.App.CurrentCircuit):
            if "C" in line:
                x = self.rect.left + self.LINEMARGINLEFT + self.MODULEMARGIN / 2 + xi * (CONFIG.MODULE_SIZE + self.MODULEMARGIN) + CONFIG.MODULE_SIZE / 2
                y_min = self.rect.top + (0.5) * self.LINESPACE
                y_max = self.rect.top + (self.App.qbit_num - 0.5) * self.LINESPACE
                pygame.draw.line(self.Screen, COLOR.GRAY, (x, y_min), (x, y_max), 2)

        # draw line modules
        for xi, line in enumerate(self.App.CurrentCircuit):
            for yi, module_key in enumerate(line):
                if module_key == "I":
                    continue
                if module_key in self.App.modules:
                    x = self.LINEMARGINLEFT + self.MODULEMARGIN / 2 + xi * (CONFIG.MODULE_SIZE + self.MODULEMARGIN)
                    y = self.rect.y + (yi + 0.5) * self.LINESPACE - (CONFIG.MODULE_SIZE / 2)
                    rect = Rect(x, y, CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE)
                    self.App.modules[module_key].Draw(self.Screen, self.App.moduleFont, rect)

                    if "C" in line:
                        pygame.draw.rect(self.Screen, COLOR.GRAY, rect, 3)

                elif yi == 0:
                    x = self.LINEMARGINLEFT + self.MODULEMARGIN / 2 + xi * (CONFIG.MODULE_SIZE + self.MODULEMARGIN)
                    y = self.rect.top + (0.5) * self.LINESPACE - CONFIG.MODULE_SIZE / 2
                    height = self.App.qbit_num * (CONFIG.MODULE_SIZE + self.MODULEMARGIN) - self.MODULEMARGIN
                    rect = Rect(x,y,CONFIG.MODULE_SIZE, height)
                    self.App.presets[module_key].Draw(self.Screen, self.App.baseFont, rect)

        # draw hovering
        if self.App.held_module_key != "":
            if self.hovering_coord != (-1, -1):
                xi = self.hovering_coord[0]
                yi = self.hovering_coord[1]
                x = self.rect.left + self.LINEMARGINLEFT + self.MODULEMARGIN / 2 + xi * (CONFIG.MODULE_SIZE + self.MODULEMARGIN)
                if self.App.held_module_key in self.App.modules:
                    y = self.rect.top + (yi + 0.5) * self.LINESPACE - CONFIG.MODULE_SIZE / 2
                    rect = Rect(x,y,CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE)
                else:
                    y = self.rect.top + (0.5) * self.LINESPACE - CONFIG.MODULE_SIZE / 2
                    height = self.App.qbit_num * (CONFIG.MODULE_SIZE + self.MODULEMARGIN) - self.MODULEMARGIN
                    rect = Rect(x,y,CONFIG.MODULE_SIZE, height)
                pygame.draw.rect(self.Screen, COLOR.GRAY, rect)

    def GetModuleCenter(self, xi, yi):
        x = self.LINEMARGINLEFT + self.MODULEMARGIN + xi * (self.MODULEMARGIN + CONFIG.MODULE_SIZE)
        y = self.rect.y + self.LINESPACE * (yi + 1) - CONFIG.MODULE_SIZE / 2
        return (x, y)

# Module Selector UI Class
class ModuleSelectorUI(BaseUI):
    margin = 10

    def __init__(self, app: qs.QuantumSimulatorApp, rect: Rect):
        super().__init__(app, rect)
        self.modules_per_line = self.rect.width // (CONFIG.MODULE_SIZE + 10)
        self.keyRectDict = {}

    def GetKeyRectDict(self) -> dict[str, Rect]:
        if list(self.keyRectDict.keys()) != self.CM.GetSelectableKeys():
            self.UpdateKeyRectDict()
        return self.keyRectDict

    def UpdateKeyRectDict(self):
        ret:dict[str, Rect] = {}
        for i, key in enumerate(self.CM.GetSelectableKeys()):
            xi = i % self.modules_per_line
            yi = i // self.modules_per_line
            x = self.rect.left + self.margin + xi * (self.margin + CONFIG.MODULE_SIZE)
            y = self.rect.top + self.margin + yi * (self.margin + CONFIG.MODULE_SIZE)
            rect = Rect(x, y, CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE)
            ret[key] = rect
        self.keyRectDict = ret

    def Draw(self):
        for key, rect in self.GetKeyRectDict().items():
            DrawModule(self.Screen, key, rect.topleft, self.App.moduleFont, size=1)

    def GetMouseHoveringModuleKey(self, mx, my) -> str:
        for key, rect in self.GetKeyRectDict().items():
            if rect.contains(Rect(mx, my, 1, 1)):
                return key
        return ""

    def Update(self, event: Event):
        if EH.IsLMBClicked(event):
            hovering_key = self.GetMouseHoveringModuleKey(event.pos[0], event.pos[1])
            if hovering_key != "":
                module_rect = self.GetKeyRectDict()[hovering_key]
                self.App.held_pos = (event.pos[0] - module_rect.x, event.pos[1] - module_rect.y)
                self.App.held_module_key = hovering_key
        
        if EH.IsRMBClicked(event):
            hovering_key = self.GetMouseHoveringModuleKey(event.pos[0], event.pos[1])
            if self.CM.IsPackedGate(hovering_key):
                if self.App.seleted_pack_key == hovering_key:
                    self.App.seleted_pack_key == ""
                else:
                    self.App.seleted_pack_key = hovering_key

# Holding Module UI Class
class HoldingModuleUI(BaseUI):
    def __init__(self, app):
        super().__init__(app, None)

    def Update(self, event: Event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.App.held_module_key = ""
    
    def Draw(self):
        if self.App.held_module_key != "":
            mx, my = pygame.mouse.get_pos()
            x = mx - self.App.held_pos[0]
            y = my - self.App.held_pos[1]
            size = 1
            if self.CM.IsPackedGate(self.App.held_module_key):
                size = self.CM
            DrawModule(self.Screen, self.App.held_module_key, (x,y), self.App.moduleFont, size)

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
            
            graph_height = graph_max_height * prob.real[0]
            graph_top = self.rect.top + graph_max_height - graph_height
            graph_left = x - self.graph_width / 2

            pygame.draw.rect(self.Screen, COLOR.GRAPHBLUE, Rect(graph_left, graph_top, self.graph_width, graph_height))