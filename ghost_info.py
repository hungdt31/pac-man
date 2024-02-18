import pygame
pygame.init()
blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost/red.bmp'), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost/pink.bmp'), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost/blue.bmp'), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost/orange.bmp'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost/powerup.bmp'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost/dead.bmp'), (45, 45))

