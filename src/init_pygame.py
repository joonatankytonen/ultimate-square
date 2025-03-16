import pygame

pygame.init()

# Ikkunan koko | Ikkunan nimi
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Square")

clock = pygame.time.Clock()
