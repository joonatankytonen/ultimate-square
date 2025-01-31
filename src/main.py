import pygame
import random

# Pygame asetukset
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Square")
clock = pygame.time.Clock()

# Pelaajan asetukset
player_size = 40
player_x, player_y = WIDTH//2, HEIGHT//2
player_speed = 5

running = True
while running:
    screen.fill((255,255,255))   
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
    pygame.draw.rect(screen, (255,0,0), (player_x, player_y, player_size, player_size))
    
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
