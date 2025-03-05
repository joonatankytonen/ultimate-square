import random

# Peli
def game(WIDTH, HEIGHT, screen, pygame, player_color, font, clock):


  game_over_font = pygame.font.Font(None, 60)
 
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

  # pelin level
  level = 1
  
  # Tasonvaihto lippu
  level_up = False

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
        
      # Jos taso on vaihtumassa, odota Enter-näppäintä
      if level_up and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        level_up = False
        print(f"Taso {level} alkaa!")
      
    if not game_over and not level_up:
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
        score, level, level_up = switch_level(score, level)
        ruokaOlemassa = 0
        

      # Tarkistetaan, tuleeko törmäyksiä seinien kanssa, jos tulee, peli loppuu=True
      if player_xPosition <= 10 or player_xPosition + player_size >= WIDTH - 10 or player_yPosition <= 10 or player_yPosition + player_size >= HEIGHT - 10:
        game_over = True
      
      # Jos new_food True niin piirrä ruoka näytölle.
      if new_food:
        pygame.draw.rect(screen, foodColor, new_food)


      # Tekstin renderöinti
    text_left = font.render("Life", True, (0, 0, 0))
    text_middle = font.render(f"Taso {level}", True, (0, 0, 0))  # Väri (mustaa)
    text_right = font.render(f"Score: {score}" , True, (0, 0, 0))
    
    
    # Piirrä teksti ruudulle (esimerkiksi ylhäällä)
    screen.blit(text_left, ( 20, 20)) # Teksti keskitettynä
    screen.blit(text_middle, (WIDTH // 2 - text_middle.get_width() // 2, 20))
    screen.blit(text_right, (WIDTH - text_right.get_width() - 20, 20))
    
    # Jos peli on ohi
    if game_over:
      game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0)) # game over fontti
      screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    
    # Jos taso vaihtuu
    if level_up:
      level_up_text = game_over_font.render(f"Taso {level} alkaa!", True, (0, 128, 0))
      instruction_text = font.render("Paina ENTER jatkaaksesi", True, (0, 0, 0))
      screen.blit(level_up_text, (WIDTH // 2 - level_up_text.get_width() // 2, HEIGHT // 2 - 50))
      screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()
    clock.tick(30)

def switch_level(score, level):
  level_up = False
  if level < 5 and score == 10:
      print("Level vaihtuu")
      level+=1
      score=0
      level_up = True
  return score, level, level_up