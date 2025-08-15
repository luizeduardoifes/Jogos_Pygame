import os
import pygame
import random
import sys

# Inicialização
pygame.init()
LARGURA, ALTURA = 500, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Flapbird")

# Cores
BRANCO = (255, 255, 255)
AZUL = (135, 206, 250)
VERDE = (0, 200, 0)

# Parâmetros do pássaro
BIRD_X = 60
BIRD_Y = ALTURA // 2
BIRD_RAIO = 20
GRAVIDADE = 0.5
PULO = -8

# Parâmetros dos canos
CANO_LARGURA = 60
CANO_ALTURA = 400
CANO_GAP = 150
CANO_VELOCIDADE = 3

# Fonte
FONTE = pygame.font.SysFont("Arial", 32)

def desenhar_bird(y):
    pygame.draw.circle(TELA, BRANCO, (BIRD_X, int(y)), BIRD_RAIO)

def desenhar_cano(x, topo):
    pygame.draw.rect(TELA, VERDE, (x, 0, CANO_LARGURA, topo))
    pygame.draw.rect(TELA, VERDE, (x, topo + CANO_GAP, CANO_LARGURA, ALTURA - topo - CANO_GAP))

def colisao(bird_y, canos):
    for x, topo in canos:
        if BIRD_X + BIRD_RAIO > x and BIRD_X - BIRD_RAIO < x + CANO_LARGURA:
            if bird_y - BIRD_RAIO < topo or bird_y + BIRD_RAIO > topo + CANO_GAP:
                return True
    if bird_y - BIRD_RAIO < 0 or bird_y + BIRD_RAIO > ALTURA:
        return True
    return False

def main():
    bird_y = BIRD_Y
    velocidade = 0
    canos = []
    pontos = 0
    relogio = pygame.time.Clock()
    rodando = True

    # Inicializa dois canos
    for i in range(2):
        x = LARGURA + i * 200
        topo = random.randint(50, ALTURA - CANO_GAP - 50)
        canos.append([x, topo])

    while rodando:
        relogio.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    velocidade = PULO

        # Física do pássaro
        velocidade += GRAVIDADE
        bird_y += velocidade

        # Movimento dos canos
        for cano in canos:
            cano[0] -= CANO_VELOCIDADE

        # Novo cano
        if canos[0][0] < -CANO_LARGURA:
            canos.pop(0)
            x = canos[-1][0] + 200
            topo = random.randint(50, ALTURA - CANO_GAP - 50)
            canos.append([x, topo])
            pontos += 1

        # Colisão
        if colisao(bird_y, canos):
            break

        # Desenho
        TELA.fill(AZUL)
        desenhar_bird(bird_y)
        for x, topo in canos:
            desenhar_cano(x, topo)
        texto = FONTE.render(f"Pontos: {pontos}", True, (0,0,0))
        TELA.blit(texto, (10, 10))
        pygame.display.flip()

    # Fim de jogo
    fim = FONTE.render("Game Over!", True, (255,0,0))
    TELA.blit(fim, (LARGURA//2 - fim.get_width()//2, ALTURA//2))
    pygame.display.flip()
    pygame.time.wait(2000)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()