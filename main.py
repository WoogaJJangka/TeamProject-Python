import pygame
import os
from board_set.BoardScreen import BoardScreen
from board_set import TileDeco
import game.game_manager as gm
from roll_dices.roller import DiceRoller
import game.player as player

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

# 플레이어 객체 생성
game_manager = gm.GameManager()

running = True
while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                steps = roller.roll_dice()
                current_player = game_manager.get_current_player()
                current_player.move(steps)
                print(f"{current_player.color} 플레이어가 {steps}칸 이동했습니다.")
                print(f"현재 위치: {current_player.position}")
                game_manager.turn_over()  # 턴 넘기기

    # 마우스가 타일 위에 있으면 색상 변경
    for m_p in all_local:
        rect = pygame.Rect(m_p.mouse_position)
        if rect.collidepoint(mouse_pos):
            m_p.tile_cog_color(background)
        else:
            m_p.tile_word(background)

    pygame.display.update()

pygame.quit()
# 게임 종료
