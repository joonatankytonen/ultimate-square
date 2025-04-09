from src.init_pygame import *

class Player:
  def __init__(self, x=WIDTH//2, y=HEIGHT//2, var_x=0, var_y=0, width=40, height=40, color=(255, 0, 0), speed=5):
      self.rect = pygame.Rect(x, y, width, height)
      self.color = color
      self.active = True
      self.speed = speed
      self.life = 3
      self.var_x = var_x
      self.var_y = var_y
      self.exploding = False
      self.explo_index = 0 
      self.exploAnim = [pygame.image.load(f'anims/explosion_animation/{i}.png') for i in range(1, 9)]
      self.explosion_timer = 0
      self.explosion_pos = (x, y)

  def move(self, keys):
      if not self.exploding: # Jos räjähdys animaatio ei pyöri niin pelaaja voi liikkua
          self.rect.x += self.var_x
          self.rect.y += self.var_y

          if keys[pygame.K_LEFT] or keys[pygame.K_a]:
              self.var_x = -self.speed
              self.var_y = 0
          elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
              self.var_x = self.speed
              self.var_y = 0
          elif keys[pygame.K_UP] or keys[pygame.K_w]:
              self.var_x = 0
              self.var_y = -self.speed
          elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
              self.var_x = 0
              self.var_y = self.speed

  def kill(self):
      self.active = False
      self.exploding = True
      self.explo_index = 0
      self.explosion_timer = pygame.time.get_ticks()
      self.explosion_pos = (self.rect.x, self.rect.y) # Tallennetaan pelaajan kuoleman hetkinen position jossa räjähdys animaatio tulee pyörimään
      self.life -= 1

  def draw(self, screen):
      if self.active and not self.exploding:
          pygame.draw.rect(screen, self.color, self.rect)
      elif self.exploding:
          self.playExplosion(screen) # Kun pelaaja piirretään ja jos explosion flag on totta niin tulee räjähdys animaatio

  def playExplosion(self, screen):
      now = pygame.time.get_ticks()
      if now - self.explosion_timer > 50:
          self.explosion_timer = now
          if self.explo_index < len(self.exploAnim):
              img = self.exploAnim[self.explo_index]
              screen.blit(img, (self.explosion_pos[0], self.explosion_pos[1]))
              self.explo_index += 1
          else:
              self.exploding = False
              self.active = True

  def startPosition(self):
      self.rect.x = WIDTH// 2 - self.rect.width // 2
      self.rect.y = HEIGHT// 2 - self.rect.height // 2