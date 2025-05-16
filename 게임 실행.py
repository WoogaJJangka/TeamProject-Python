import pygame
import random
import BoardScreen as BS # 뒷배경 함수 불러오기

pygame.init()

BS.BoardScreen() # 뒷배경 그리기 함수 실행

done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pygame.display.update()


pygame.quit()