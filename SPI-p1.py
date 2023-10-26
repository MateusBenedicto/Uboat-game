import pygame
from pygame import mixer
import random

#Inicia mixer pra usar sons
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

# Define fps
clock = pygame.time.Clock()
fps = 90

# Tamanho da tela
screen_largura = 600
screen_altura = 800

#Carrega os sons
explosion_fx = pygame.mixer.Sound("explosão/explosion.wav")
explosion_fx.set_volume(0.15)

explosionA_fx = pygame.mixer.Sound("explosão/explosion2.wav")
explosionA_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("explosão/laser_fx.wav")
laser_fx.set_volume(0.10)

theme = pygame.mixer.Sound("Musica/Tema.mp3")
theme.set_volume(0.20)

theme.play(loops=-1)

screen = pygame.display.set_mode((screen_largura, screen_altura))
pygame.display.set_caption('Space Invaders')


#definir fontes
font30 = pygame.font.SysFont('Comic Sans', 30)
font40 = pygame.font.SysFont('Comic Sans', 40)


# Define variaveis
linha = 5 
coluna = 5
alien_cooldown = 1000 
ultimo_tiro_A = pygame.time.get_ticks()
countdown = 3
contagen = pygame.time.get_ticks()
game_over = 0 #Se 1 jogador ganhou, se -1 jogador perder

#Define cores
red = (255,0,0)
green = (0,255,0)
white = (255,255,255)

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
        self.image = pygame.image.load("ship.png")
        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image, 180)  
        self.rect.center = [x, y]
        self.vida_start = vida
        self.vida_restante = vida
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self):
        # Define a velocidade do movimento
        vel = 5
        #Define um cooldown
        cooldown = 500 #milisegunddos
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

        # Faz a barra de vida
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 20), self.rect.width, 15))
        if self.vida_restante > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 20), int(self.rect.width * (self.vida_restante / self.vida_start)), 15))
        if self.vida_restante <= 0:
            explosao = Explosao(self.rect.centerx, self.rect.centery, 3)
            self.kill()
            game_over = -1
        return game_over


#Cria classe tiros
class Tiros(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0 :
            self.kill()
        if pygame.sprite.spritecollide(self, alien_grupo, True):
            self.kill()
            explosion_fx.play()
            explosao = Explosao(self.rect.centerx, self.rect.centery, 2)
            explosao_grupo.add(explosao)

#Cria class aliens 
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('alien' + str(random.randint(1,4)) +".png")
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


#Cria classe alien tiro
class A_Tiros(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("alien_bullet.png")
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
                img = pygame.transform.scale(img,(200, 200))
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
alien_grupo = pygame.sprite.Group()
A_Tiros_grupo = pygame.sprite.Group()
explosao_grupo = pygame.sprite.Group()        

def creat_aliens():
    #Gera os aliens
    for row in range(linha):
        for item in range(coluna):
            alien = Alien(100 + item * 100, 50 + row *70)
            alien_grupo.add(alien)

creat_aliens()
# Criar jogador
nave = Nave(int(screen_largura/2), screen_altura-100, 3)
nave_grupo.add(nave)
run = True
while run:

    clock.tick(fps)

    #Coloca o background
    draw_background()

    if countdown == 0:
        #cria balas de aliens aleatórios
        #conta o tempo atual
        time_now = pygame.time.get_ticks()
        #Alien atira
        if time_now - ultimo_tiro_A > alien_cooldown and len(A_Tiros_grupo) < 6 and len(alien_grupo) >0 :
                ataque_alien = random.choice(alien_grupo.sprites())
                alien_tiros= A_Tiros(ataque_alien.rect.centerx, ataque_alien.rect.bottom)
                A_Tiros_grupo.add(alien_tiros)
                ultimo_tiro_A = time_now

        #checa se mata todos os aliens
        if len(alien_grupo) == 0:
            game_over = 1
        

        if game_over ==0:
            #atualiza posição da nave
            game_over = nave.update()
            #atualiza os tiros 
            tiros_grupo.update()
            alien_grupo.update()
            A_Tiros_grupo.update()

        elif game_over == - 1:
            draw_text('GAME OVER', font40, white, int(screen_largura/2 -100), int(screen_altura/2))
        elif game_over ==  1:
            draw_text('YOU WIN', font40, white, int(screen_largura/2 -100), int(screen_altura/2))



    if countdown > 0:
        draw_text('SE PREPARE!', font40, white, int(screen_largura/2 -110), int(screen_altura/2 +50))
        draw_text(str(countdown), font40, white, int(screen_largura/2), int(screen_altura/2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - contagen> 1000:
            countdown -= 1
            contagen = count_timer

    #atualiza explosao_grupo fora dos ifs pois é animação
    explosao_grupo.update()
    
   #Desenha os grupos de sprite
    nave_grupo.draw(screen)
    tiros_grupo.draw(screen)
    alien_grupo.draw(screen)
    A_Tiros_grupo.draw(screen)
    explosao_grupo.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()