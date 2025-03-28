import pygame
import random
import sys
from player import Player
from enemy import Enemy
from bullet import Bullet
from shop import Shop

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Blaster")

COLORS = {
    "background": (30, 30, 50),
    "text": (240, 240, 240),
    "enemy": (200, 100, 100)
}

class GameState:
    def __init__(self):
        self.score = 0
        self.coins = 0
        self.bullet_speed = -10
        self.shop = Shop()
        self.current_problem = None
        self.correct_answer = None
        self.player_shape = "circle"  # Default shape

game_state = GameState()

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect

def main_menu():
    while True:
        screen.fill(COLORS["background"])
        draw_text("MATH BLASTER", 74, COLORS["text"], WIDTH//2, 100)
        
        play_btn = draw_text("PLAY", 50, COLORS["text"], WIDTH//2, 250)
        shop_btn = draw_text("SHOP", 50, COLORS["text"], WIDTH//2, 320)
        help_btn = draw_text("HOW TO PLAY", 50, COLORS["text"], WIDTH//2, 390)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_btn.collidepoint(mouse_pos):
                    difficulty_menu()
                elif shop_btn.collidepoint(mouse_pos):
                    game_state.shop.show(screen, game_state)
                elif help_btn.collidepoint(mouse_pos):
                    how_to_play()

def difficulty_menu():
    screen.fill(COLORS["background"])
    draw_text("SELECT DIFFICULTY", 60, COLORS["text"], WIDTH//2, 100)
    easy = draw_text("E - EASY", 50, COLORS["text"], WIDTH//2, 250)
    medium = draw_text("M - MEDIUM", 50, COLORS["text"], WIDTH//2, 320)
    hard = draw_text("H - HARD", 50, COLORS["text"], WIDTH//2, 390)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e: game_loop("easy")
                if event.key == pygame.K_m: game_loop("medium")
                if event.key == pygame.K_h: game_loop("hard")
                if event.key == pygame.K_ESCAPE: main_menu()

def how_to_play():
    screen.fill(COLORS["background"])
    lines = [
        "HOW TO PLAY:",
        "1. Use LEFT/RIGHT arrows to move",
        "2. Press SPACE to shoot numbers",
        "3. Only shoot the correct answer!",
        "4. Collect coins to buy shapes in the shop",
        "5. Wrong answers will end the game!",
        "Press ESC to return to menu"
    ]
    
    y = 100
    for line in lines:
        draw_text(line, 36, COLORS["text"], WIDTH//2, y)
        y += 40
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

def generate_problem(difficulty):
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    if difficulty == "hard" and random.choice([True, False]):
        op = "/"
        a, b = a * b, a  # Ensure division results in an integer
    else:
        op = random.choice(["+", "-", "*"])
    problem = f"{a} {op} {b}"
    answer = eval(problem)
    game_state.current_problem = problem
    game_state.correct_answer = answer
    return int(answer)

def game_loop(difficulty):
    player = Player(WIDTH//2, HEIGHT-60, game_state.player_shape)
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    answer = generate_problem(difficulty)
    
    enemy_speed = {"easy": 2, "medium": 4, "hard": 6}[difficulty]
    running = True
    
    while running:
        screen.fill(COLORS["background"])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.add(Bullet(player.rect.centerx, player.rect.top, game_state.bullet_speed))
                if event.key == pygame.K_ESCAPE:
                    main_menu()
        
        keys = pygame.key.get_pressed()
        player.move(keys, WIDTH)
        
        if random.random() < 0.02:
            x = random.randint(0, WIDTH-60)
            value = random.choice([answer, random.randint(max(1, answer-10), answer+10)])
            enemies.add(Enemy(x, -40, str(value), COLORS["enemy"]))
        
        bullets.update()
        enemies.update(enemy_speed)
        
        for bullet in bullets:
            for enemy in pygame.sprite.spritecollide(bullet, enemies, True):
                if int(enemy.value) == answer:
                    game_state.score += 1
                    game_state.coins += 1
                    answer = generate_problem(difficulty)
                else:
                    running = False
                bullet.kill()
        
        if pygame.sprite.spritecollideany(player, enemies):
            running = False
        
        player.draw(screen)
        enemies.draw(screen)
        bullets.draw(screen)
        
        draw_text(f"Problem: {game_state.current_problem} = ?", 36, COLORS["text"], WIDTH//2 + 50, 20)
        draw_text(f"Score: {game_state.score}  Coins: {game_state.coins}", 36, COLORS["text"], WIDTH//2, 60)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    main_menu()

if __name__ == "__main__":
    main_menu()
