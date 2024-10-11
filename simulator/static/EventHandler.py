import pygame
from pygame.event import Event
    
def IsLMBClicked(event: Event) -> bool:
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            return True
    return False

def IsLMBReleased(event: Event) -> bool:
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            return True
    return False

def IsRMBClicked(event: Event) -> bool:
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 3:
            return True
    return False

def IsRMBReleased(event: Event) -> bool:
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 3:
            return True
    return False
