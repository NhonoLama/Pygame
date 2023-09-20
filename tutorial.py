import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
PLAYER_SPEED = 1
BULLET_SPEED = 1
ENEMY_SPEED = 1

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")

# Player
player_img = pygame.image.load("assets/0_Minotaur_Idle_000.png")
player_img = pygame.transform.scale(player_img, (150, 150))
player_rect = player_img.get_rect()
player_rect.center = (WIDTH // 2, HEIGHT - 50)
player_x_change = 0

# Bullets
bullets = []

# Enemies


class Enemy:
    def __init__(self, posx, posy, name):
        self.ename = name
        self.enemy_img = pygame.image.load(
            "assets/enemy.png")
        self.enemy_img = pygame.transform.scale(self.enemy_img, (150, 150))
        self.enemy_rect = self.enemy_img.get_rect()
        self.enemy_rect.center = (posx, posy)
        self.enemy_x_change = ENEMY_SPEED
        self.enemy_live = True


lvl1enemies = [Enemy(800, 50, 1), Enemy(10, 140, 2), Enemy(230, 250, 3)]
lvl2enemies = [Enemy(800, 50, 7), Enemy(10, 140, 4), Enemy(
    230, 250, 12), Enemy(456, 300, 14), Enemy(876, 420, 99)]

levels = [lvl1enemies, lvl2enemies]
print(levels[0])
level = 0
noOfEnemies = len(levels[level])

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -PLAYER_SPEED
            if event.key == pygame.K_RIGHT:
                player_x_change = PLAYER_SPEED
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(
                    player_rect.centerx, player_rect.top + 5, 4, 10)
                bullets.append(bullet)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Move the player
    player_rect.x += player_x_change
    if player_rect.x > WIDTH:
        player_rect.x -= WIDTH
    if player_rect.x < 0:
        player_rect.x += WIDTH

    # Move the enemy
    for enemy in levels[level]:
        enemy.enemy_rect.x += enemy.enemy_x_change
        if enemy.enemy_rect.x > WIDTH:
            enemy.enemy_rect.x -= WIDTH+200

    # Bullet movement
    for bullet in bullets:
        bullet.y -= BULLET_SPEED

    # Remove bullets that go off-screen
    bullets = [bullet for bullet in bullets if bullet.y > 0]

    # Collision detection
    for bullet in bullets:
        for enemy in levels[level]:
            if enemy.enemy_rect.colliderect(bullet):
                enemy.enemy_live = False
                if level == 0:
                    lvl1enemies.remove(enemy)
                else:
                    lvl2enemies.remove(enemy)
                bullets.remove(bullet)
                noOfEnemies -= 1
    # level upped
    if noOfEnemies == 0:
        level = 1
        noOfEnemies = len(levels[level])

    # Draw everything
    font = pygame.font.SysFont("Arial", 36)
    screen.fill(WHITE)
    txtsurf = font.render(f"LEVEL: {level}", True, (0, 0, 0))
    screen.blit(txtsurf, (1000, 650))
    txtsurf2 = font.render(f"ENEMY LEFT: {noOfEnemies}", True, (0, 0, 0))
    screen.blit(txtsurf2, (100, 650))

    if level == 1 and noOfEnemies == 0:
        txtsurf3 = font.render("You Win", True, (0, 0, 0))
        screen.blit(txtsurf3, (400, 350))

    screen.blit(player_img, player_rect)
    for enemy in levels[level]:
        if enemy.enemy_live:
            screen.blit(enemy.enemy_img, enemy.enemy_rect)
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)

    pygame.display.update()

# Game over
pygame.quit()
sys.exit()
