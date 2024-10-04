import pygame
import COLOR
import CONFIG

class Module():
    def __init__(self, text, color) -> None:
        self.text = text  # 텍스트, 안티앨리어싱, 색상
        self.color = color

    def Draw(self, screen, font, x, y):
        rect = (x,y,CONFIG.MODULE_SIZE, CONFIG.MODULE_SIZE)
        rect_center = (x + CONFIG.MODULE_SIZE / 2, y + CONFIG.MODULE_SIZE)
        pygame.draw.rect(screen, self.color, rect)
        text = font.render(self.text, True, COLOR.TEXT)
        text_rect = text.get_rect(center=rect_center)
        screen.blit(text, text_rect)