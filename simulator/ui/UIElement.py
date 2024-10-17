from __future__ import annotations
import pygame
from pygame import Rect, Surface
from pygame.event import Event
from pygame.font import Font

from ui.BaseUI import BaseUI
from static import COLOR, CONFIG
import app.QuantumSimulatorApp as qs
import static.EventHandler as EH 
from app.CircuitManager import GATES

import numpy as np

MODULE_SIZE = 30

LINEWIDTH = 2
LINESPACE = 40

LINEMARGINTOP = 10
LINEMARGINLEFT = 50
LINEMARGINRIGHT = 30

MODULEMARGIN = 10

def GetModuleRect(topCenter, moduleSize:int = 1):
    topleft = (topCenter[0] - MODULE_SIZE / 2, topCenter[1] - MODULE_SIZE / 2)
    size = (MODULE_SIZE, MODULE_SIZE + LINESPACE * (moduleSize - 1))
    return  Rect(topleft, size)

def DrawModule(surface: Surface, key: str, topCenter, font: Font, moduleSize: int = 1):
    color = COLOR.WHITE
    if key == "":
        color = COLOR.HOVERING_COLOR
    if key in COLOR.MODULE_COLOR:
        color = COLOR.MODULE_COLOR[key]
    
    rect = GetModuleRect(topCenter, moduleSize)
    pygame.draw.rect(surface, color, rect)

    if key != "":
        text = font.render(key, True, COLOR.BLACK)  # Text rendering
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)

