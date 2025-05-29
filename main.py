import pygame
import pygame_gui
import os
from board_set.BoardScreen import BoardScreen
from game import game_manager as gm
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

# 플레이어 객체 생성
game_manager = gm.GameManager()

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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_manager.get_current_player().is_bankrupt:
                    print(f"{game_manager.get_current_player_color()} 플레이어는 파산 상태입니다. 턴을 넘깁니다.")
                    game_manager.turn_over()
                else:
                    steps = roller.roll_dice()
                    current_player = game_manager.get_current_player()
                    current_player.move(steps)
                    print(f"{current_player.color} 플레이어가 {steps}칸 이동했습니다.")
                    print(f"현재 위치: {current_player.position}")
                    succes, message = game_manager.tile_event(current_player.position, current_player.turn)
                    print(message)
                    game_manager.turn_over()  # 턴 넘기기

            # F1 + p (커맨드)
            elif event.key == pygame.K_p:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_F1]:
                    print(f'현제 플레이어들의 위치: {[p.position for p in game_manager.players]}')
                
            # F1 + m (커맨드)
            elif event.key == pygame.K_m:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_F1]:
                    print(f'현제 플레이어들의 돈: {[p.money for p in game_manager.players]}')


        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 좌클릭
            clicked_tile_index = tiledeco.get_clicked_tile_index(mouse_pos, all_local)
            if clicked_tile_index is not None:
                print(clicked_tile_index)





    manager.update(time_delta)
    manager.draw_ui(background)

    pygame.display.update()

pygame.quit()

