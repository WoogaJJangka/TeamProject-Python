import pygame
import random
import BoardScreen as BS

pygame.init()

BS.BoardScreen()

done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pygame.display.update()


pygame.quit()