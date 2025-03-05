from init_pygame import *

class Player:
  def __init__(self, x=WIDTH/2, y=HEIGHT/2, var_x=0, var_y=0, width=40, heigt=40, color=(255, 0, 0), speed=5):
    self.rect = pygame.Rect(x,y,width, heigt)
    self.color = color
    self.speed = speed
    self.var_x = var_x
    self.var_y = var_y

  def move(self, keys):
    self.rect.x += self.var_x
    self.rect.y += self.var_y

    if keys[pygame.K_LEFT]:
      self.var_x = -self.speed # Aina nappia painaessa pelaaja vaihtaa suuntaa toiseen ja lopettaa vauhdin toisessa.
      self.var_y = 0
    if keys[pygame.K_RIGHT]:
      self.var_x = self.speed
      self.var_y = 0
    if keys[pygame.K_UP]:
      self.var_x = 0
      self.var_y = -self.speed
    if keys[pygame.K_DOWN]:
      self.var_x = 0
      self.var_y = self.speed

  def draw(self, screen):
    pygame.draw.rect(screen, self.color, self.rect)
