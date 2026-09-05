import pygame


class Button:
    def __init__(self, rect, text, font, color=(200, 200, 200), text_color=(0, 0, 0)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 2)
        rendered = self.font.render(self.text, True, self.text_color)
        surface.blit(rendered, rendered.get_rect(center=self.rect.center))

    def is_clicked(self, position):
        return self.rect.collidepoint(position)
