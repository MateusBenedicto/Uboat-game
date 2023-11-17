import pygame
import sys
import random

# inicialização do pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

#configurações do menu
clock = pygame.time.Clock()
fps = 90
screen_largura = 600
screen_altura = 800

# definr cores
white = (255, 255, 255)
green = (0, 255, 0)
red = (255,0,0)


#tela
screen = pygame.display.set_mode((screen_largura, screen_altura))
pygame.display.set_caption('U-BOAT')

#definir fontes
font30 = pygame.font.Font("fonte/font.ttf", 30)
font50 = pygame.font.Font("fonte/font.ttf", 50)
font40 = pygame.font.SysFont('fonte/font.ttf', 40)
font60 = pygame.font.SysFont('fonte/font.ttf', 60)
        
menu_theme = pygame.mixer.Sound("Musica/tema-M.mp3")
menu_theme.set_volume(1.30)

explosion_fx = pygame.mixer.Sound("explosão/explosion.wav")
explosion_fx.set_volume(0.15)

explosionA_fx = pygame.mixer.Sound("explosão/explosion2.wav")
explosionA_fx.set_volume(0.50)

laser_fx = pygame.mixer.Sound("explosão/laser_fx.wav")
laser_fx.set_volume(0.10)

theme = pygame.mixer.Sound("Musica/Tema.mp3")
theme.set_volume(1.30)
menu_theme.play(loops=-1)

class Button:
    def __init__(self, x, y, width, height, normal_image, hover_image, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.normal_image = pygame.image.load(normal_image)
        self.hover_image = pygame.image.load(hover_image)
        self.action = action
        self.is_hovered = False

    def draw(self):
        if self.is_hovered:
            screen.blit(self.hover_image, self.rect)
        else:
            screen.blit(self.normal_image, self.rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            if self.action:
                self.action()
# função pra desenhar texto
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2))


