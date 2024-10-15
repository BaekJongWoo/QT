from __future__ import annotations
import pygame
from pygame import Rect, Surface
from pygame.event import Event
from pygame.font import Font
from ui.Module import PresetModule
from ui import COLOR, CONFIG
import app.QuantumSimulatorApp as qs
import static.EventHandler as EH 

import numpy as np

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
            self.App.Clear()
            self.App.Compute()
        return super().Update(event)

class BuildButtonUI(ButtonUI):
    def __init__(self, app, rect):
        super().__init__(app, rect, "Add", app.baseFont, COLOR.YELLOW, COLOR.LIGHTYELLOW)

    def Update(self, event):
        if EH.IsLMBClicked(event) and self.is_hovering:
            base_name =  "P" + str(len(self.App.presets))
            base_gates = np.full((self.App.max_module_per_line, self.App.qbit_num), "I", dtype="U2")
            preset_module = PresetModule(base_name, COLOR.WHITE, base_gates)
            self.App.AddPreset(base_name, preset_module)
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
        if self.App.held_module_key != "I" and self.hovering_coord != (-1, -1):
            self.App.AddModule(self.hovering_coord[0], self.hovering_coord[1], self.App.held_module_key)
        self.hovering_line_idx = "I"
        self.hovering_coord = (-1, -1)

    def DeleteHover(self):
        if self.hovering_coord != (-1, -1):
            self.App.RemoveModule(self.hovering_coord[0], self.hovering_coord[1])

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
        for (xi, yi), module_key in np.ndenumerate(self.App.CurrentCircuit):
            if module_key == "I":
                continue
            if module_key in self.App.modules:
                x = self.LINEMARGINLEFT + self.MODULEMARGIN / 2 + xi * (CONFIG.MODULE_SIZE + self.MODULEMARGIN)
                y = self.rect.y + (yi + 0.5) * self.LINESPACE - (CONFIG.MODULE_SIZE / 2)
                rect = Rect(x, y, CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE)
                self.App.modules[module_key].Draw(self.Screen, self.App.moduleFont, rect)
            elif yi == 0:
                x = self.LINEMARGINLEFT + self.MODULEMARGIN / 2 + xi * (CONFIG.MODULE_SIZE + self.MODULEMARGIN)
                y = self.rect.top + (0.5) * self.LINESPACE - CONFIG.MODULE_SIZE / 2
                height = self.App.qbit_num * (CONFIG.MODULE_SIZE + self.MODULEMARGIN) - self.MODULEMARGIN
                rect = Rect(x,y,CONFIG.MODULE_SIZE, height)
                self.App.presets[module_key].Draw(self.Screen, self.App.baseFont, rect)
        
        # draw hovering
        if self.App.held_module_key != "I":
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
    def __init__(self, app: qs.QuantumSimulatorApp, rect: Rect):
        super().__init__(app, rect)
        self.modules_per_line = self.rect.width // (CONFIG.MODULE_SIZE + 10)
        self.module_rects: dict[Rect] = {}
        self.UpdateModuleRects()

    def UpdateModuleRects(self):
        i = 0
        for module_key in self.App.modules.keys():
            xi = i % self.modules_per_line
            yi = i // self.modules_per_line
            x = 10 + xi * (10 + CONFIG.MODULE_SIZE)
            y = self.rect.top + 10 + yi * (10 + CONFIG.MODULE_SIZE)
            self.module_rects[module_key] = Rect(x, y, CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE)
            i+=1
        for module_key in self.App.presets.keys():
            xi = i % self.modules_per_line
            yi = i // self.modules_per_line
            x = 10 + xi * (10 + CONFIG.MODULE_SIZE)
            y = self.rect.top + 10 + yi * (10 + CONFIG.MODULE_SIZE)
            self.module_rects[module_key] = Rect(x, y, CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE)
            i+=1

    def Draw(self):
        for module_key in self.App.modules.keys():
            rect = self.module_rects[module_key]
            module = self.App.modules[module_key]
            module.Draw(self.App.screen, self.App.moduleFont, rect)

        for preset_key in self.App.presets.keys():
            rect = self.module_rects[preset_key]
            preset = self.App.presets[preset_key]
            preset.Draw(self.App.screen, self.App.moduleFont, rect)
            if self.App.seleted_preset == preset_key:
                pygame.draw.rect(self.Screen, COLOR.BLACK, rect, width=3)


    def Update(self, event: Event):
        if EH.IsLMBClicked(event):
            mouse_pos_rect = Rect(event.pos[0], event.pos[1], 1, 1)
            held_key = self.get_hovering_module_key(mouse_pos_rect)
            if held_key != "I":
                if self.App.seleted_preset != "" and held_key in self.App.presets:
                    pass
                else:
                    module_rect = self.module_rects[held_key]
                    held_pos =  (mouse_pos_rect.x - module_rect.x,
                                mouse_pos_rect.y - module_rect.y)
                    self.App.held_pos = held_pos
                    self.App.held_module_key = held_key
        
        if EH.IsRMBClicked(event):
            mouse_pos_rect = Rect(event.pos[0], event.pos[1], 1, 1)
            key = self.get_hovering_module_key(mouse_pos_rect)
            if key in self.App.presets:
                if self.App.seleted_preset == key:
                    self.App.seleted_preset = ""
                else:
                    self.App.seleted_preset = key
            elif self.rect.contains(mouse_pos_rect):
                self.App.seleted_preset = ""

    def get_hovering_module_key(self, mouse_pos_rect: Rect):
        for key, rect in self.module_rects.items():
            if rect.contains(mouse_pos_rect):
                return key
        return "I"

# Holding Module UI Class
class HoldingModuleUI(BaseUI):
    def __init__(self, app):
        super().__init__(app, None)

    def Update(self, event: Event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.App.held_module_key = "I"
    
    def Draw(self):
        if self.App.held_module_key != "I":
            mx, my = pygame.mouse.get_pos()
            rect = Rect(mx - self.App.held_pos[0], my - self.App.held_pos[1], CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE)
            if self.App.held_module_key in self.App.modules:
                module = self.App.modules[self.App.held_module_key]
            else:
                module = self.App.presets[self.App.held_module_key]
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
            

            