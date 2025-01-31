import pygame
import random

# Pygame asetukset
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Square")
clock = pygame.time.Clock()

# Fontin luominen
font = pygame.font.Font(None, 20)

# Tekstin renderöinti
text_left = font.render("Life", True, (0, 0, 0))
text_middle = font.render("Taso 1", True, (0, 0, 0))  # Väri (mustaa)
text_right = font.render("Score", True, (0, 0, 0))

# Pelaajan asetukset
player_size = 40
player_x, player_y = WIDTH//2, HEIGHT//2
player_speed = 5

running = True
while running:
    screen.fill((255, 255, 255))  # Täytetään näyttö valkoiseksi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed
    
    # Piirrä pelaaja
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_size, player_size))
    
    # Piirrä teksti ruudulle (esimerkiksi ylhäällä)
    screen.blit(text_left, ( 20, 20))  # Teksti keskitettynä
    screen.blit(text_middle, (WIDTH // 2 - text_middle.get_width() // 2, 20))
    screen.blit(text_right, (WIDTH - text_right.get_width() - 20, 20))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
