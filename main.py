import pygame
import math
from player_info import direction, counter, player_X , player_Y , player_images, turns_allowed
from board import boards
pygame.init()

WIDTH = 900
HEIGHT = 754
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf',20)
level = boards
color = 'blue'
player_speed = 2
PI = math.pi
flicker = False
direction_command = 0

# chia screen thành các ô vuông nhỏ có width = height_cell và height = width_cell
height_cell = ((HEIGHT - 50) // 32)
width_cell = (WIDTH // 30)
half_width_cell = width_cell // 2
half_height_cell = height_cell // 2

for i in range(1,5):
  player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player/{i}.bmp'),(35, 35)))
def draw_board():
  for i in range(len(level)):
    for j in range(len(level[i])):
      # pygame.draw.rect(screen, 'red', (j * width_cell, i * height_cell, width_cell, height_cell), 1)
      if level[i][j] == 1:
        # tham số thứ 3 được xem như tọa độ của tâm hình tròn
        pygame.draw.circle(screen, 'white', (j * width_cell + (0.5*width_cell), i * height_cell + (0.5 * height_cell)), 4)
      if level[i][j] == 2 and not flicker:
        pygame.draw.circle(screen, 'white', (j * width_cell + (0.5*width_cell), i * height_cell + (0.5 * height_cell)), 10)
      if level[i][j] == 3:
        # vẽ đường thẳng : tham số thứ 3 và 4 lần lượt là tọa độ của điểm bắt đầu và kết thúc
        # tham số cuối cùng là độ dày của đường thẳng
        pygame.draw.line(screen, color, (j * width_cell + (0.5 * width_cell), i * height_cell),
                                        (j * width_cell + (0.5 * width_cell), i * height_cell + height_cell), 3)
      if level[i][j] == 4:
        pygame.draw.line(screen, color, (j * width_cell, i * height_cell + (0.5 * height_cell)),
                                        (j * width_cell + width_cell, i * height_cell + (0.5 * height_cell)), 3)
      if level[i][j] == 5:
        # tham số thứ 3 là hình chữ nhật chứa arc có gồm tọa độ góc trái trên và góc phải dưới
        pygame.draw.arc(screen, color, [(j * width_cell - (width_cell * 0.5)), (i * height_cell + (0.5 * height_cell)), width_cell, height_cell], 0, PI / 2, 3)
      if level[i][j] == 6:
        pygame.draw.arc(screen, color, [(j * width_cell + (width_cell * 0.5)), (i * height_cell + (0.5 * height_cell)), width_cell, height_cell], PI / 2, PI, 3)
      if level[i][j] == 7:
        pygame.draw.arc(screen, color, [(j * width_cell + (width_cell * 0.5)), (i * height_cell - (0.35 * height_cell)), width_cell, height_cell], PI, 3 * PI / 2, 3)
      if level[i][j] == 8:
        pygame.draw.arc(screen, color, [(j * width_cell - (width_cell * 0.42)), (i * height_cell - (0.42 * height_cell)), width_cell, height_cell], 3* PI / 2, 2 * PI, 3)
      # draw gate
      if level[i][j] == 9:
        pygame.draw.line(screen, 'white', (j * width_cell, i * height_cell + (0.5 * height_cell)),
                                          (j * width_cell + width_cell, i * height_cell + (0.5 * height_cell)), 3)

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
  x_index = (center_X // width_cell)
  y_index = (center_Y // height_cell)
  reminder_x = center_X % width_cell
  reminder_y = center_Y % height_cell
  directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]  # Right, Left, Up, Down

  for i, (dx, dy) in enumerate(directions):
      new_x = x_index + dx
      new_y = y_index + dy 
      if 0 <= new_y < len(level) and 0 <= new_x < len(level[0]):
        if level[new_y][new_x] < 3:
          turns[i] = True
        elif i == 0 and reminder_x <= half_width_cell:
          turns[i] = True
        elif i == 1 and reminder_x >= half_width_cell:
          turns[i] = True
        elif i == 2 and reminder_y >= half_height_cell:
          turns[i] = True
        elif i == 3 and reminder_y <= half_height_cell:
          turns[i] = True
  return turns

def move_player(player_X, player_Y):
  # r, l, u, d
  if direction == 0 and turns_allowed[0]:
    player_X += player_speed
  elif direction == 1 and turns_allowed[1]:
    player_X -= player_speed
  elif direction == 2 and turns_allowed[2]:
    player_Y -= player_speed
  elif direction == 3 and turns_allowed[3]:
    player_Y += player_speed
  return player_X, player_Y
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
  center_X = player_X + half_width_cell + 4
  center_Y = player_Y + half_height_cell + 8
  # pygame.draw.circle(screen,'white',(player_X, player_Y), 4)
  # pygame.draw.circle(screen,'white',(center_X, center_Y), 4)
  turns_allowed = check_position(center_X, center_Y)
  player_X, player_Y = move_player(player_X, player_Y)
  # setting up pygame
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RIGHT:
        direction_command = 0
      if event.key == pygame.K_LEFT:
        direction_command = 1
      if event.key == pygame.K_UP:
        direction_command = 2
      if event.key == pygame.K_DOWN:
        direction_command = 3
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_RIGHT and direction_command == 0:
        direction_command = direction
      if event.key == pygame.K_LEFT and direction_command == 1:
        direction_command = direction
      if event.key == pygame.K_UP and direction_command == 2:
        direction_command = direction
      if event.key == pygame.K_DOWN and direction_command == 3:
        direction_command = direction

    for i in range(4):
      if direction_command == i and turns_allowed[i]:
        direction = i

  pygame.display.flip()
pygame.quit()