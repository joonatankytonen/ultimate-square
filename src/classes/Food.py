from init_pygame import *

class Food:
  def __init__(self,x,y,width=15, height=15, color=(254,141,77)):
    self.rect = pygame.Rect(x,y,width, height)
    self.color = color

  def draw(self, screen):
    pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
