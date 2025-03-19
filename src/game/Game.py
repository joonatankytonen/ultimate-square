import random
from classes.Player import Player
from classes.Food import Food
from game.Main_menu import *
from init_pygame import *

# Peli
def game(WIDTH, HEIGHT, screen, pygame, player_color, font, clock, main_menu):

  game_over_font = pygame.font.Font(None, 60)
  
  #elämä
  elama = 3

  # sydämmen kuvat
  heart_image = pygame.image.load("imgs/heart.png")
  heart_image = pygame.transform.scale(heart_image, (30, 30))  
  heart_rect = heart_image.get_rect()

  # Ruoka muuttujat
  ruokaOlemassa = 0
  new_food = None
  
  # Luo pelaaja
  player = Player(color=(player_color))
  
  #pelin score 
  score = 0
  score_increment = 1

  # pelin level
  level = 1
  
  # Tasonvaihto lippu
  level_up = False
  
  #pelaajan aloitusnopeus
  player_speed = 5

  running = True
  game_over = False

  
  while running:
    screen.fill((255, 255, 255)) # Täytetään näyttö valkoiseksi
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 10) # Piirretään reunat mustaksi
    
    
    # Piirrä pelaaja
    player.draw(screen=screen)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
        
      # Jos taso on vaihtumassa, odota Enter-näppäintä
      if level_up and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        level_up = False
        print(f"Taso {level} alkaa!")
      
    if not game_over and not level_up:
      keys = pygame.key.get_pressed()
      player.move(keys=keys)

      # Jos ruokaa ei ole spawnaa yksi.
      if ruokaOlemassa == 0:
        x = random.randint(50, WIDTH-50)
        y = random.randint(50, HEIGHT-50)
        new_food = True
        food = Food(x,y)
        ruokaOlemassa = 1
        
      # Jos pelaaja osuu ruokaan poistaa se aikaisemman ruoan ja spawnaa uuden.
      if player.rect.colliderect(food):
        print("syöty")
        score += score_increment  # Lisää pistettä ruokaa syödessä
        score, level, level_up, player_speed = switch_level(score, level, player, player_speed)
        ruokaOlemassa = 0
      # Tarkistetaan, tuleeko törmäyksiä seinien kanssa, jos tulee, peli loppuu=True
      if player.rect.x <= 5 or player.rect.x + player.rect.width >= WIDTH - 5 or player.rect.y <= 5 or player.rect.y + player.rect.height >= HEIGHT - 5:
        elama -= 1
        print(f"Elämä jäljellä: {elama}")
        #uudelleen sijoittaminen kuoleman jälkeen 
        player.rect.x = WIDTH // 2 - player.rect.width// 2
        player.rect.y= HEIGHT // 2 -player.rect.height// 2
        
        if elama <= 0:
            game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0)) # game over fontti
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
            pygame.display.update()  # Update display immediately to show the text
            pygame.time.wait(2000)
            main_menu()
            return
      
      # Jos new_food True niin piirrä ruoka näytölle.
      if new_food:
        food.draw(screen=screen)


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
  if level < 5 and score == 10:
      print("Level vaihtuu")
      level+=1
      score=0
      level_up = True
      player_speed += 1 # nopeus kasvaa
      
      # Tason vaihtuessa pelaaja aloittaa keskeltä
      player.rect.x = WIDTH // 2 - player.rect.width // 2
      player.rect.y = HEIGHT // 2 - player.rect.height // 2
      
  return score, level, level_up, player_speed

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

