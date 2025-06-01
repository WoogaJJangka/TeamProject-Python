import pygame
import os
import random
import time

# 주사위 클래스
class DiceRoller: 
    def __init__(self, screen, image_folder_path, size = (100,100)):
        self.screen = screen # 주사위를 그릴 pygame 화면 Surface
        self.image_folder_path = image_folder_path # 주사위 이미지가 저장된 폴더 경로
        self.size = size # 주사위 이미지의 크기 (가로, 세로)
        self.dice_imgs = self._load_dice_images() # 주사위 눈 이미지 리스트 로드

    def _load_dice_images(self): # 주사위 눈 이미지를 불러오는 함수
        imgs = []
        for i in range(1, 7): # 1~6까지 반복하여 각 눈 이미지를 불러옴
            img_path = os.path.join(self.image_folder_path, f"dice{i}.png") # 이미지 파일 경로 생성
            img = pygame.image.load(img_path) # 이미지 파일 로드
            img = pygame.transform.scale(img, self.size) # 이미지 크기 조정
            imgs.append(img) # 리스트에 추가
        return imgs

    def roll_two_dice(self, group_pos=None, roll_times=20, delay=50):
        """
        두 개의 주사위를 굴리고, 주사위 객체 그룹(배경+주사위들)을 원하는 위치에 그림.
        group_pos: (x, y) - 주사위 객체 그룹의 좌상단 위치
        roll_times: 주사위 굴리는 애니메이션 반복 횟수
        delay: 각 프레임 사이의 지연(ms)
        """
        dice_w, dice_h = self.size
        gap = 40  # 두 주사위 사이의 간격
        pad = 20  # 배경판의 여백

        # group_pos가 None이면 에러를 발생시키거나, 기본값을 왼쪽 고정 위치로 강제
        if group_pos is None:
            # 중앙에 그리는 코드는 더 이상 필요 없음. 왼쪽 고정 위치로 강제.
            group_pos = (44, 600)
        bg_rect_x, bg_rect_y = group_pos
        total_w = dice_w * 2 + gap
        bg_rect_width = total_w + pad * 2
        bg_rect_height = dice_h + pad * 2

        # 두 주사위의 실제 그릴 위치 계산
        pos1 = (bg_rect_x + pad, bg_rect_y + pad)
        pos2 = (bg_rect_x + pad + dice_w + gap, bg_rect_y + pad)

        idx1 = idx2 = 0 # 주사위 눈 인덱스

        for _ in range(roll_times):
            idx1 = random.randint(0, 5) # 첫 번째 주사위 눈(0~5)
            idx2 = random.randint(0, 5) # 두 번째 주사위 눈(0~5)

            # 검은색 테두리(배경판보다 3px 크게)
            pygame.draw.rect(
                self.screen, (0, 0, 0),
                (bg_rect_x - 3, bg_rect_y - 3, bg_rect_width + 6, bg_rect_height + 6),
                border_radius=24
            )
            # 하얀색 배경판
            pygame.draw.rect(
                self.screen, (255, 255, 255),
                (bg_rect_x, bg_rect_y, bg_rect_width, bg_rect_height),
                border_radius=20
            )

            # 두 주사위 이미지 그리기
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

        return idx1 + 1, idx2 + 1 # 실제 주사위 눈(1~6) 반환

    def roll_dice(self, group_pos=None):  # 위치 인자 추가
        """
        더블(같은 눈)이 나오면 다시 굴리는 규칙을 적용한 주사위 굴리기 함수.
        group_pos: 주사위 객체 그룹의 좌상단 위치
        """
        result1, result2 = self.roll_two_dice(group_pos=group_pos)
        print(f"🎲 주사위 결과: {result1}, {result2}")
        step = (result1 + result2)
        print(step, 0)
        while result1 == result2: # 더블이면 다시 굴림
            result1, result2 = self.roll_two_dice(group_pos=group_pos)
            print(f"🎲 주사위 결과: {result1}, {result2}")
            step += (result1 + result2)
            print(step, 1)
        return step # 총 이동 칸 수 반환
