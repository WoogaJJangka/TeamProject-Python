
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
import pygame_gui
import os
from board_set.BoardScreen import BoardScreen
from roll_dices.roller import DiceRoller
from game.tile_info import all_tiles  # 개선된 all_tiles 사용


pygame.init()
clock = pygame.time.Clock()
background = pygame.display.set_mode((1500, 1000))
background.fill((255, 255, 255))


# 보드 배경 그리기
BoardScreen(background)


# 타일 설정
tiles = all_tiles()

# 주사위 객체 생성
roller = DiceRoller(background, os.path.join("roll_dices", "assets"))

running = True
while running:
    time_delta = clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()

    # 타일 하이라이트
    for tile in tiles: # 타일 정보 전부 반복
        tile.draw(background, mouse_pos)
        if tile.visual.rect.collidepoint(mouse_pos):  # highlight 기준
            tile.draw_info(background, pos=(50, 50))
            break  # 하나만 표시하면 되므로 break

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 게임 X 종료
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # 스페이스 바 클릭 인식
            move = roller.roll_dice() # 주사위 굴리기(roll_dices.roller.py 참고)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, tile in enumerate(tiles): # 0부터 19까지 타일 반복(인덱스 번호, 타일)
                if tile.is_clicked(mouse_pos): # 특정 타일과 마우스 포인터가 겹칠 경우 True
                    print(idx)
                    break


    pygame.display.update()

pygame.quit()