# Quantum Circuit UI Class
class QuantumCircuitUI(BaseUI):
    
    def Update(self, event):
        if EH.IsLMBReleased(event):
            target_coord = self.GetHoverTargetCoord()
            if target_coord != None and self.App.held_module_key != "":
                self.App.AddModule(target_coord[0], target_coord[1], self.App.held_module_key)

        if EH.IsRMBClicked(event):
            target_coord = self.GetHoverTargetCoord()
            if target_coord != None:
                self.App.RemoveModule(target_coord[0], target_coord[1])

    def GetLineHeight(self, yi):
        return self.rect.top + LINEMARGINTOP + (yi + 0.5) * LINESPACE

    def GetCoordCenter(self, xi, yi):
        x = self.rect.left + LINEMARGINLEFT + (xi + 0.5) * (MODULE_SIZE + MODULEMARGIN)
        y = self.GetLineHeight(yi)
        return (x,y)

    def GetCollisionRect(self, xi, yi) -> Rect:
        center = self.GetCoordCenter(xi, yi)
        size = (MODULE_SIZE + MODULEMARGIN, LINESPACE)
        topleft = (center[0] - size[0] / 2, center[1] - size[1] / 2)
        return Rect(topleft, size)

    def GetHoverTargetCoord(self):
        mx, my = pygame.mouse.get_pos()
        target_rect = Rect(mx,my,1,1)
        for xi, line in enumerate(self.App.CurrentCircuit):
            for yi, key in enumerate(line):
                rect = self.GetCollisionRect(xi, yi)
                if rect.contains(target_rect):
                    return (xi, yi)
        else:
            qbit_num = self.CM.GetQbitNum(self.App.seleted_pack_key)
            line_num = self.CM.GetLen(self.App.seleted_pack_key)
            for yi in range(qbit_num):
                y = self.GetLineHeight(yi)
                y_min = y - LINESPACE / 2
                y_max = y + LINESPACE / 2
                if y_min < my < y_max:
                    return (line_num - 1, yi)
        return None

    def Draw(self):

        if self.App.seleted_pack_key != "":
            pygame.draw.rect(self.Screen, COLOR.WHITE, self.rect, 4)

        # draw base lines
        for yi in range(self.CM.GetQbitNum()):
            y = self.GetLineHeight(yi)
            text = self.App.baseFont.render(f"q[{yi}]", True, COLOR.BASETEXT)  # Text rendering
            text_rect = text.get_rect(center=(25, y))
            self.Screen.blit(text, text_rect)
            pygame.draw.line(self.Screen, COLOR.BASELINE, (LINEMARGINLEFT, y), (CONFIG.SCREEN_WIDTH - LINEMARGINRIGHT, y), width=LINEWIDTH)

        # draw measure line
        y = self.rect.y + (self.CM.GetQbitNum(self.App.seleted_pack_key) + 0.5) * LINESPACE
        pygame.draw.line(self.Screen, COLOR.BASELINE, (LINEMARGINLEFT, y - 2), (CONFIG.SCREEN_WIDTH - LINEMARGINRIGHT, y - 2), width=LINEWIDTH // 2)
        pygame.draw.line(self.Screen, COLOR.BASELINE, (LINEMARGINLEFT, y + 2), (CONFIG.SCREEN_WIDTH - LINEMARGINRIGHT, y + 2), width=LINEWIDTH // 2)

        # control line
        for xi, line in enumerate(self.App.CurrentCircuit):
            for yi, key in enumerate(line):
                if key == 'C':
                    cx, cy = self.GetCoordCenter(xi, yi)
                    y_min = self.GetLineHeight(0)
                    y_max = self.GetLineHeight(len(line) - 1)
                    pygame.draw.line(self.Screen, COLOR.GRAY, (cx, y_min), (cx, y_max), 2)
                    break

        # draw line modules
        for xi, line in enumerate(self.App.CurrentCircuit):
            for yi, key in enumerate(line):
                if key == "I" or key.isdigit():
                    continue
                center = self.GetCoordCenter(xi, yi)

                module_size = 1
                if self.CM.IsPackedGate(key):
                    module_size = self.CM.GetQbitNum(key)

                DrawModule(self.Screen, key, center, self.App.moduleFont, module_size)

                if "C" in line:
                    rect = GetModuleRect(center, module_size)
                    pygame.draw.rect(self.Screen, COLOR.GRAY, rect, 3)

        # draw hovering
        for xi, line in enumerate(self.App.CurrentCircuit):
            for yi, key in enumerate(line):
                collision_rect = self.GetCollisionRect(xi, yi)
                pygame.draw.rect(self.Screen, COLOR.WHITE, collision_rect, 3)

    def GetModuleCenter(self, xi, yi):
        x = LINEMARGINLEFT + MODULEMARGIN + xi * (MODULEMARGIN + MODULE_SIZE)
        y = self.rect.y + LINESPACE * (yi + 1) - MODULE_SIZE / 2
        return (x, y)

# Module Selector UI Class
class ModuleSelectorUI(BaseUI):
    margin = 10

    def __init__(self, app: qs.QuantumSimulatorApp, rect: Rect):
        super().__init__(app, rect)
        self.modules_per_line = self.rect.width // (MODULE_SIZE + 10)
    
    def GetRectCenter(self, i:int):
        xi = i % self.modules_per_line
        yi = i // self.modules_per_line
        x = self.rect.left + (xi + 0.5) * (self.margin + MODULE_SIZE)
        y = self.rect.top + (yi + 0.5) * (self.margin + MODULE_SIZE)
        return (x,y)
    
    def GetSeletableKeys(self):
        return list(GATES.keys()) + ['C'] + list(self.CM.packed_gate.keys())

    def GetKeyRectDict(self) -> dict[str, Rect]:
        ret = {}
        for i, key in enumerate(self.GetSeletableKeys()):
            center = self.GetRectCenter(i)
            ret[key] = GetModuleRect(center)
        return ret

    def Draw(self):
        for i, key in enumerate(self.GetSeletableKeys()):
            center = self.GetRectCenter(i)
            DrawModule(self.Screen, key, center, self.App.moduleFont, 1)
            if self.App.seleted_pack_key == key:
                rect = GetModuleRect(center)
                pygame.draw.rect(self.Screen, COLOR.BLACK, rect, width=3)

    def GetMouseHoveringModuleKey(self, mx, my) -> str:
        for key, rect in self.GetKeyRectDict().items():
            if rect.contains(Rect(mx, my, 1, 1)):
                return key
        return ""

    def Update(self, event: Event):
        if EH.IsLMBClicked(event):
            hovering_key = self.GetMouseHoveringModuleKey(event.pos[0], event.pos[1])
            if hovering_key != "":
                self.App.held_module_key = hovering_key
        
        if EH.IsRMBClicked(event):
            hovering_key = self.GetMouseHoveringModuleKey(event.pos[0], event.pos[1])
            if self.CM.IsPackedGate(hovering_key):
                if self.App.seleted_pack_key == hovering_key:
                    self.App.seleted_pack_key = ""
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
            size = 1
            if self.CM.IsPackedGate(self.App.held_module_key):
                size = self.CM.GetQbitNum(self.App.held_module_key)
            DrawModule(self.Screen, self.App.held_module_key, (mx,my), self.App.moduleFont, size)

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
            
            qbit_text = format(q_idx, f'0{self.CM.GetQbitNum(self.App.seleted_pack_key)}b')
            text = self.App.baseFont.render(f"|{qbit_text}⟩", True, COLOR.BASETEXT)  # Text rendering
            text_rect = text.get_rect(center=(x, self.rect.bottom - self.baseline_margin / 2))
            self.Screen.blit(text, text_rect)
            
            graph_height = graph_max_height * prob.real[0]
            graph_top = self.rect.top + graph_max_height - graph_height
            graph_left = x - self.graph_width / 2

            pygame.draw.rect(self.Screen, COLOR.GRAPHBLUE, Rect(graph_left, graph_top, self.graph_width, graph_height))