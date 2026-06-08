"""
안전한 리소스 로더 (Safe Resource Loader)
- 이미지 로드 실패 시 기본 placeholder 반환
- 폰트 로드 실패 시 시스템 폰트 사용
- 모든 로드 작업에 예외 처리 적용
"""
import pygame
import os
from .constants import COLORS

class ResourceLoader:
    """리소스 로딩 유틸리티 클래스"""
    
    def __init__(self):
        self.loaded_images = {}  # 로드된 이미지 캐시
        self.loaded_fonts = {}   # 로드된 폰트 캐시
    
    @staticmethod
    def create_placeholder_surface(width=100, height=100, color=COLORS['gray']):
        """
        리소스 로드 실패 시 반환할 placeholder 서피스 생성
        """
        surface = pygame.Surface((width, height))
        surface.fill(color)
        pygame.draw.rect(surface, COLORS['black'], (0, 0, width, height), 2)
        return surface
    
    def load_image(self, path, size=None, fallback_size=(100, 100)):
        """
        이미지 파일 로드 (캐싱 포함)
        
        Args:
            path (str): 이미지 파일 경로
            size (tuple): (width, height) - 크기 조정 원함. None이면 원본 크기
            fallback_size (tuple): 로드 실패 시 placeholder 크기
        
        Returns:
            pygame.Surface: 로드된 이미지 또는 placeholder
        """
        # 캐시 확인 (size 포함)
        cache_key = (path, size)
        if cache_key in self.loaded_images:
            return self.loaded_images[cache_key]
        
        try:
            if not os.path.exists(path):
                print(f"⚠️  이미지 파일 없음: {path}")
                placeholder = self.create_placeholder_surface(*fallback_size)
                self.loaded_images[cache_key] = placeholder
                return placeholder
            
            img = pygame.image.load(path)
            
            if size:
                img = pygame.transform.scale(img, size)
            
            self.loaded_images[cache_key] = img
            print(f"✅ 이미지 로드 성공: {path}")
            return img
        
        except pygame.error as e:
            print(f"❌ Pygame 이미지 로드 실패: {path} - {e}")
            placeholder = self.create_placeholder_surface(*fallback_size)
            self.loaded_images[cache_key] = placeholder
            return placeholder
        
        except Exception as e:
            print(f"❌ 예기치 않은 오류 (이미지 로드): {path} - {e}")
            placeholder = self.create_placeholder_surface(*fallback_size)
            self.loaded_images[cache_key] = placeholder
            return placeholder
    
    def load_font(self, path, size, fallback_font_name='arial'):
        """
        폰트 파일 로드 (캐싱 포함)
        
        Args:
            path (str): 폰트 파일 경로
            size (int): 폰트 크기
            fallback_font_name (str): 로드 실패 시 사용할 시스템 폰트 이름
        
        Returns:
            pygame.font.Font: 로드된 폰트 또는 시스템 폰트
        """
        cache_key = (path, size)
        if cache_key in self.loaded_fonts:
            return self.loaded_fonts[cache_key]
        
        try:
            if path and os.path.exists(path):
                font = pygame.font.Font(path, size)
                self.loaded_fonts[cache_key] = font
                print(f"✅ 폰트 로드 성공: {path} (크기: {size})")
                return font
            else:
                print(f"⚠️  폰트 파일 없음: {path}, 시스템 폰트 사용")
                font = pygame.font.SysFont(fallback_font_name, size)
                self.loaded_fonts[cache_key] = font
                return font
        
        except pygame.error as e:
            print(f"❌ Pygame 폰트 로드 실패: {path} - {e}")
            font = pygame.font.SysFont(fallback_font_name, size)
            self.loaded_fonts[cache_key] = font
            return font
        
        except Exception as e:
            print(f"❌ 예기치 않은 오류 (폰트 로드): {path} - {e}")
            font = pygame.font.SysFont(fallback_font_name, size)
            self.loaded_fonts[cache_key] = font
            return font
    
    def clear_cache(self):
        """캐시 초기화"""
        self.loaded_images.clear()
        self.loaded_fonts.clear()
        print("🗑️  리소스 캐시 초기화")

# 전역 리소스 로더 인스턴스
resource_loader = ResourceLoader()
