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
from board_set import tiledeco
from roll_dices.roller import DiceRoller
from game_gui import button, Lavel


pygame.init()
clock = pygame.time.Clock()
background = pygame.display.set_mode((1500, 1000))
background.fill((255, 255, 255))

# GUI 설정
manager = pygame_gui.UIManager((1500,1000))

# 보드 배경 그리기
BoardScreen(background)

# 타일 설정 (board_set/tiledeco.py 참고)
all_local = tiledeco.all_local()

# 타일 글씨 그리기
for name in all_local:
    tiledeco.TileDeco.tile_word(name, background)

# 주사위 객체 생성
roller = DiceRoller(background, os.path.join("roll_dices", "assets"))

#YES 아니면 NO 버튼 생성
ybutton = button.Ybutton(manager)
nbutton = button.Nbutton(manager)
ybutton.hide()
nbutton.hide()


running = True
while running:
    time_delta  = clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()

    # 마우스가 타일 위에 있으면 색상 변경
    tiledeco.tile_color_change(mouse_pos, all_local, background)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # 스페이스바 누르면 주사위 굴리기
            move = roller.roll_dice()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 좌클릭
            clicked_tile_index = tiledeco.get_clicked_tile_index(mouse_pos, all_local)
            if clicked_tile_index is not None:
                print(clicked_tile_index)





    manager.update(time_delta)
    manager.draw_ui(background)

    pygame.display.update()

pygame.quit()

