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

    def roll_two_dice(self, pos1=None, pos2=None, roll_times=20, delay=50):
        # 화면 중앙에 주사위 위치 계산
        if pos1 is None or pos2 is None:
            screen_w, screen_h = self.screen.get_size() # 스크린 넓이와 높이 가져오기
            dice_w, dice_h = self.size # 주사위 넓이 높이 가져우기
            total_w = dice_w * 2 + 40  # 주사위 사이 간격 40px
            start_x = (screen_w - total_w) // 2 # 첫 주사위 x축 생성 좌표
            y = (screen_h - dice_h) // 2 # 주사위 y축 생성 좌표
            pos1 = (start_x, y) # 첫 번째 주사위 생성 좌표
            pos2 = (start_x + dice_w + 40, y) # 두 번째 주사위 생성 좌표
        idx1 = idx2 = 0 # 주사위 1,2의 초기값을 0으로 설정
        
        for _ in range(roll_times): # 주사위가 돌아가는 시간 설정
            idx1 = random.randint(0, 5) # 주사위 값 랜덤 부여(1~6)
            idx2 = random.randint(0, 5) # 주사위 값 랜덤 부여 (1~6)

            self.screen.blit(self.dice_imgs[idx1], pos1) # 주사위 값에 맞는 이미지를 위치에 불러옴
            self.screen.blit(self.dice_imgs[idx2], pos2) # 주사위 값에 맞는 이미지를 위치에 불러옴
            pygame.display.update() # 설정한 디스플레이를 불러옴
            pygame.time.delay(delay) # 주사위를 확인할 시간을 줌

        # 🎯 최종 결과를 다시 그려서 고정시킴
        self.screen.blit(self.dice_imgs[idx1], pos1) # 주사위 첫 번째 값에 맞는 이미지를 pos1에 불러오기
        self.screen.blit(self.dice_imgs[idx2], pos2) # 주사위 두 번째 값에 맞는 이미지를 pos2에 불러오기
        pygame.display.update() # 디스플레이 적용
        time.sleep(1)

        return idx1 + 1, idx2 + 1

    def roll_dice(self): # 주사위 굴리기기
        result1 , result2 = self.roll_two_dice() # 2개의 주사위 결과를 받기
        print(f"🎲 주사위 결과: {result1}, {result2}") # 결과를 터미널에 표시
        step = (result1 + result2)
        print(step , 0)
        while result1 == result2:
                result1 , result2 = self.roll_two_dice()
                print(f"🎲 주사위 결과: {result1}, {result2}") # 결과를 터미널에 표시
                step += (result1 + result2)
                print (step ,1)
        return step