def start_game():
    global abre_menu
    abre_menu = False
    
    menu_theme.stop()
    
    theme.play(loops=-1)

    screen = pygame.display.set_mode((screen_largura, screen_altura))
    pygame.display.set_caption('U-BOAT')




    # Define variaveis
    linha = 5 
    coluna = 5
    enemy_cooldown = 700 
    ultimo_tiro_A = pygame.time.get_ticks()
    countdown = 3
    contagen = pygame.time.get_ticks()
    game_over = 0 #Se 1 jogador ganhou, se -1 jogador perder



    #Carregar imagem de background
    background = pygame.image.load("céu.png")

    def draw_background():
        screen.blit(background, (0, 0))

    #def funçao pra criar texto
    def draw_text(text, font, text_cor, x, y):
        img = font.render(text,True, text_cor)
        screen.blit(img,(x, y))



    #Classe da nave
    class Nave(pygame.sprite.Sprite):
        def __init__(self, x, y, vida):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("BOAT/ship1.png")
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            self.vida_start = vida
            self.vida_restante = vida
            self.ultimo_tiro = pygame.time.get_ticks()
            self.imagens = { 3: pygame.image.load("BOAT/ship1.png"),2: pygame.image.load("BOAT/BOAT.png"), 1: pygame.image.load("BOAT/BOAT2.png")}
            self.image = self.imagens[vida]
        

        def update(self):
            # Define a velocidade do movimento
            vel = 4.5
            #Define um cooldown
            cooldown = 600 #milisegunddos
            game_over = 0
            
            # Obtém pressionamento de tecla
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= vel
            if keys[pygame.K_RIGHT] and self.rect.right < screen_largura:
                self.rect.x += vel
            #pega o tempo atual
            time_now = pygame.time.get_ticks()
            #Define tecla para os tiros
            if keys[pygame.K_SPACE] and time_now - self.ultimo_tiro > cooldown: 
                laser_fx.play() 
                tiro = Tiros(self.rect.centerx, self.rect.top)
                tiros_grupo.add(tiro)
                self.ultimo_tiro = time_now

            #mask da colisão da nave, partes invisiveis sem colisão
            self.mask = pygame.mask.from_surface(self.image)

            if self.vida_restante in self.imagens:
                self.image = self.imagens[self.vida_restante]
            # Faz a barra de vida
            pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 20), self.rect.width, 15))
            if self.vida_restante > 0:
                pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 20), int(self.rect.width * (self.vida_restante / self.vida_start)), 15))
            if self.vida_restante <= 0:
                explosao = Explosao(self.rect.centerx, self.rect.centery, 3)
                self.kill()
                explosao_grupo.add(explosao)
                game_over = -1
            return game_over


    #Cria classe tiros
    class Tiros(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("sprites-tiros/tiro.png")
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

        def update(self):
            self.rect.y -= 5
            if self.rect.bottom < 0 :
                self.kill()
            enemy_colisao = pygame.sprite.spritecollide(self, enemy_grupo, True, pygame.sprite.collide_mask)
        
            for enemy in enemy_colisao:
                explosion_fx.play()
                explosao = Explosao(enemy.rect.centerx, enemy.rect.centery, 2)
                explosao_grupo.add(explosao)
                self.kill()


    #Cria class enemys 
    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('S-enemys/inimigo' + str(random.randint(1,6)) +".png")
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            self.move_counter = 0
            self.move_direction = 1
    
        def update(self):
            self.rect.x += self.move_direction
            self.move_counter += 1
            if abs(self.move_counter) > 75:
                self.move_direction  *= -1
                self.move_counter *= self.move_direction


    #Cria classe enemy tiro
    class E_Tiros(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("sprites-tiros/E_tiro.png")
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

        def update(self):
            self.rect.y += 2
            if self.rect.top > screen_altura :
                self.kill()
            if pygame.sprite.spritecollide(self, nave_grupo, False, pygame.sprite.collide_mask):
                self.kill()
                explosionA_fx.play()
                #diminui a vida
                nave.vida_restante -= 1
                explosao = Explosao(self.rect.centerx, self.rect.centery, 1)
                explosao_grupo.add(explosao)


    #Cria classe explosao
    class Explosao(pygame.sprite.Sprite):
        def __init__(self, x, y, size):
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            for num in range (1,6):
                img = pygame.image.load(f"explosão/exp{num}.png")
                if size == 1:
                    img = pygame.transform.scale(img,(20, 20))
                if size == 2:
                    img = pygame.transform.scale(img,(40, 40))
                if size == 3:
                    img = pygame.transform.scale(img,(100, 100))
                #adiciona a lista de imaghens
                self.images.append(img)
            self.index = 0
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            self.counter = 0

        def update(self):
            explosao_vel = 5
            #atualiza a animaçao explo
            self.counter += 1
            if self.counter >= explosao_vel and self.index < len(self.images) - 1:
                self.counter = 0
                self.index += 1
                self.image = self.images[self.index]
            
            if self.index >= len(self.images) - 1 and self.counter >= explosao_vel:
                self.kill()

    # Criando grupos de sprites 
    nave_grupo = pygame.sprite.Group()
    tiros_grupo = pygame.sprite.Group()
    enemy_grupo = pygame.sprite.Group()
    E_Tiros_grupo = pygame.sprite.Group()
    explosao_grupo = pygame.sprite.Group()        

    def creat_enemys():
        #Gera os enemys
        for row in range(linha):
            for item in range(coluna):
                enemy = Enemy(100 + item * 100, 50 + row *70)
                enemy_grupo.add(enemy)

    creat_enemys()
    # Criar jogador
    nave = Nave(int(screen_largura/2), screen_altura-100, 3)
    nave_grupo.add(nave)
    run = True
    while run:

        clock.tick(fps)

        #Coloca o background
        draw_background()

        if countdown == 0:
            #cria balas de enemys aleatórios
            #conta o tempo atual
            time_now = pygame.time.get_ticks()
            #enemy atira
            if time_now - ultimo_tiro_A > enemy_cooldown and len(E_Tiros_grupo) < 8 and len(enemy_grupo) > 0 :
                    ataque_enemy = random.choice(enemy_grupo.sprites())
                    enemy_tiros= E_Tiros(ataque_enemy.rect.centerx, ataque_enemy.rect.bottom)
                    E_Tiros_grupo.add(enemy_tiros)
                    ultimo_tiro_A = time_now

            #checa se mata todos os enemys
            if len(enemy_grupo) == 0:
                game_over = 1
            

            if game_over ==0:
                #atualiza posição da nave
                game_over = nave.update()
                #atualiza os tiros 
                tiros_grupo.update()
                enemy_grupo.update()
                E_Tiros_grupo.update()

            if game_over == -1 or game_over == 1:
                if game_over == -1:
                    draw_text('GAME OVER', font60, white, int(screen_largura/2 - 120), int(screen_altura/2))
                elif game_over == 1:
                    draw_text('YOU WIN', font60, white, int(screen_largura/2 - 120), int(screen_altura/2))


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False




        if countdown > 0:
            draw_text('GET READY!', font40, white, int(screen_largura/2 - 90), int(screen_altura/2 +50))
            draw_text(str(countdown), font40, white, int(screen_largura/2 - 7 ), int(screen_altura/2 + 100))
            count_timer = pygame.time.get_ticks()
            if count_timer - contagen> 1000:
                countdown -= 1
                contagen = count_timer

        #Atualiza explosao_grupo fora dos ifs pois é animação
        explosao_grupo.update()
        
    #Desenha os grupos de sprite
        nave_grupo.draw(screen)
        tiros_grupo.draw(screen)
        enemy_grupo.draw(screen)
        E_Tiros_grupo.draw(screen)
        explosao_grupo.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    pygame.quit()


#função para sair do jogo
def quit_game():
    pygame.quit()
    sys.exit()

#Classe principal do menu
class MainMenu:
    def __init__(self):
        self.play_button = Button(150, 300, 300, 75, "Botões/play.png", "Botões/play_hover.png",start_game)
        self.quit_button = Button(150, 450, 300, 75, "Botões/quit.png","Botões/quit_hover.png", quit_game)


    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                self.play_button.check_hover(event.pos)
                self.quit_button.check_hover(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.play_button.check_click(event.pos)
                    self.quit_button.check_click(event.pos)

    def draw(self):
        # Carrega a imagem de fundo menu
        background = pygame.image.load('Background.jpg')
        screen.blit(background, (0, 0))  

        draw_text("Main Menu", font50, white, screen_largura // 2, 100)
        self.play_button.draw()
        self.quit_button.draw()
        pygame.display.update()

abre_menu = True

#loop principal
while True:
    if abre_menu:
        main_menu = MainMenu()
        while abre_menu:
            main_menu.update()
            main_menu.draw()
            clock.tick(fps)
