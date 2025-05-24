from board_set import board_start 
import roll_dices.roller
import pygame

board_start.set_board()
roller = roll_dices.roller.DiceRoller(board_start.background,"roll_dices\\assets")

for event in pygame.event.get():
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # 키를 누르고 이벤트 키가 스페이스이면
        roller.roll_dice()