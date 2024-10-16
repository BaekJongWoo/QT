from static import COLOR, CONFIG
import static.EventHandler as EH

import pygame
from pygame import Rect, Surface
from pygame.event import Event
from pygame.font import Font

from ui.BaseUI import BaseUI

class ButtonUI(BaseUI):
    is_hovering = False
    button_pressed = False
    enabled = True

    def __init__(self, app, rect, text, font: Font,
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

        if self.enabled:
            if EH.IsLMBClicked(event) and self.is_hovering:
                self.button_pressed = True
                self.Pressed()
            
            if EH.IsLMBReleased(event):
                self.button_pressed = False

    def Pressed(self):
        pass

    def Draw(self):
        color = self.color
        if not self.enabled:
            color = COLOR.GRAY
        elif self.button_pressed:
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

    def Pressed(self):
        self.App.Clear()
        self.App.Compute()

class AddPresetButtonUI(ButtonUI):
    def __init__(self, app, rect):
        super().__init__(app, rect, "Add", app.baseFont, COLOR.YELLOW, COLOR.LIGHTYELLOW)
    
    def Pressed(self):
        pass

class QbitMinusButton(ButtonUI):
    def __init__(self, app, rect, text):
        super().__init__(app, rect, text, app.baseFont, COLOR.WHITE, COLOR.LIGHTGRAY, COLOR.GRAY)

    def Update(self, event):
        self.enabled = self.CM.IsSubQbitValid(self.App.seleted_pack_key)
        return super().Update(event)

    def Pressed(self):
        self.CM.SubQbit(self.App.seleted_pack_key)

class QbitPlusButton(ButtonUI):
    def __init__(self, app, rect, text):
        super().__init__(app, rect, text, app.baseFont, COLOR.WHITE, COLOR.LIGHTGRAY, COLOR.GRAY)

    def Pressed(self):
        self.CM.AddQbit(self.App.seleted_pack_key)