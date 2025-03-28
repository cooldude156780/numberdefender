import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, shape):
        super().__init__()
        self.shape = shape
        self.image = self.create_shape_surface(shape)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 8
    
    def move(self, keys, width):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def create_shape_surface(self, shape):
        surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        if shape == "triangle":
            pygame.draw.polygon(surface, (100,200,100), [(20,0), (0,40), (40,40)])
        elif shape == "hexagon":
            pygame.draw.polygon(surface, (100,100,200), [(10,0), (30,0), (40,20), (30,40), (10,40), (0,20)])
        elif shape == "star":
            points = []
            for i in range(10):
                angle = i * 36 * 3.14159 / 180
                r = 20 if i % 2 == 0 else 10
                points.append((
                    20 + int(r * pygame.math.Vector2(1, 0).rotate(angle).x),
                    20 + int(r * pygame.math.Vector2(1, 0).rotate(angle).y)
                ))
            pygame.draw.polygon(surface, (200,200,100), points)
        else:  # Default circle
            pygame.draw.circle(surface, (200,100,100), (20, 20), 20)
        return surface
