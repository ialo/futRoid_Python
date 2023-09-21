import pygame
import sys
import pygame.time



# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Mesclar Imagem e Texto")

# Carrega a imagem com fundo transparente
imagem = pygame.image.load("asteroidsPics/spaceRocket.png").convert_alpha()

# Define as cores
branco = (255, 255, 255)
fonte = pygame.font.Font(None, 30)  # Escolha a fonte e o tamanho desejados

# Texto que você deseja exibir
texto = "IALO"

# Posição inicial da imagem e do texto
pos_imagem = [300, 400]
pos_texto = [20, 10]

# Velocidades de movimento da imagem
velocidade_imagem = [1, 1]

# Crie uma superfície para mesclar a imagem e o texto
superficie_combinada = pygame.Surface((imagem.get_width(), imagem.get_height())).convert_alpha()
superficie_combinada.blit(imagem, (0, 0))

# Renderiza o texto na superfície combinada
texto_imagem = fonte.render(texto, True, branco)  # Cor do texto (preto)
superficie_combinada.blit(texto_imagem, pos_texto)

centro_x = largura // 2
centro_y = altura // 2
angulo_rotacao = 0
# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    imagem_rotacionada = pygame.transform.rotate(superficie_combinada, angulo_rotacao).convert_alpha()
    retangulo_rotacionado = imagem_rotacionada.get_rect(center=(centro_x, centro_y))

    # Preenche a tela com a cor branca
    tela.fill(branco)

    # Desenha a imagem girada na tela
    tela.blit(imagem_rotacionada, retangulo_rotacionado.topleft)

    # Atualiza a tela
    pygame.display.flip()

    # Aumenta o ângulo de rotação a cada iteração
    angulo_rotacao += 1

    if angulo_rotacao >= 360:
        angulo_rotacao = 0

    pygame.time.delay( 10)