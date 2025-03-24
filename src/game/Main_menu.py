from . import Game
import os
import json
from init_pygame import *
import game.Game as elama

# HAKEMISTON MÄÄRITYS highscore.json tiedostolle
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
high_score_file = os.path.join(BASE_DIR, "highscore.json")

# Fontin luominen
font = pygame.font.Font(None, 20)

# logoloinen tähän
game_title = pygame.image.load("imgs/ultimate square 2.jpg")

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

def load_high_scores():
    # Käytetään samaa polkua joka määriteltiin ylhäällä
    try:
        with open(high_score_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def main_menu():
  global player_color
  running = True
  selected_color_index = 0  # uutta: valittu väri nuolinäppäimillä
  color_keys = list(colors.keys())

  while running:
    high_scores = load_high_scores()
    screen.fill((50, 50, 50)) # Taustaväri
    
    # TOP 5 High Scores -otsikko
    high_score_title = font.render("TOP 5 High Scores", True, (255, 255, 255))
    screen.blit(high_score_title, (WIDTH // 2 - high_score_title.get_width() // 2, 50))
    
    # Lista alkaa otsikon alta
    y_offset = 90
    for index, entry in enumerate(high_scores):
      score_text = small_font.render(f"{index+1}. {entry['name']}: {entry['score']}", True, (255, 255, 255))
      screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, y_offset))
      y_offset += 30

    # Värivalinnan otsikko ja nappulat keskellä
    color_text_y = y_offset + 30
    color_text = font.render("Choose your player color:", True, (253, 253, 253))
    screen.blit(color_text, (WIDTH // 2 - color_text.get_width() // 2, color_text_y))
    
    # Värivalintanapit keskelle
    button_x = WIDTH // 2 - (len(colors) * 80) // 2
    button_y = color_text_y + 50
    for idx, (color_name, color_value) in enumerate(colors.items()):
      # Piirrä väri-nappi
      pygame.draw.rect(screen, color_value, (button_x, button_y, 60, 60))

      # Jos tämä väri on valittu nuolinäppäimillä, piirrä korostuskehys
      if idx == selected_color_index:
        pygame.draw.rect(screen, (255, 255, 255), (button_x - 5, button_y - 5, 70, 70), 3)

      # Piirrä värin nimi
      text = small_font.render(color_name, True, (255, 255, 255))
      screen.blit(text, (button_x, button_y + 65))
      button_x += 90

    # Painikkeita vielä vähän alemmas
    button_y += 130

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

      # Hiiren klikkaukset (vanha toiminta säilyy)
      elif event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        button_x = WIDTH // 2 - (len(colors) * 80) // 2
        button_y = color_text_y + 40
        for idx, (color_name, color_value) in enumerate(colors.items()):
          if button_x < x < button_x + 60 and button_y < y < button_y + 60:
            player_color = color_value
            selected_color_index = idx  # päivitetään myös nuoliohjaus
            print(f"Pelaajan väri valittu: {color_name}")
          button_x += 80
        if start_button.collidepoint(x, y):
          player_name = ask_player_name()
          Game.game(WIDTH=WIDTH, HEIGHT=HEIGHT, screen=screen, pygame=pygame,
                    player_color=player_color, font=font, clock=clock,
                    main_menu=main_menu, player_name=player_name)
        if ohjeet_button.collidepoint(x, y):
          guide_screen()

      # Nuolinäppäimet ja ENTER - näppäimet
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          selected_color_index = (selected_color_index - 1) % len(colors)
          print(f"Valittu väri: {color_keys[selected_color_index]}")
        elif event.key == pygame.K_RIGHT:
          selected_color_index = (selected_color_index + 1) % len(colors)
          print(f"Valittu väri: {color_keys[selected_color_index]}")
        elif event.key == pygame.K_RETURN:
          player_color = colors[color_keys[selected_color_index]]
          print(f"Pelaajan väri valittu: {color_keys[selected_color_index]}")
          player_name = ask_player_name()
          Game.game(WIDTH=WIDTH, HEIGHT=HEIGHT, screen=screen, pygame=pygame,
                    player_color=player_color, font=font, clock=clock,
                    main_menu=main_menu, player_name=player_name)

def ask_player_name():
    player_name = ""
    active = True

    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 60)  # Leveämpi laatikko
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_active

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_name.strip() != "":
                        return player_name
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        screen.fill((30, 30, 30))

        # Otsikko
        text = font.render("Enter your nickname and press ENTER", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))

        # Lasketaan fontin koko dynaamisesti
        max_font_size = 64
        min_font_size = 28
        font_size = max_font_size

        # Pienennetään fonttia jos ei mahdu laatikkoon
        fits = False
        while not fits and font_size >= min_font_size:
            font_input = pygame.font.Font(None, font_size)
            txt_surface = font_input.render(player_name, True, (255, 255, 255))
            if txt_surface.get_width() <= input_box.width - 20:
                fits = True
            else:
                font_size -= 2  # pienennetään fonttia, kunnes mahtuu

        # Piirrä laatikko
        pygame.draw.rect(screen, color, input_box, 2)

        # Keskitetään teksti laatikkoon
        text_x = input_box.x + (input_box.width - txt_surface.get_width()) // 2
        text_y = input_box.y + (input_box.height - txt_surface.get_height()) // 2
        screen.blit(txt_surface, (text_x, text_y))

        pygame.display.flip()
        clock.tick(30)

# ohjeet sivu
def guide_screen():
    running = True
    # nuolinäppäimine kuva ja koko
    arrowKeys = pygame.image.load("imgs/arrowkeys.png").convert_alpha()
    arrowKeys = pygame.transform.scale(arrowKeys, (230, 150))

    while running:
        screen.fill((50, 50, 50)) # Taustaväri

        # Nuolinäppäin teksti
        arrowKeysText = "Move player with"
        arrowKeysText_x = 60
        arrowKeysText_y = 150
        arrowKeysText = font.render(arrowKeysText, True, (255, 255, 255))
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

        screen.blit(arrowKeys, (80, 230))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
            if back_button.collidepoint(x, y):
                main_menu()

# Ensimmäinen aloitussivu (vain logo ja "Press ENTER")
def logo_splash():
    running = True
    text_visible = True  # Teksti vilkkuu
    text_timer = 0

    while running:
        screen.fill((0, 0, 0))  # Musta tausta

        # Näytetään pelin logo koko ruudulla, jos löytyy
        if game_title:
            screen.blit(pygame.transform.scale(game_title, (800, 400)), (50, 100))

        # Vilkkuva teksti "Press ENTER"
        if text_visible:
            enter_text = font.render("Press ENTER", True, (255, 255, 255))
            screen.blit(enter_text, (WIDTH // 2 - enter_text.get_width() // 2, HEIGHT - 100))

        pygame.display.flip()
        clock.tick(30)  # 30 FPS

        # Tekstin vilkkuminen
        text_timer += 1
        if text_timer % 30 == 0:  # Joka 30 framea vaihtuu näkyvyys
            text_visible = not text_visible

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER-painike
                    main_menu()

def save_high_score(score):
    """Tallenna pelaajan tulos tiedostoon high_score.txt"""
    global high_score
    if score > high_score:
        high_score = score
        with open("high_score.txt", "w") as file:
            file.write(str(score))
            print(f"Uusi high score: {score}")
    else:
        print(f"Pelaajan tulos: {score}")
