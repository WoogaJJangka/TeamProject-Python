import pygame


class ConsoleLog:
    def __init__(self, font_path, max_lines=8, position=(40, 0), size=(300, 640)):
        self.font_path = str(font_path)
        self.max_lines = max_lines
        self.position = position
        self.size = size
        self.messages = []

    def add(self, message):
        messages = message if isinstance(message, list) else [message]
        for item in messages:
            self.messages.insert(0, str(item))
            print(str(item))
        del self.messages[self.max_lines:]

    def draw(self, surface):
        font = pygame.font.Font(self.font_path, 16)
        start_y = surface.get_height() // 2 - self.max_lines * 20
        box = pygame.Surface(self.size)
        box.fill((255, 255, 255))
        surface.blit(box, (self.position[0], start_y - 2))

        lines = []
        for message in self.messages:
            wrapped = [message[index:index + 22] for index in range(0, len(message), 22)]
            lines.extend(reversed(wrapped))
        for index, line in enumerate(lines[:self.max_lines]):
            rendered = font.render(line, True, (30, 30, 30))
            surface.blit(rendered, (self.position[0] + 5, start_y + (self.max_lines - 1 - index) * 20))
