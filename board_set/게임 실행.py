import pygame
import random
import BoardScreen as BS # 뒷배경 함수 불러오기

pygame.init()

BS.BoardScreen() # 뒷배경 그리기 함수 실행

done = False # 실행 상태
while not done:

    for event in pygame.event.get(): # 이벤트 가져오기
        if event.type == pygame.QUIT: # 게임이 종료되면
            done = True # 실행 상태 변경
    pygame.display.update() # 디스플레이 적용


pygame.quit()