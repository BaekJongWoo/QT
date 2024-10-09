import pygame 
from pygame import Rect, Surface
from pygame.font import Font
import ui.COLOR as COLOR

class Module():
    def __init__(self, text, color, gate) -> None:
        self.text = text  # 텍스트, 안티앨리어싱, 색상
        self.color = color
        self.gate = gate

    def Draw(self, screen: Surface, font: Font, rect: Rect):
        pygame.draw.rect(screen, self.color, rect)
        text = font.render(self.text, True, COLOR.TEXT)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
