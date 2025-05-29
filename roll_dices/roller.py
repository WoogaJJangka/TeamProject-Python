import pygame
import os
import random
import time

# 주사위 클래스
class DiceRoller: 
    def __init__(self, screen, image_folder_path, size = (100,100)):
        self.screen = screen # 스크린 변수 
        self.image_folder_path = image_folder_path # 폴더 주소
        self.size = size # 주사위 사이즈
        self.dice_imgs = self._load_dice_images() # 이미지 불러오기

    def _load_dice_images(self): # 이미지 불러오기 함수
        imgs = []
        for i in range(1, 7): # 1~6까지 반복
            img_path = os.path.join(self.image_folder_path, f"dice{i}.png") # 이미지파일 경로를 가져오기
            img = pygame.image.load(img_path) # img에 이미지를 로드하기 
            img = pygame.transform.scale(img, self.size) # 이미지 크기 변경
            imgs.append(img) # img를 imgs에 추가하기

        return imgs

    def roll_two_dice(self, group_pos=None, roll_times=20, delay=50):
        # group_pos: (x, y) - 주사위 객체 그룹(배경+주사위들)의 좌상단 위치
        dice_w, dice_h = self.size
        gap = 40  # 주사위 사이 간격
        pad = 20  # 배경 여백

        # 그룹 위치 지정
        if group_pos is None:
            screen_w, screen_h = self.screen.get_size()
            total_w = dice_w * 2 + gap
            bg_rect_width = total_w + pad * 2
            bg_rect_height = dice_h + pad * 2
            bg_rect_x = (screen_w - bg_rect_width) // 2
            bg_rect_y = (screen_h - bg_rect_height) // 2
        else:
            bg_rect_x, bg_rect_y = group_pos
            total_w = dice_w * 2 + gap
            bg_rect_width = total_w + pad * 2
            bg_rect_height = dice_h + pad * 2

        pos1 = (bg_rect_x + pad, bg_rect_y + pad)
        pos2 = (bg_rect_x + pad + dice_w + gap, bg_rect_y + pad)

        idx1 = idx2 = 0

        for _ in range(roll_times):
            idx1 = random.randint(0, 5)
            idx2 = random.randint(0, 5)

            # 검은색 테두리(조금 더 크게)
            pygame.draw.rect(
                self.screen, (0, 0, 0),
                (bg_rect_x - 3, bg_rect_y - 3, bg_rect_width + 6, bg_rect_height + 6),
                border_radius=24
            )
            # 하얀색 배경
            pygame.draw.rect(
                self.screen, (255, 255, 255),
                (bg_rect_x, bg_rect_y, bg_rect_width, bg_rect_height),
                border_radius=20
            )

            self.screen.blit(self.dice_imgs[idx1], pos1)
            self.screen.blit(self.dice_imgs[idx2], pos2)
            pygame.display.update()
            pygame.time.delay(delay)

        # 🎯 최종 결과를 다시 그려서 고정시킴
        pygame.draw.rect(
            self.screen, (0, 0, 0),
            (bg_rect_x - 3, bg_rect_y - 3, bg_rect_width + 6, bg_rect_height + 6),
            border_radius=24
        )
        pygame.draw.rect(
            self.screen, (255, 255, 255),
            (bg_rect_x, bg_rect_y, bg_rect_width, bg_rect_height),
            border_radius=20
        )
        self.screen.blit(self.dice_imgs[idx1], pos1)
        self.screen.blit(self.dice_imgs[idx2], pos2)
        pygame.display.update()
        time.sleep(1)

        return idx1 + 1, idx2 + 1

    def roll_dice(self, group_pos=None):  # 위치 인자 추가
        result1, result2 = self.roll_two_dice(group_pos=group_pos)
        print(f"🎲 주사위 결과: {result1}, {result2}")
        step = (result1 + result2)
        print(step, 0)
        while result1 == result2:
            result1, result2 = self.roll_two_dice(group_pos=group_pos)
            print(f"🎲 주사위 결과: {result1}, {result2}")
            step += (result1 + result2)
            print(step, 1)
        return step
