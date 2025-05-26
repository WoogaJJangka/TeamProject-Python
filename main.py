# from board_set import board_start
# import roll_dices.roller
# import pygame
#
# board_start.set_board()
# roller = roll_dices.roller.DiceRoller(board_start.background,"roll_dices\\assets")
#
# for event in pygame.event.get():
#     if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # 키를 누르고 이벤트 키가 스페이스이면
#         roller.roll_dice()

import pygame
import os
from board_set.BoardScreen import BoardScreen
from board_set import TileDeco
from roll_dices.roller import DiceRoller

pygame.init()
clock = pygame.time.Clock()
background = pygame.display.set_mode((1500, 1000))
background.fill((255, 255, 255))

# 보드 배경 그리기
BoardScreen(background)

# 타일 설정 (board_set/TileDeco.py 참고)
all_local = TileDeco.all_local()

# 타일 글씨 그리기
for name in all_local:
    TileDeco.Tile.tile_word(name, background)

# 주사위 객체 생성
roller = DiceRoller(background, os.path.join("roll_dices", "assets"))

running = True
while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # 스페이스바 누르면 주사위 굴리기
            roller.roll_dice()

    # 마우스가 타일 위에 있으면 색상 변경
    for m_p in all_local:
        rect = pygame.Rect(m_p.mouse_position)
        if rect.collidepoint(mouse_pos):
            m_p.tile_cog_color(background)
        else:
            m_p.tile_word(background)

    pygame.display.update()

pygame.quit()

