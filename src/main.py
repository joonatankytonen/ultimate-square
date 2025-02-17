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
 
# logoloinen tähän
game_title = pygame.image.load("pelin_nimi.png")
 
# pelaajan väri
player_color = (255, 0, 0) # oletusväri punainen
 
# fontti-pontti asetukset
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)
 
# värivaihtoehdot
colors = {
"Red": (255, 0, 0),
"Blue": (0, 0, 255),
"Green": (0, 255, 0),
"Yellow": (255, 255, 0)
}


 
# pelin aloitussivu
def start_screen():
  global player_color
  running = True
  while running:
    screen.fill((50, 50, 50)) # Taustaväri
      
    # Värivalinnan otsikko ja nappulat keskellä
    color_text = font.render("Choose your player color:", True, (253, 253, 253))
    screen.blit(color_text, (WIDTH // 2 - color_text.get_width() // 2, 250))
    
    # Värivalintanapit keskelle
    button_x = WIDTH // 2 - (len(colors) * 80) // 2
    button_y = 300
    for color_name, color_value in colors.items():
      pygame.draw.rect(screen, color_value, (button_x, button_y, 60, 60))
      text = small_font.render(color_name, True, (255, 255, 255))
      screen.blit(text, (button_x, button_y + 65))
      button_x += 80
    
    # Painikkeita vielä vähän alemmas
    button_y += 150 
    
    # START-nappula
    start_button = pygame.Rect(WIDTH // 2 + 10, button_y, 120, 50)
    pygame.draw.rect(screen, (211, 211, 211), start_button, border_radius=15)
    start_text = font.render("START", True, (0, 0, 0))
    text_x = start_button.x + (start_button.width - start_text.get_width()) // 2
    text_y = start_button.y + (start_button.height - start_text.get_height()) // 2
    screen.blit(start_text, (text_x, text_y))
    
    # OHJEET-nappula
    ohjeet_button = pygame.Rect(WIDTH // 2 - 130, button_y, 120, 50)
    pygame.draw.rect(screen, (211, 211, 211), ohjeet_button, border_radius=15)
    ohjeet_text = font.render("GUIDE", True, (0, 0, 0))
    text_x = ohjeet_button.x + (ohjeet_button.width - ohjeet_text.get_width()) // 2
    text_y = ohjeet_button.y + (ohjeet_button.height - ohjeet_text.get_height()) // 2
    screen.blit(ohjeet_text, (text_x, text_y))
      
    pygame.display.flip()
      
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        button_x = 10
        button_y = 370
        for color_name, color_value in colors.items():
          if button_x < x < button_x + 60 and button_y < y < button_y + 60:
            player_color = color_value
            print(f"Pelaajan väri valittu: {color_name}")
          button_x += 80
        if start_button.collidepoint(x, y):
          game()
        if ohjeet_button.collidepoint(x,y):
          guide_screen()

# ohjeet sivu
def guide_screen():
  running = True
  # nuolinäppäimine kuva ja koko
  arrowKeys = pygame.image.load("arrowkeys.png").convert_alpha()
  arrowKeys = pygame.transform.scale(arrowKeys, (230,150))

  while running:
    screen.fill((50, 50, 50)) # Taustaväri

    # Nuolinäppäin teksti
    arrowKeysText = "Move player with"
    arrowKeysText_x = 60
    arrowKeysText_y = 150
    arrowKeysText = font.render(arrowKeysText, True, (255,255,255))
    arrowKeysText = pygame.transform.rotate(arrowKeysText, 30)
    screen.blit(arrowKeysText, (arrowKeysText_x, arrowKeysText_y))
    

    # Ohjeet vasemmassa yläkulmassa
    ohjeText = """
  
    Avoid obstacles and walls.
    
    Eat 10 foods to advance to the
    next level.
    
    There are 5 levels and the last one
    is endless!
    """
    lines = ohjeText.split("\n")
    x_margin = 400
    y_start = 40
    line_spacing = 50
    y = y_start
    for line in lines:
      rendered_text = font.render(line, True, (255, 255, 255))
      x = x_margin
      screen.blit(rendered_text, (x, y))
      y += line_spacing

    # BACK-nappula
    back_button = pygame.Rect(50, 500, 120, 50)
    pygame.draw.rect(screen, (211, 211, 211), back_button, border_radius=15)
    back_text = font.render("BACK", True, (0, 0, 0))
    text_x = back_button.x + (back_button.width - back_text.get_width()) // 2
    text_y = back_button.y + (back_button.height - back_text.get_height()) // 2
    screen.blit(back_text, (text_x, text_y))

    screen.blit(arrowKeys, (80,230))
    clock.tick(30)
    pygame.display.flip()
      
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
      if back_button.collidepoint(x,y):
        start_screen()

# Peli
def game():
 
  # Ruoka muuttujat
  foodColor=(254, 141, 77)
  foodSize=15
  ruokaOlemassa = 0
  new_food = None
  
  # Pelaajan asetukset
  player_size = 40
  player_xPosition, player_yPosition = WIDTH//2, HEIGHT//2 # Pelaajan alku position on pelin kentän keskellä
  player_speed = 5
  player_variable_x=0 # Tämä on pelaajan muuttuvat x ja y positiot jotka muuttavat oikeaa x ja y:tä
  player_variable_y=0 # Tämä on pelaajan muuttuvat x ja y positiot jotka muuttavat oikeaa x ja y:tä

  #pelin score 
  score = 0
  score_increment = 1

  running = True
  game_over = False
  
  while running:
    screen.fill((255, 255, 255)) # Täytetään näyttö valkoiseksi
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 10) # Piirretään reunat mustaksi
    
    # Piirrä pelaaja
    player = pygame.draw.rect(screen, player_color, (player_xPosition, player_yPosition, player_size, player_size))
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      
    if not game_over:
      player_xPosition += player_variable_x # Päivitetään pelaajan sijaintia koko ajan, jotta pelaaja on koko ajan liikkeessä
      player_yPosition += player_variable_y
    
      keys = pygame.key.get_pressed()
      if keys[pygame.K_LEFT]:
        player_variable_x = -player_speed # Aina nappia painaessa pelaaja vaihtaa suuntaa toiseen ja lopettaa vauhdin toisessa.
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
      
      # Jos ruokaa ei ole spawnaa yksi.
      if ruokaOlemassa == 0:
        x = random.randint(50, WIDTH-50)
        y = random.randint(50, HEIGHT-50)
        new_food = pygame.Rect(x,y,foodSize,foodSize)
        ruokaOlemassa = 1
      # Jos pelaaja osuu ruokaan poistaa se aikaisemman ruoan ja spawnaa uuden.
      if player.colliderect(new_food):
        print("syöty")
        score += score_increment  # Lisää pistettä ruokaa syödessä
        ruokaOlemassa = 0
    
      # Tarkistetaan, tuleeko törmäyksiä seinien kanssa, jos tulee, peli loppuu=True
      if player_xPosition <= 10 or player_xPosition + player_size >= WIDTH - 10 or player_yPosition <= 10 or player_yPosition + player_size >= HEIGHT - 10:
        game_over = True
      
      # Jos new_food True niin piirrä ruoka näytölle.
      if new_food:
        pygame.draw.rect(screen, foodColor, new_food)


      # Tekstin renderöinti
    text_left = font.render("Life", True, (0, 0, 0))
    text_middle = font.render("Taso 1", True, (0, 0, 0))  # Väri (mustaa)
    text_right = font.render(f"Score: {score}" , True, (0, 0, 0))
    
    
    # Piirrä teksti ruudulle (esimerkiksi ylhäällä)
    screen.blit(text_left, ( 20, 20)) # Teksti keskitettynä
    screen.blit(text_middle, (WIDTH // 2 - text_middle.get_width() // 2, 20))
    screen.blit(text_right, (WIDTH - text_right.get_width() - 20, 20))
    
    if game_over:
      game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0)) # game over fontti
      screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    
    pygame.display.flip()
    clock.tick(30)
# kutsu aloitusnäyttöä
start_screen()
 
# pelaajan valitsema väri
print("Pelaajan valitsema väri:", player_color)

# Sulje peli
pygame.quit()

