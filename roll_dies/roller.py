import pygame
import os
import random
import time

# 주사위 굴리기 모션
class DiceRoller: 
    def __init__(self, screen, image_folder_path, size=(100, 100)):
        self.screen = screen # 스크린 변수 
        self.image_folder_path = image_folder_path 
        self.size = size
        self.dice_imgs = self._load_dice_images()

    def _load_dice_images(self):
        imgs = []
        for i in range(1, 7):
            img_path = os.path.join(self.image_folder_path, f"dice{i}.png")
            img = pygame.image.load(img_path)
            img = pygame.transform.scale(img, self.size)
            imgs.append(img)
        return imgs

    def roll_two_dice(self, pos1=(80, 100), pos2=(220, 100), roll_times=20, delay=50):
        idx1 = idx2 = 0
        for _ in range(roll_times):
            idx1 = random.randint(0, 5)
            idx2 = random.randint(0, 5)

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.dice_imgs[idx1], pos1)
            self.screen.blit(self.dice_imgs[idx2], pos2)
            pygame.display.update()
            pygame.time.delay(delay)

        # 🎯 최종 결과를 다시 그려서 고정시킴
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.dice_imgs[idx1], pos1)
        self.screen.blit(self.dice_imgs[idx2], pos2)
        pygame.display.update()
        time.sleep(1)

        return idx1 + 1, idx2 + 1


