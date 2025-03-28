import pygame

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()
