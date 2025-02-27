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

# Pelaajan väri
player_color = (255, 0, 0)  # oletusväri punainen

# Fontti-pontti asetukset
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Värivaihtoehdot
colors = {
    "Red": (255, 0, 0),
    "Blue": (0, 0, 255),
    "Green": (0, 255, 0),
    "Yellow": (255, 255, 0)
}

elama = 3  # Starting lives

# Pelin aloitussivu
def start_screen():
    global player_color
    running = True
    while running:
        screen.fill((50, 50, 50))  # Taustaväri
        
        # Värivalinnan otsikko ja nappulat keskellä
        color_text = font.render("Choose your player color:", True, (253, 253, 253))
        screen.blit(color_text, (WIDTH // 2 - color_text.get_width() // 2, 250))
        
        # Värivalintanapit
        button_x = WIDTH // 2 - (len(colors) * 80) // 2
        button_y = 300
        for color_name, color_value in colors.items():
            pygame.draw.rect(screen, color_value, (button_x, button_y, 60, 60))
            text = small_font.render(color_name, True, (255, 255, 255))
            screen.blit(text, (button_x, button_y + 65))
            button_x += 80
        
        # START-nappula
        start_button = pygame.Rect(WIDTH // 2 + 10, button_y + 150, 120, 50)
        pygame.draw.rect(screen, (211, 211, 211), start_button, border_radius=15)
        start_text = font.render("START", True, (0, 0, 0))
        text_x = start_button.x + (start_button.width - start_text.get_width()) // 2
        text_y = start_button.y + (start_button.height - start_text.get_height()) // 2
        screen.blit(start_text, (text_x, text_y))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                button_x = WIDTH // 2 - (len(colors) * 80) // 2
                button_y = 300
                for color_name, color_value in colors.items():
                    if button_x < x < button_x + 60 and button_y < y < button_y + 60:
                        player_color = color_value
                        print(f"Pelaajan väri valittu: {color_name}")
                    button_x += 80
                if start_button.collidepoint(x, y):
                    game()

# Peli
def game():
    global elama
    foodColor = (254, 141, 77)
    foodSize = 15
    ruokaOlemassa = 0
    new_food = None

    player_size = 40
    player_xPosition, player_yPosition = WIDTH // 2, HEIGHT // 2  # Pelaajan alku position
    player_speed = 5
    player_variable_x = 0
    player_variable_y = 0

    score = 0
    score_increment = 1

    level = 1
    game_over = False

    while not game_over:
        screen.fill((255, 255, 255))  # Täytetään näyttö valkoiseksi
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 10)  # Piirretään reunat mustaksi

        # Piirrä pelaaja
        player = pygame.draw.rect(screen, player_color, (player_xPosition, player_yPosition, player_size, player_size))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        player_xPosition += player_variable_x
        player_yPosition += player_variable_y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_variable_x = -player_speed
            player_variable_y = 0
        if keys[pygame.K_RIGHT]:
            player_variable_x = player_speed
            player_variable_y = 0
        if keys[pygame.K_UP]:
            player_variable_x = 0
            player_variable_y = -player_speed
        if keys[pygame.K_DOWN]:
            player_variable_x = 0
            player_variable_y = player_speed

        # Ruoka spawnaus
        if ruokaOlemassa == 0:
            x = random.randint(50, WIDTH-50)
            y = random.randint(50, HEIGHT-50)
            new_food = pygame.Rect(x, y, foodSize, foodSize)
            ruokaOlemassa = 1
        if player.colliderect(new_food):
            score += score_increment  # Lisää pistettä ruokaa syödessä
            score, level = switch_level(score, level)
            ruokaOlemassa = 0

        # Border collision detection: if the player hits the border, lose a life
        if player_xPosition <= 10 or player_xPosition + player_size >= WIDTH - 10 or player_yPosition <= 10 or player_yPosition + player_size >= HEIGHT - 10:
            elama -= 1
            print(f"Lives remaining: {elama}")
            # Reset player position after losing a life
            player_xPosition = WIDTH // 2 - player_size // 2
            player_yPosition = HEIGHT // 2 - player_size // 2

            if elama <= 0:
                print("Game Over!")
                game_over = True

        # Draw the food
        if new_food:
            pygame.draw.rect(screen, foodColor, new_food)

        # Text rendering
        text_left = font.render(f"Life: {elama}", True, (0, 0, 0))
        text_middle = font.render(f"Level {level}", True, (0, 0, 0))
        text_right = font.render(f"Score: {score}", True, (0, 0, 0))

        screen.blit(text_left, (20, 20))
        screen.blit(text_middle, (WIDTH // 2 - text_middle.get_width() // 2, 20))
        screen.blit(text_right, (WIDTH - text_right.get_width() - 20, 20))

        pygame.display.flip()
        clock.tick(30)

def switch_level(score, level):
    if level < 5 and score >= 10:
        print("Level change!")
        level += 1
        score = 0
    return score, level

# Start the game
start_screen()

# Close Pygame
pygame.quit()
