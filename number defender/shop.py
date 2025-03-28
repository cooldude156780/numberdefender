import pygame
import sys
import math

def draw_text(text, size, color, x, y, screen):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

class Shop:
    def __init__(self):
        self.items = [
            {"name": "Circle", "cost": 0, "shape": "circle", "owned": True, "equipped": True},
            {"name": "Triangle", "cost": 25, "shape": "triangle", "owned": False, "equipped": False},
            {"name": "Hexagon", "cost": 50, "shape": "hexagon", "owned": False, "equipped": False},
            {"name": "Star", "cost": 100, "shape": "star", "owned": False, "equipped": False}
        ]
    
    def show(self, screen, state):
        while True:
            screen.fill((40, 40, 60))
            draw_text("SHOP", 60, (255,255,255), 400, 50, screen)
            
            for i, item in enumerate(self.items):
                y_pos = 150 + i * 100
                self.draw_shape(screen, item["shape"], (200, y_pos), 40)
                
                if item["owned"]:
                    if item["equipped"]:
                        text = f"{item['name']} (Equipped)"
                        color = (100, 255, 100)
                    else:
                        text = f"{item['name']} (Owned) - Press {i+1} to equip"
                        color = (255, 255, 100)
                else:
                    text = f"{item['name']} - {item['cost']} coins - Press {i+1} to buy"
                    color = (200,255,200) if state.coins >= item["cost"] else (100,100,100)
                
                draw_text(text, 30, color, 500, y_pos, screen)
            
            draw_text(f"Your coins: {state.coins}", 36, (255,255,255), 400, 550, screen)
            draw_text("Press ESC to return", 30, (255,255,255), 400, 580, screen)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: self.buy_or_equip(0, state)
                    if event.key == pygame.K_2: self.buy_or_equip(1, state)
                    if event.key == pygame.K_3: self.buy_or_equip(2, state)
                    if event.key == pygame.K_4: self.buy_or_equip(3, state)
                    if event.key == pygame.K_ESCAPE:
                        return
    
    def buy_or_equip(self, index, state):
        item = self.items[index]
        if item["owned"]:
            if not item["equipped"]:
                for i in self.items:
                    i["equipped"] = False
                item["equipped"] = True
                state.player_shape = item["shape"]
        elif state.coins >= item["cost"]:
            state.coins -= item["cost"]
            item["owned"] = True

    def draw_shape(self, screen, shape, pos, size):
        if shape == "triangle":
            points = [
                (pos[0], pos[1] - size//2),
                (pos[0] - size//2, pos[1] + size//2),
                (pos[0] + size//2, pos[1] + size//2)
            ]
            pygame.draw.polygon(screen, (100,200,100), points)
        elif shape == "hexagon":
            points = []
            for i in range(6):
                angle_deg = 60 * i - 30
                angle_rad = math.pi / 180 * angle_deg
                points.append((pos[0] + size//2 * math.cos(angle_rad),
                               pos[1] + size//2 * math.sin(angle_rad)))
            pygame.draw.polygon(screen, (100,100,200), points)
        elif shape == "star":
            points = []
            for i in range(10):
                angle_deg = 36 * i - 90
                angle_rad = math.pi / 180 * angle_deg
                radius = size//2 if i % 2 == 0 else size//4
                points.append((pos[0] + radius * math.cos(angle_rad),
                               pos[1] + radius * math.sin(angle_rad)))
            pygame.draw.polygon(screen, (255,255,0), points)
        else:  # Default circle
            pygame.draw.circle(screen, (200,100,100), pos, size//2)
