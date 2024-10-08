import pygame
import ui.COLOR as COLOR

class Module():
    def __init__(self, text, color) -> None:
        self.text = text  # 텍스트, 안티앨리어싱, 색상
        self.color = color

    def Draw(self, screen, font, rect: pygame.rect):
        pygame.draw.rect(screen, self.color, rect.Tuple())
        text = font.render(self.text, True, COLOR.TEXT)
        text_rect = text.get_rect(center=rect.Center)
        screen.blit(text, text_rect)