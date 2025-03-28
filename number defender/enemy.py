import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, value, color=(200, 100, 100)):
        super().__init__()
        self.image = pygame.Surface((60, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.font = pygame.font.Font(None, 36)
        self.value = value
        
        text = self.font.render(value, True, (255,255,255))
        self.image.blit(text, (20, 10))
    
    def update(self, speed):
        self.rect.y += speed
