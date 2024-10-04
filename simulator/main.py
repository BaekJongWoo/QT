import pygame
import sys
from Circuit import QuantumCircuit
from Gate import *
from Module import Module
import COLOR
import CONFIG

# Pygame 초기화
pygame.init()

# 화면 크기 설정

screen = pygame.display.set_mode((CONFIG.SCREEN_WIDTH, CONFIG.SCREEN_HEIGHT))
pygame.display.set_caption("Click and Hold to Draw Circle")

qc = QuantumCircuit(3)

# 폰트 객체 생성
fontPath = "simulator/D2Coding.ttf"
baseFont = pygame.font.Font(fontPath, 15)  # None은 기본 폰트를 의미, 74는 폰트 크기
moduleFont = pygame.font.Font(None, 24)

ModuleList = [
    Module("H", COLOR.BLUSHRED),
    Module("X", COLOR.SHADYSKY),
    Module("Y", COLOR.SHADYSKY),
    Module("Z", COLOR.SHADYSKY),
]

# 원의 반지름 설정
radius = 20

# 마우스가 눌린 상태를 추적하는 변수
mouse_held = False

module_pos_list = []
def Iniitalize():
    for i in range(len(ModuleList)):
        xi = i % CONFIG.MODULES_PER_LINE
        yi = i // CONFIG.MODULES_PER_LINE
        x = 10 + xi * (10 + CONFIG.MODULE_SIZE)
        y = CONFIG.CIRCUIT_UI_HEIGHT + 10 + yi * (10 + CONFIG.MODULES_PER_LINE)
        module_pos_list.append((x,y))


def Update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()                    

        # 마우스 버튼을 눌렀을 때
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 왼쪽 버튼 클릭
                mouse_held = True

        # 마우스 버튼을 뗐을 때
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 왼쪽 버튼 클릭 해제
                mouse_held = False

def Draw():
    # 배경 화면을 흰색으로 채우기
    screen.fill(COLOR.BACKGROUND)

    DrawBaseLine()
    DrawModulesBase()

    # 마우스를 누르고 있는 동안 원을 그리기
    if mouse_held:
        pos = pygame.mouse.get_pos()
        pygame.draw.circle(screen, COLOR.RED, pos, radius)

    # 화면 업데이트
    pygame.display.flip()

def DrawBaseLine():
    for i in range(qc.size):
        y = (i+1) * CONFIG.LINESPACE
        text = baseFont.render(f"q[{i}]", True, COLOR.BASETEXT)  # 텍스트, 안티앨리어싱, 색상
        text_rect = text.get_rect(center=(25, y))  # 텍스트를 화면 중앙에 배치
        screen.blit(text, text_rect)
        pygame.draw.line(screen, COLOR.BASELINE, (50,y), (CONFIG.SCREEN_WIDTH - 30,y), width=CONFIG.LINEWIDTH)
    
    y = (qc.size + 1) * CONFIG.LINESPACE
    pygame.draw.line(screen, COLOR.BASELINE, (50,y-2), (CONFIG.SCREEN_WIDTH - 30,y-2), width=CONFIG.LINEWIDTH//2)
    pygame.draw.line(screen, COLOR.BASELINE, (50,y+2), (CONFIG.SCREEN_WIDTH - 30,y+2), width=CONFIG.LINEWIDTH//2)

def DrawModulesBase():
    for i, module in enumerate(ModuleList):
        rect = module_pos_list[i]
        module.Draw(screen, moduleFont, rect[0], rect[1])

# 게임 루프
running = True
Iniitalize()
while running:
    Update()
    Draw()