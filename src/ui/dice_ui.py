"""
주사위 UI (Dice Animation)
"""
import pygame
import random
import time
from src.core.resource_loader import resource_loader

class DiceUI:
    """주사위 렌더링 및 애니메이션"""
    
    def __init__(self, image_folder_path: str, size: tuple = (100, 100)):
        """
        DiceUI 초기화
        
        Args:
            image_folder_path (str): 주사위 이미지 폴더 경로
            size (tuple): 주사위 이미지 크기 (w, h)
        """
        self.size = size
        self.image_folder_path = image_folder_path
        self.dice_imgs = self._load_dice_images()
    
    def _load_dice_images(self) -> list:
        """주사위 1~6 이미지 로드"""
        imgs = []
        for i in range(1, 7):
            path = f"{self.image_folder_path}/dice{i}.png"
            img = resource_loader.load_image(path, self.size, self.size)
            imgs.append(img)
        return imgs
    
    def roll_two_dice(self, screen: pygame.Surface, group_pos: tuple = None, 
                      roll_times: int = 20, delay: int = 50) -> tuple:
        """
        주사위 2개 굴림 (애니메이션 포함)
        
        Args:
            screen (pygame.Surface): 렌더링 대상
            group_pos (tuple): (x, y) 주사위 그룹 위치
            roll_times (int): 애니메이션 프레임 수
            delay (int): 프레임 간 지연 (ms)
        
        Returns:
            (dice1, dice2): 1~6 범위의 주사위 눈
        """
        dice_w, dice_h = self.size
        gap = 40
        pad = 20
        
        # 배경판 위치 계산
        if group_pos is None:
            screen_w, screen_h = screen.get_size()
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
        
        # 주사위 위치
        pos1 = (bg_rect_x + pad, bg_rect_y + pad)
        pos2 = (bg_rect_x + pad + dice_w + gap, bg_rect_y + pad)
        
        idx1 = idx2 = 0
        
        # 애니메이션 루프
        for _ in range(roll_times):
            idx1 = random.randint(0, 5)
            idx2 = random.randint(0, 5)
            
            # 검은 테두리
            pygame.draw.rect(screen, (0, 0, 0),
                           (bg_rect_x - 3, bg_rect_y - 3, bg_rect_width + 6, bg_rect_height + 6),
                           border_radius=24)
            # 흰 배경
            pygame.draw.rect(screen, (255, 255, 255),
                           (bg_rect_x, bg_rect_y, bg_rect_width, bg_rect_height),
                           border_radius=20)
            
            # 주사위 이미지
            screen.blit(self.dice_imgs[idx1], pos1)
            screen.blit(self.dice_imgs[idx2], pos2)
            pygame.display.update()
            pygame.time.delay(delay)
        
        # 최종 결과 고정 표시
        pygame.draw.rect(screen, (0, 0, 0),
                       (bg_rect_x - 3, bg_rect_y - 3, bg_rect_width + 6, bg_rect_height + 6),
                       border_radius=24)
        pygame.draw.rect(screen, (255, 255, 255),
                       (bg_rect_x, bg_rect_y, bg_rect_width, bg_rect_height),
                       border_radius=20)
        screen.blit(self.dice_imgs[idx1], pos1)
        screen.blit(self.dice_imgs[idx2], pos2)
        pygame.display.update()
        time.sleep(1)
        
        return idx1 + 1, idx2 + 1  # 1~6 범위 반환
