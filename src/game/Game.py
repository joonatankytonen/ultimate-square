import random  
import json
import os
from src.classes.Player import Player
from src.classes.Food import Food
from src.game.Main_menu import *
from src.init_pygame import *
import pygame.mixer


# Tiedostopolku highscore.json:iin
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
high_score_file = os.path.join(BASE_DIR, "../highscore.json")

# Peli
def game(WIDTH, HEIGHT, screen, pygame, player_color, font, clock, main_menu, player_name):  # <-- Lisätty player_name!
  
  pygame.mixer.init()
  
  print(f"pelaajan nimi on {player_name}")
  mainFont = pygame.font.Font(None, 60)

  # sydämmen kuvat
  heart_image = pygame.image.load("imgs/heart.png")
  heart_image = pygame.transform.scale(heart_image, (30, 30))  
  heart_rect = heart_image.get_rect()

  # Ruoka muuttujat
  food = None
  
  # Luo pelaaja
  player = Player(color=player_color)
  player.rect.x = WIDTH // 2 - player.rect.width // 2
  player.rect.y = HEIGHT // 2 - player.rect.height // 2
  
  # Pelin score 
  score = 0
  score_increment = 1
  
  # Lataa highscoret tiedostosta
  try:
    with open(high_score_file, "r") as file:
      high_scores = json.load(file)
  except (FileNotFoundError, json.JSONDecodeError):
    high_scores = []
       
  # Pelin level
  level = 1
  
  # Tasonvaihto lippu
  level_up = False
  
  # Pelaajan aloitusnopeus
  player_speed = 5

  # Esteet (tyhjä alussa, generoidaan level 2 alkaen)
  obstacles = generate_obstacles(level, WIDTH, HEIGHT, player)

  running = True
  game_over = False
  new_high_score = False
  new_high_score_timer = 0
  
  toista_musiikki(level)
  
  while running:
    screen.fill((220, 220, 220))  # Täytetään näyttö valeanharmaaksi
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 10)  # Piirretään reunat mustaksi
    
     # Piirrä esteet
    # Esteiden ulkonäkö – tasosta riippuen
    # Esteiden ulkonäkö (Level 5: vilkkuvat)
    for obstacle in obstacles:
      if level == 5:
        time = pygame.time.get_ticks()
        visible = (time // 1000) % 3 != 2  # Näkyy 2s, piilossa 1s

        if visible:
            red = 128 + (time // 100 % 127)
            green = 64 + ((time // 100 * 2) % 128)
            blue = 255 - (time // 100 % 128)
            special_color = (red % 256, green % 256, blue % 256)
            pygame.draw.rect(screen, special_color, obstacle, border_radius=10)
      else:
          pygame.draw.rect(screen, (128, 0, 128), obstacle)


    # Piirrä pelaaja
    player.draw(screen=screen)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
        
      # Jos taso on vaihtumassa, odota Enter-näppäintä
      if level_up and event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
        level_up = False
        print(f"Taso {level} alkaa!")
        toista_musiikki(level)
      
    if not game_over and not level_up:
      keys = pygame.key.get_pressed()
      player.move(keys=keys)

      # Tarkistetaan törmäykset esteisiin
      for obstacle in obstacles:
          if player.rect.colliderect(obstacle):
              player.kill()
              print(f"Osuit esteeseen! Elämä jäljellä: {player.life}")
              player.rect.x = WIDTH // 2 - player.rect.width // 2
              player.rect.y = HEIGHT // 2 - player.rect.height // 2
              if player.life <= 0:
                elematLoppu(player_name=player_name, score=score, main_menu=main_menu, player_color=player_color)
      # Jos ruokaa ei ole, spawnaa yksi
      if food is None:
          while True:
            x = random.randint(50, WIDTH-50)
            y = random.randint(50, HEIGHT-50)
            new_food = Food(x, y)
            # Varmistetaan, ettei ruoka ole esteen päällä
            if not any(obstacle.colliderect(new_food.rect) for obstacle in obstacles):
              food = new_food  # Tallennetaan ruoka pysyvästi
              break

      # Jos ruoka on olemassa, piirrä se
      if food:
        food.draw(screen=screen)

      # Jos pelaaja osuu ruokaan, poista se ja spawnaa uusi
      if food and player.rect.colliderect(food.rect):
        print("syöty")
        score += score_increment  # Lisää pistettä ruokaa syödessä
        score, level, level_up, player_speed, new_obstacles = switch_level(score, level, player, player_speed, WIDTH, HEIGHT)
        food = None  # Ruoka poistetaan, jotta uusi voidaan spawnaa
        
        # Päivitä esteet vain jos taso vaihtuu
        if level_up:
            obstacles = new_obstacles
            pygame.mixer.music.stop()

      # Tarkistetaan, tuleeko törmäyksiä seinien kanssa
      if player.rect.x <= 5 or player.rect.x + player.rect.width >= WIDTH - 5 or player.rect.y <= 5 or player.rect.y + player.rect.height >= HEIGHT - 5:
        player.kill()
        print(f"Elämä jäljellä: {player.life}")
        # Uudelleensijoittaminen kuoleman jälkeen 
        player.rect.x = WIDTH // 2 - player.rect.width// 2
        player.rect.y = HEIGHT // 2 - player.rect.height// 2
        
        if player.life <= 0:
          elematLoppu(player_name=player_name, score=score, main_menu=main_menu, player_color=player_color)


    draw_health_bar(heart_image=heart_image, heart_rect=heart_rect, elama=player.life)

    # Tekstin renderöinti
    text_middle = font.render(f"Taso {level}", True, (0, 0, 0))  # Väri (mustaa)
    text_right = font.render(f"Score: {score}" , True, (0, 0, 0))
    
    # Piirrä teksti ruudulle (esimerkiksi ylhäällä)
    screen.blit(text_middle, (WIDTH // 2 - text_middle.get_width() // 2, 20))
    screen.blit(text_right, (WIDTH - text_right.get_width() - 20, 20))
    
    # High Score näkyville (suurin pisteistä top 5 listalta)
    highest_score = max([entry['score'] for entry in high_scores], default=0)
    high_score_text = font.render(f"High Score: {highest_score}", True, (0, 0, 0))
    screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 20, 50))
    
    if new_high_score and pygame.time.get_ticks() - new_high_score_timer < 1000: 
      new_high_score_text = font.render("Uusi High Score!", True, (255, 0, 0))
      screen.blit(new_high_score_text, (WIDTH // 2 - new_high_score_text.get_width() // 2, 50))
      
    # Jos taso vaihtuu
    # Jos päästään tasolle 5 -> Endless Mode teksti
    if level_up:
      if level == 5:
        large_font = pygame.font.Font(None, 100)
        level_up_text = large_font.render("ENDLESS MODE", True, (192, 0, 0))
      else:
        level_up_text = mainFont.render(f"Taso {level} alkaa!", True, (0, 128, 0))
        
      instruction_text = font.render("Paina SPACE jatkaaksesi", True, (0, 0, 0))
      screen.blit(level_up_text, (WIDTH // 2 - level_up_text.get_width() // 2, HEIGHT // 2 - 50))
      screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()
    clock.tick(30)

def elematLoppu(player_name, score, main_menu, player_color):
  pygame.mixer.music.stop()
  game_over = True
  save_high_score(player_name, score)  # <-- Tallennus
  new_high_score = True
  new_high_score_timer = pygame.time.get_ticks()
  pygame.display.update()  # Update display immediately to show the text
  pygame.time.wait(500)
  popUpWindow(main_menu=main_menu, player_name=player_name, player_color=player_color)

def popUpWindow(main_menu, player_name, player_color):
  game_over_font = pygame.font.Font(None, 60)
  font = pygame.font.Font(None, 36)

  # PopUp window koko
  popUpWIDTH=350
  popUpHEIGTH=350

  # Nappi muuttujia
  buttonWidth = 120
  buttonHeigth = 50
  buttonColor = pygame.Color(232, 221, 194)
  buttonBorderColor = pygame.Color(117, 117, 117)
  buttonBorderRadius = 15

  # Taustan himmennys juttuja
  dimScreenColor = pygame.Color(30,30,30,5)
  dimSurf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
  dimSurf.fill(dimScreenColor)
  
  while True:
    pygame.display.update()

    # Himmennä tausta
    screen.blit(dimSurf,(0,0))

    #Pop-Up window and game over text
    popup_rect = pygame.Rect(WIDTH//2-popUpWIDTH//2, HEIGHT//2-popUpHEIGTH//2, popUpWIDTH, popUpHEIGTH)
    pygame.draw.rect(screen, (200, 200, 200), popup_rect, border_radius=10)
    pygame.draw.rect(screen, (0, 0, 0), popup_rect, 2, border_radius=10)  # Border
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (popUpWIDTH-26, popUpHEIGTH //2))

    # again-nappula
    again_button = pygame.Rect(WIDTH//2-popUpWIDTH//2+115, HEIGHT//2-popUpHEIGTH//2+130,buttonWidth, buttonHeigth)
    pygame.draw.rect(screen, buttonColor, again_button, border_radius=buttonBorderRadius)
    pygame.draw.rect(screen, buttonBorderColor, again_button, 2, border_radius=buttonBorderRadius)
    start_text = font.render("AGAIN", True, (0, 0, 0))
    text_x = again_button.x + (again_button.width - start_text.get_width()) // 2
    text_y = again_button.y + (again_button.height - start_text.get_height()) // 2
    screen.blit(start_text, (text_x, text_y))

    # menu-nappula
    menu_button = pygame.Rect(WIDTH//2-popUpWIDTH//2+115, HEIGHT//2-popUpHEIGTH//2+190, buttonWidth, buttonHeigth)
    pygame.draw.rect(screen, buttonColor, menu_button, border_radius=buttonBorderRadius)
    pygame.draw.rect(screen, buttonBorderColor, menu_button, 2, border_radius=buttonBorderRadius)
    start_text = font.render("MENU", True, (0, 0, 0))
    text_x = menu_button.x + (menu_button.width - start_text.get_width()) // 2
    text_y = menu_button.y + (menu_button.height - start_text.get_height()) // 2
    screen.blit(start_text, (text_x, text_y))

    # lopeta-nappula
    quit_button = pygame.Rect(WIDTH//2-popUpWIDTH//2+115, HEIGHT//2-popUpHEIGTH//2+250, buttonWidth, buttonHeigth)
    pygame.draw.rect(screen, buttonColor, quit_button, border_radius=buttonBorderRadius)
    pygame.draw.rect(screen, buttonBorderColor, quit_button, 2, border_radius=buttonBorderRadius)
    start_text = font.render("QUIT", True, (0, 0, 0))
    text_x = quit_button.x + (quit_button.width - start_text.get_width()) // 2
    text_y = quit_button.y + (quit_button.height - start_text.get_height()) // 2
    screen.blit(start_text, (text_x, text_y))
    

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        x,y = event.pos
        if again_button.collidepoint(x,y):
          print("uudestaan")
          game(WIDTH=WIDTH, HEIGHT=HEIGHT, screen=screen, pygame=pygame, player_color=player_color, font=font, clock=clock, main_menu=main_menu, player_name=player_name)
        if menu_button.collidepoint(x,y):
          print("menu")
          main_menu()
        if quit_button.collidepoint(x,y):
          print("quit")   
          pygame.quit()
          exit()

def save_high_score(player_name, score):
  try:
    with open(high_score_file, "r") as file:
      high_scores = json.load(file)
  except (FileNotFoundError, json.JSONDecodeError):
    high_scores = []
    
  high_scores.append({"name": player_name, "score": score})
  high_scores = sorted(high_scores, key=lambda x: x["score"], reverse=True)[:5]
  
  with open(high_score_file, "w") as file:
    json.dump(high_scores, file, indent=2)
    
  print("päivitetyt highscoret:", high_scores)

def switch_level(score, level, player, player_speed, WIDTH, HEIGHT):
  level_up = False
  obstacles = []
  if level < 5 and score != 0 and score % 10 == 0:
    print("Level vaihtuu")
    level+=1
    level_up = True
    player_speed += 1.5 # nopeus kasvaa
    print(f"Taso: {level}, Pelaajan nopeus: {player_speed}")
    
    player.speed = player_speed
    
    # Tason vaihtuessa pelaaja aloittaa keskeltä
    player.rect.x = WIDTH // 2 - player.rect.width // 2
    player.rect.y = HEIGHT // 2 - player.rect.height // 2
    
    # Generoidaan uudet esteet
    obstacles = generate_obstacles(level, WIDTH, HEIGHT, player)
      
  return score, level, level_up, player_speed, obstacles

# Funktio esteiden generointiin
def generate_obstacles(level, WIDTH, HEIGHT, player):
    obstacles = []
    min_distance_from_edge = 80  # ettei tule liian reunaan
    min_distance_between_obstacles = 120  # ettei tule liian lähelle toisiaan
    max_attempts = 100  # ettei jää ikuiseen silmukkaan

    if level >= 2:
        for _ in range(level):
            attempts = 0
            while attempts < max_attempts:
                x = random.randint(min_distance_from_edge, WIDTH - min_distance_from_edge - 100)
                y = random.randint(min_distance_from_edge, HEIGHT - min_distance_from_edge - 30)
                new_obstacle = pygame.Rect(x, y, 100, 30)

                # Ei pelaajan aloituspaikalle
                player_area = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 - 50, 100, 100)

                # Ei liian lähelle muita esteitä
                too_close = any(new_obstacle.colliderect(o.inflate(min_distance_between_obstacles, min_distance_between_obstacles)) for o in obstacles)

                if not new_obstacle.colliderect(player_area) and not too_close:
                    obstacles.append(new_obstacle)
                    break

                attempts += 1
    return obstacles

  
def draw_health_bar(heart_image, heart_rect, elama):
  hearts_x_start = 20# Siirretään sydämet tekstin oikealle puolelle

  for i in range(elama):  # Piirretään niin monta sydäntä kuin on elämiä
      screen.blit(heart_image, (hearts_x_start + i * (heart_rect.width + 5), 15))  # Sydämet tekstin jälkeen
      
def toista_musiikki(level):
  if level == 5:
    pygame.mixer.music.load("music/level5_music.wav")
  else :
    pygame.mixer.music.load("music/level1_4_music.wav")
  pygame.mixer.music.play(-1)
