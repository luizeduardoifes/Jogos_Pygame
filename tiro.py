import pygame
import sys

# Inicialização do pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Tiro Simples")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Jogador
player_width, player_height = 50, 10
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 40
player_speed = 5

# Tiro
bullet_width, bullet_height = 5, 10
bullets = []
bullet_speed = 7

# Alvo
target_width, target_height = 40, 20
target_x = WIDTH // 2 - target_width // 2
target_y = 50
target_speed = 3
target_direction = 1

clock = pygame.time.Clock()

def draw():
    screen.fill(WHITE)
    # Jogador
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_width, player_height))
    # Tiros
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)
    # Alvo
    pygame.draw.rect(screen, BLACK, (target_x, target_y, target_width, target_height))
    pygame.display.flip()

def move_bullets():
    global bullets
    for bullet in bullets:
        bullet.y -= bullet_speed
    bullets = [b for b in bullets if b.y > 0]

def check_collision():
    global target_x, target_y
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet)
        target_rect = pygame.Rect(target_x, target_y, target_width, target_height)
        if bullet_rect.colliderect(target_rect):
            return True
    return False

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(player_x + player_width // 2 - bullet_width // 2,
                                    player_y, bullet_width, bullet_height)
                bullets.append(bullet)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Movimento do alvo
    target_x += target_speed * target_direction
    if target_x <= 0 or target_x >= WIDTH - target_width:
        target_direction *= -1

    move_bullets()

    if check_collision():
        # Reinicia o alvo em uma nova posição
        target_x = pygame.mouse.get_pos()[0]
        target_y = 50
        bullets.clear()

    draw()
    clock.tick(60)