import pygame

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, value, color):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.font = pygame.font.Font(None, 24)
        self.value = value
        text = self.font.render(value, True, (255,255,255))
        self.image.blit(text, (8, 5))
        self.speed = 3

    def update(self):
        self.rect.y += self.speed