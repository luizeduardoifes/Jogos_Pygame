import pygame
import sys
import random

# Inicialização
pygame.init()
LARGURA, ALTURA = 600, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Brick Breaker Clássico")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

# Paddle
PADDLE_LARG = 80
PADDLE_ALT = 10
paddle = pygame.Rect(LARGURA//2 - PADDLE_LARG//2, ALTURA - 30, PADDLE_LARG, PADDLE_ALT)
vel_paddle = 7

# Bola
bola = pygame.Rect(LARGURA//2 - 10, ALTURA//2 - 10, 20, 20)
vel_bola = [random.choice([-4, 4]), -4]

# Tijolos
TIJOLO_LARG = 60
TIJOLO_ALT = 20
tijolos = []
for linha in range(5):
    for coluna in range(8):
        tijolo = pygame.Rect(10 + coluna*(TIJOLO_LARG+10), 40 + linha*(TIJOLO_ALT+10), TIJOLO_LARG, TIJOLO_ALT)
        tijolos.append(tijolo)

# Fonte
fonte = pygame.font.SysFont("Arial", 24)

def desenhar():
    TELA.fill(PRETO)
    pygame.draw.rect(TELA, AZUL, paddle)
    pygame.draw.ellipse(TELA, BRANCO, bola)
    for tijolo in tijolos:
        pygame.draw.rect(TELA, VERDE, tijolo)
    pygame.display.flip()

def main():
    rodando = True
    vitoria = False
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimento do paddle
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= vel_paddle
        if teclas[pygame.K_RIGHT] and paddle.right < LARGURA:
            paddle.x += vel_paddle

        # Movimento da bola
        bola.x += vel_bola[0]
        bola.y += vel_bola[1]

        # Colisão com paredes
        if bola.left <= 0 or bola.right >= LARGURA:
            vel_bola[0] *= -1
        if bola.top <= 0:
            vel_bola[1] *= -1

        # Colisão com paddle
        if bola.colliderect(paddle):
            bola.bottom = paddle.top  # Garante que a bola não fique presa na raquete
            vel_bola[1] *= -1

        # Colisão com tijolos
        for tijolo in tijolos[:]:
            if bola.colliderect(tijolo):
                tijolos.remove(tijolo)
                vel_bola[1] *= -1
                break

        # Fim de jogo
        if bola.bottom >= ALTURA:
            texto = fonte.render("Game Over!", True, VERMELHO)
            TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//2))
            pygame.display.flip()
            pygame.time.wait(2000)
            rodando = False

        if not tijolos:
            texto = fonte.render("Você Venceu!", True, VERDE)
            TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//2))
            pygame.display.flip()
            pygame.time.wait(2000)
            rodando = False

        desenhar()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()