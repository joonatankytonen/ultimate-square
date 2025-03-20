import random 
from classes.Player import Player
from classes.Food import Food
from game.Main_menu import *
from init_pygame import *

# Peli
def game(WIDTH, HEIGHT, screen, pygame, player_color, font, clock, main_menu):

  game_over_font = pygame.font.Font(None, 60)
  
  # elämä
  elama = 3

  # sydämmen kuvat
  heart_image = pygame.image.load("imgs/heart.png")
  heart_image = pygame.transform.scale(heart_image, (30, 30))  
  heart_rect = heart_image.get_rect()

  # Ruoka muuttujat
  food = None
  
  # Luo pelaaja
  player = Player(color=(player_color))
  
  # Pelin score 
  score = 0
  score_increment = 1

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

  while running:
    screen.fill((255, 255, 255))  # Täytetään näyttö valkoiseksi
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 10)  # Piirretään reunat mustaksi

    # Piirrä esteet
    for obstacle in obstacles:
        pygame.draw.rect(screen, (128, 0, 128), obstacle)

    # Piirrä pelaaja
    player.draw(screen=screen)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
        
      # Jos taso on vaihtumassa, odota Enter-näppäintä
      if level_up and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        level_up = False
        obstacles = generate_obstacles(level, WIDTH, HEIGHT, player)  # Uudet esteet levelin alussa
        print(f"Taso {level} alkaa!")
      
    if not game_over and not level_up:
      keys = pygame.key.get_pressed()
      player.move(keys=keys)

      # Tarkistetaan törmäykset esteisiin
      for obstacle in obstacles:
          if player.rect.colliderect(obstacle):
              elama -= 1
              print(f"Osuit esteeseen! Elämä jäljellä: {elama}")
              player.rect.x = WIDTH // 2 - player.rect.width // 2
              player.rect.y = HEIGHT // 2 - player.rect.height // 2
              if elama <= 0:
                  game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
                  screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
                  pygame.display.update()
                  pygame.time.wait(2000)
                  main_menu()
                  return

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

      # Tarkistetaan, tuleeko törmäyksiä seinien kanssa
      if player.rect.x <= 10 or player.rect.x + player.rect.width >= WIDTH - 10 or player.rect.y <= 10 or player.rect.y + player.rect.height >= HEIGHT - 10:
        elama -= 1
        print(f"Elämä jäljellä: {elama}")
        # Uudelleensijoittaminen kuoleman jälkeen 
        player.rect.x = WIDTH // 2 - player.rect.width// 2
        player.rect.y = HEIGHT // 2 - player.rect.height// 2
        
        if elama <= 0:
            game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
            pygame.display.update()  # Update display immediately to show the text
            pygame.time.wait(2000)
            main_menu()
            return

    # Piirrä Sydämmet
    draw_health_bar(heart_image=heart_image, heart_rect=heart_rect, elama=elama)

    # Tekstin renderöinti
    text_middle = font.render(f"Taso {level}", True, (0, 0, 0))  # Väri (mustaa)
    text_right = font.render(f"Score: {score}" , True, (0, 0, 0))
    
    # Piirrä teksti ruudulle (esimerkiksi ylhäällä)
    screen.blit(text_middle, (WIDTH // 2 - text_middle.get_width() // 2, 20))
    screen.blit(text_right, (WIDTH - text_right.get_width() - 20, 20))
    
    # Jos taso vaihtuu
    if level_up:
      level_up_text = game_over_font.render(f"Taso {level} alkaa!", True, (0, 128, 0))
      instruction_text = font.render("Paina ENTER jatkaaksesi", True, (0, 0, 0))
      screen.blit(level_up_text, (WIDTH // 2 - level_up_text.get_width() // 2, HEIGHT // 2 - 50))
      screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()
    clock.tick(30)

def switch_level(score, level, player, player_speed):
  level_up = False
  obstacles = []
  if level < 5 and score == 10:
      print("Level vaihtuu")
      level+=1
      score=0
      level_up = True
      player_speed += 2 # nopeus kasvaa
      
      player.speed = player_speed
      
      # Tason vaihtuessa pelaaja aloittaa keskeltä
      player.rect.x = WIDTH // 2 - player.rect.width // 2
      player.rect.y = HEIGHT // 2 - player.rect.height // 2
      
      print(f"Taso {level} ja pelaajan nopeus {player.speed}")
      # Generoidaan uudet esteet
      obstacles = generate_obstacles(level, WIDTH, HEIGHT, player)
      
  return score, level, level_up, player_speed, obstacles


# Funktio esteiden generointiin
def generate_obstacles(level, WIDTH, HEIGHT, player):
    obstacles = []
    if level >= 2:  # Esteitä vain level 2 alkaen
        for _ in range(level):  # Lisää yhtä monta estettä kuin level
            while True:
                x = random.randint(50, WIDTH - 150)
                y = random.randint(50, HEIGHT - 50)
                obstacle = pygame.Rect(x, y, 100, 30)  # Kiinteän kokoinen este
                
                # Varmistetaan, ettei este ole pelaajan aloituspaikalla
                player_area = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 - 50, 100, 100)
                if not obstacle.colliderect(player_area):
                    obstacles.append(obstacle)
                    break
    return obstacles

# Tason vaihto - päivitetty esteiden luonti mukaan
def switch_level(score, level, player, player_speed, WIDTH, HEIGHT):
    level_up = False
    obstacles = []
    if level < 5 and score == 10:
        print("Level vaihtuu")
        level += 1
        score = 0
        level_up = True
        player_speed += 1  # Nopeus kasvaa
        
        # Pelaaja aloittaa keskeltä
        player.rect.x = WIDTH // 2 - player.rect.width // 2
        player.rect.y = HEIGHT // 2 - player.rect.height // 2
        
        # Generoidaan uudet esteet
        obstacles = generate_obstacles(level, WIDTH, HEIGHT, player)

    return score, level, level_up, player_speed, obstacles
  
def draw_health_bar(heart_image, heart_rect, elama):
  font = pygame.font.Font(None, 36)
  """Piirtää 'Life:' tekstin ja sen viereen sydämet elämien mukaan."""
  text_left = font.render("Life:", True, (0, 0, 0))
  screen.blit(text_left, (20, 20))  # Näytetään "Life:" teksti

  # Lasketaan sydänten aloituspaikka suhteessa tekstiin
  text_width = text_left.get_width()
  hearts_x_start = 30 + text_width  # Siirretään sydämet tekstin oikealle puolelle

  for i in range(elama):  # Piirretään niin monta sydäntä kuin on elämiä
      screen.blit(heart_image, (hearts_x_start + i * (heart_rect.width + 5), 15))  # Sydämet tekstin jälkeen