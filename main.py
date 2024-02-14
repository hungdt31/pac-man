import pygame

pygame.init()

WIDTH = 900
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf',20)

run = True
while run:
  timer.tick(fps)
  screen.fill('black')
  # setting up pygame
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  
  pygame.display.flip()
pygame.quit()