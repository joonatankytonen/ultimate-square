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
game_over_font = pygame.font.Font(None, 60)

# Tekstin renderöinti
text_left = font.render("Life", True, (0, 0, 0))
text_middle = font.render("Taso 1", True, (0, 0, 0))  # Väri (mustaa)
text_right = font.render("Score", True, (0, 0, 0))

# Pelaajan asetukset
player_size = 40
player_x, player_y = WIDTH//2, HEIGHT//2
player_speed = 5

running = True
game_over = False
while running:
    screen.fill((255, 255, 255))  # Täytetään näyttö valkoiseksi
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 10) # Piirretään reunat mustaksi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed
        
        # Tarkistetaan, tuleeko törmäyksiä seinien kanssa, jos tulee, peli loppuu=True
        if player_x <= 10 or player_x + player_size >= WIDTH - 10 or player_y <= 10 or player_y + player_size >= HEIGHT - 10:
            game_over = True
    
    # Piirrä pelaaja
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_size, player_size))
    
    # Piirrä teksti ruudulle (esimerkiksi ylhäällä)
    screen.blit(text_left, ( 20, 20))  # Teksti keskitettynä
    screen.blit(text_middle, (WIDTH // 2 - text_middle.get_width() // 2, 20))
    screen.blit(text_right, (WIDTH - text_right.get_width() - 20, 20))
    
    if game_over:
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0)) # game over fontti
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
