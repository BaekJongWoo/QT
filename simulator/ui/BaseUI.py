from __future__ import annotations

from pygame import Rect, Surface
from pygame.event import Event
from pygame.font import Font

import app.QuantumSimulatorApp as qs

class BaseUI:
    def __init__(self, app: qs.QuantumSimulatorApp, rect: Rect):
        self.App = app
        self.rect = rect
        self.CM = self.App.cm

    def Update(self, event: Event):
        pass

    def Draw(self):
        pass

    @property
    def Screen(self) -> Surface:
        return self.App.screen