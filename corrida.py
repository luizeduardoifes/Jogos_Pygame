import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA = 500
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Corrida")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Carro do jogador
CARRO_LARGURA = 50
CARRO_ALTURA = 90
carro_img = pygame.Surface((CARRO_LARGURA, CARRO_ALTURA))
carro_img.fill(AZUL)
carro_x = LARGURA // 2 - CARRO_LARGURA // 2
carro_y = ALTURA - CARRO_ALTURA - 10
velocidade = 5

# Obstáculos
obstaculo_largura = 50
obstaculo_altura = 90
obstaculo_velocidade = 7
obstaculos = []

# Pontuação
pontos = 0
fonte = pygame.font.SysFont(None, 36)

def desenhar_obstaculos(obstaculos):
    for obs in obstaculos:
        pygame.draw.rect(TELA, VERMELHO, obs)

def mostrar_pontos(pontos):
    texto = fonte.render(f"Pontos: {pontos}", True, PRETO)
    TELA.blit(texto, (10, 10))

def main():
    global carro_x, pontos
    relogio = pygame.time.Clock()
    rodando = True

    while rodando:
        relogio.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Movimento do carro
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and carro_x > 0:
            carro_x -= velocidade
        if teclas[pygame.K_RIGHT] and carro_x < LARGURA - CARRO_LARGURA:
            carro_x += velocidade

        # Gerar obstáculos
        if random.randint(1, 30) == 1:
            x_obs = random.randint(0, LARGURA - obstaculo_largura)
            obstaculos.append(pygame.Rect(x_obs, -obstaculo_altura, obstaculo_largura, obstaculo_altura))

        # Mover obstáculos
        for obs in obstaculos:
            obs.y += obstaculo_velocidade

        # Remover obstáculos fora da tela e contar pontos
        obstaculos[:] = [obs for obs in obstaculos if obs.y < ALTURA]
        pontos += sum(1 for obs in obstaculos if obs.y + obstaculo_altura >= ALTURA)

        # Colisão
        carro_rect = pygame.Rect(carro_x, carro_y, CARRO_LARGURA, CARRO_ALTURA)
        for obs in obstaculos:
            if carro_rect.colliderect(obs):
                rodando = False

        # Desenhar tudo
        TELA.fill(BRANCO)
        TELA.blit(carro_img, (carro_x, carro_y))
        desenhar_obstaculos(obstaculos)
        mostrar_pontos(pontos)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()