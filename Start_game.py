import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo Divertido para Crianças")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)

# Sons
som_colisao = pygame.mixer.Sound('explosion-6801.mp3')  # Carregar sons
som_power_up = pygame.mixer.Sound('item-pick-up-38258.mp3')

# Clock para controlar o FPS
clock = pygame.time.Clock()

# Fonte para pontuação
fonte = pygame.font.SysFont(None, 40)


# Classe do Jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
        self.rect.center = (largura // 2, altura - 50)
        self.velocidade = 5
        self.velocidade_normal = self.velocidade
        self.tempo_invencivel = 0
        self.vidas = 3

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.right < largura:
            self.rect.x += self.velocidade
        if self.tempo_invencivel > 0:
            self.tempo_invencivel -= 1  # Diminui o tempo de invencibilidade


# Classe do Inimigo
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(PRETO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidade = random.randint(3, 8)
        self.velocidade_normal = self.velocidade

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > altura:
            self.rect.x = random.randint(0, largura - self.rect.width)
            self.rect.y = random.randint(-100, -40)


# Classe do Power-up
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo
        self.image = pygame.Surface((30, 30))

        # Cor e efeito baseados no tipo de power-up
        if self.tipo == 'velocidade':
            self.image.fill(AZUL)
        elif self.tipo == 'desacelerar':
            self.image.fill(AMARELO)
        elif self.tipo == 'vida':
            self.image.fill(VERDE)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidade = 5

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > altura:
            self.rect.x = random.randint(0, largura - self.rect.width)
            self.rect.y = random.randint(-100, -40)


# Função para o menu inicial
def mostrar_menu():
    tela.fill(BRANCO)
    fonte = pygame.font.SysFont(None, 55)
    texto = fonte.render("Pressione qualquer tecla para jogar", True, PRETO)
    tela.blit(texto, (100, 250))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYUP:
                esperando = False


# Função para mostrar a pontuação e as vidas
def mostrar_info(pontuacao, vidas):
    texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, PRETO)
    texto_vidas = fonte.render(f'Vidas: {vidas}', True, PRETO)
    tela.blit(texto_pontuacao, (10, 10))
    tela.blit(texto_vidas, (10, 50))


# Função principal do jogo
def jogo():
    jogador = Jogador()
    inimigos = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()

    for _ in range(5):  # Cria 5 inimigos no início
        inimigo = Inimigo()
        inimigos.add(inimigo)

    todos_sprites = pygame.sprite.Group()
    todos_sprites.add(jogador)
    todos_sprites.add(inimigos)

    # Pontuação
    pontuacao = 0
    power_up_ativo = False
    tempo_power_up = 0

    jogando = True
    while jogando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Adiciona power-up aleatoriamente
        if random.randint(0, 300) == 1:
            tipo_power_up = random.choice(['velocidade', 'desacelerar', 'vida'])
            power_up = PowerUp(tipo_power_up)
            power_ups.add(power_up)
            todos_sprites.add(power_up)

        # Atualiza as posições
        todos_sprites.update()

        # Colisão com inimigos (se o jogador não estiver invencível)
        if jogador.tempo_invencivel == 0:
            if pygame.sprite.spritecollide(jogador, inimigos, False):
                som_colisao.play()
                jogador.vidas -= 1
                if jogador.vidas <= 0:
                    jogando = False  # Fim de jogo
                else:
                    jogador.tempo_invencivel = 180  # Jogador invencível por 3 segundos

        # Colisão com power-ups
        power_up_colisao = pygame.sprite.spritecollide(jogador, power_ups, True)
        for power_up in power_up_colisao:
            som_power_up.play()
            if power_up.tipo == 'velocidade':
                jogador.velocidade += 3
                tempo_power_up = 300  # Power-up dura 5 segundos
            elif power_up.tipo == 'desacelerar':
                for inimigo in inimigos:
                    inimigo.velocidade -= 3
                tempo_power_up = 300
            elif power_up.tipo == 'vida':
                jogador.vidas += 1

        # Controle do tempo dos power-ups
        if tempo_power_up > 0:
            tempo_power_up -= 1
        else:
            jogador.velocidade = jogador.velocidade_normal  # Restaura velocidade normal
            for inimigo in inimigos:
                inimigo.velocidade = inimigo.velocidade_normal  # Restaura velocidade normal dos inimigos

        # Desenha a tela
        tela.fill(BRANCO)
        todos_sprites.draw(tela)
        mostrar_info(pontuacao, jogador.vidas)

        # Atualiza o display
        pygame.display.flip()

        # Atualiza a pontuação
        pontuacao += 1

        # Controla o FPS
        clock.tick(60)


# Loop principal do jogo
while True:
    mostrar_menu()
    jogo()
