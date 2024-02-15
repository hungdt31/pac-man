import pygame
import math
from player_info import direction, counter, player_X , player_Y , player_images, turns_allowed
from board import boards
pygame.init()

WIDTH = 900
HEIGHT = 750
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf',20)
level = boards
color = 'blue'
PI = math.pi
flicker = False

for i in range(1,5):
  player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player/{i}.bmp'),(40, 40)))
def draw_board():
  # chia screen thành các ô vuông nhỏ có width = num1 và height = num2
  num1 = ((HEIGHT - 50) // 32)
  num2 = (WIDTH // 30)

  for i in range(len(level)):
    for j in range(len(level[i])):
      if level[i][j] == 1:
        # tham số thứ 3 được xem như tọa độ của tâm hình tròn
        pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 + (0.5 * num1)), 4)
      if level[i][j] == 2 and not flicker:
        pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 + (0.5 * num1)), 10)
      if level[i][j] == 3:
        # vẽ đường thẳng : tham số thứ 3 và 4 lần lượt là tọa độ của điểm bắt đầu và kết thúc
        # tham số cuối cùng là độ dày của đường thẳng
        pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                        (j * num2 + (0.5 * num2), i * num1 + num1), 3)
      if level[i][j] == 4:
        pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                        (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
      if level[i][j] == 5:
        # tham số thứ 3 là hình chữ nhật chứa arc có gồm tọa độ góc trái trên và góc phải dưới
        pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], 0, PI / 2, 3)
      if level[i][j] == 6:
        pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
      if level[i][j] == 7:
        pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.35 * num1)), num2, num1], PI, 3 * PI / 2, 3)
      if level[i][j] == 8:
        pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.42)), (i * num1 - (0.42 * num1)), num2, num1], 3* PI / 2, 2 * PI, 3)
      # draw gate
      if level[i][j] == 9:
        pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                          (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

def draw_player():
  # 0 - RIGHT, 1 - LEFT, 2 - UP, 3 - DOWN
  if direction == 0:
    screen.blit(player_images[counter // 5], (player_X, player_Y))
  elif direction == 1:
    screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_X, player_Y))
  elif direction == 2:
    screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_X, player_Y))
  elif direction == 3:
    screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_X, player_Y))

def check_position(center_X, center_Y):
  turns = [False] * 4
  num1 = ((HEIGHT - 50) // 32)
  num2 = (WIDTH // 30)
  num3 = 15
  if center_X // 30 < 29:
    if direction == 0:
      print('check check')
  else:
    turns[0] = True
    turns[1] = True
  return turns

run = True

while run:
  timer.tick(fps)
  screen.fill('black')
  if counter < 19:
    counter += 1
    if counter > 3:
      flicker = False
  else:
    counter = 0
    flicker = True
  draw_board()
  draw_player()
  center_X = player_X + 21
  center_Y = player_Y + 21
  pygame.draw.circle(screen,'white',(center_X, center_Y), 4)
  turns_allowed = check_position(center_X, center_Y)

  # setting up pygame
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RIGHT:
        direction = 0
      if event.key == pygame.K_LEFT:
        direction = 1
      if event.key == pygame.K_UP:
        direction = 2
      if event.key == pygame.K_DOWN:
        direction = 3
  pygame.display.flip()
pygame.quit()