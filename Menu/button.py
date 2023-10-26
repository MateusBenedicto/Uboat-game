import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Button Exenpmlo")
fonte1 = pygame.font.SysFont("cambria", 50)

# Defina variáveis para cores
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)

class Button():
    def __init__(self, image, x, y, text_input):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_input = text_input
        self.text = fonte1.render(self.text_input, True, BRANCO)
        self.text_rect = self.text.get_rect(center=(self.x, self.y))

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_input(self, posicao):
        if self.rect.collidepoint(posicao):
            print("Butão clicado")

    def hover_color(self, posicao):
        if self.rect.collidepoint(posicao):
            self.text = fonte1.render(self.text_input, True, VERDE)
        else:
            self.text = fonte1.render(self.text_input, True, BRANCO)

button_surface = pygame.image.load("Menu/assets/Play Rect.png")
button_surface = pygame.transform.scale(button_surface, (400, 150))

button = Button(button_surface, 300, 300, "aperta ai troxa")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            button.check_input(pygame.mouse.get_pos())
    screen.fill(BRANCO)  # Define a cor de fundo como branco

    button.update()
    button.hover_color(pygame.mouse.get_pos())
    pygame.display.update()
