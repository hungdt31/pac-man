import pygame
import math
from ghost_info import blinky_img, pinky_img, inky_img,clyde_img, spooked_img, dead_img
from board import boards
pygame.init()

WIDTH = 900
HEIGHT = 774
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf',20)
level = boards
color = 'blue'
player_speed = 3
PI = math.pi
flicker = False

score = 0
power_up = False
power_counter = 0
eaten_ghost = [False] * 4
start_counter = 0
moving = False
lives = 3
counter = 0

# chia screen thành các ô vuông nhỏ có width = height_cell và height = width_cell
height_cell = ((HEIGHT - 70) // 32)
width_cell = (WIDTH // 30)
half_width_cell = width_cell // 2
half_height_cell = height_cell // 2


class Map:
  def draw_board(self):
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
          pygame.draw.line(screen, color, (j * width_cell + (0.5 * width_cell), i * height_cell),(j * width_cell + (0.5 * width_cell), i * height_cell + height_cell), 3)
        if level[i][j] == 4:
          pygame.draw.line(screen, color, (j * width_cell, i * height_cell + (0.5 * height_cell)),(j * width_cell + width_cell, i * height_cell + (0.5 * height_cell)), 3)
        if level[i][j] == 5:
          # tham số thứ 3 là hình chữ nhật chứa arc có gồm tọa độ góc trái trên và góc phải dưới
          pygame.draw.arc(screen, color, [(j * width_cell - (width_cell * 0.5)), (i * height_cell + (0.5 * height_cell)), width_cell, height_cell], 0, PI / 2, 3)
        if level[i][j] == 6:
          pygame.draw.arc(screen, color, [(j * width_cell + (width_cell * 0.5)), (i * height_cell + (0.5 * height_cell)), width_cell, height_cell], PI / 2, PI, 3)
        if level[i][j] == 7:
          pygame.draw.arc(screen, color, [(j * width_cell + (width_cell * 0.5)), (i * height_cell - (0.35 * height_cell)), width_cell, height_cell], PI, 3 * PI / 2, 3)
        if level[i][j] == 8:
          pygame.draw.arc(screen, color, [(j * width_cell - (width_cell * 0.42)), (i * height_cell - (0.42 * height_cell)), width_cell, height_cell], 3* PI / 2, 2 * PI, 3)
        if level[i][j] == 9:
          # draw gate
          pygame.draw.line(screen, 'white', (j * width_cell, i * height_cell + (0.5 * height_cell)), (j * width_cell + width_cell, i * height_cell + (0.5 * height_cell)), 3)

  def draw_misc(self):
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text,(15, 730))
    if power_up:
      pygame.draw.circle(screen, 'blue', (140, 740), 15)
    for i in range(lives):
      screen.blit(pygame.transform.scale(pygame.image.load('assets/player/heart.png'), (30, 30)), (650 + i * 40, 725))


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

def check_collision(center_X, center_Y):
  global score, power_up, power_counter, eaten_ghost
  x_index = center_X // width_cell
  y_index = center_Y // height_cell
  if level[y_index][x_index] == 1:
    level[y_index][x_index] = 0
    score += 10
  elif level[y_index][x_index] == 2:
    level[y_index][x_index] = 0
    score += 50
    power_up = True
    power_counter = 0
    eaten_ghost = [False] * 4


class Ghost:
  def __init__(self, x_coord, y_coord, target, speed, img, box, id):
    self.x_pos = x_coord
    self.y_pos = y_coord
    self.center_x = self.x_pos 
    self.center_y = self.y_pos 
    self.target = target
    self.speed = speed
    self.img = img
    self.in_box = box
    self.id = id
    self.turns, self.in_box = self.check_collision()
    self.rect = self.draw()
  def draw(self):
    if True:
      screen.blit(self.img, (self.x_pos, self.y_pos))
    else:
      screen.blit(self.img, (self.x_pos, self.y_pos))
    # return ghost_rect

class Player:
    _instance = None

    def __init__(self):
        # Private constructor
        self.direction= 0
        self.direction_command = 0
        self.player_X = 480 - 4
        self.player_Y = 462 - 8
        self.player_images = []
        for i in range(1,5):
          self.player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player/{i}.bmp'),(40, 40)))
        # R - L - U - D
        self.turns_allowed = [False] * 4
        pass
    
    @classmethod
    def get_player(self):
        if self._instance is None:
            self._instance = Player()
        return self._instance
    
    def draw_player(self):
      # 0 - RIGHT, 1 - LEFT, 2 - UP, 3 - DOWN
      if player.direction== 0:
        screen.blit(self.player_images[counter // 5], (self.player_X, self.player_Y))
      elif player.direction== 1:
        screen.blit(pygame.transform.flip(self.player_images[counter // 5], True, False), (self.player_X, self.player_Y))
      elif player.direction== 2:
        screen.blit(pygame.transform.rotate(self.player_images[counter // 5], 90), (self.player_X, self.player_Y))
      elif player.direction== 3:
        screen.blit(pygame.transform.rotate(self.player_images[counter // 5], 270), (self.player_X, self.player_Y))

    def move_player(self):
        # r, l, u, d
      if self.direction== 0 and self.turns_allowed[0]:
        self.player_X += player_speed
      elif self.direction== 1 and self.turns_allowed[1]:
        self.player_X -= player_speed
      elif self.direction== 2 and self.turns_allowed[2]:
        self.player_Y -= player_speed
      elif self.direction== 3 and self.turns_allowed[3]:
        self.player_Y += player_speed

    def process(self):
      self.draw_player()
      center_X = self.player_X + half_width_cell + 4
      center_Y = self.player_Y + half_height_cell + 8
      # pygame.draw.circle(screen,'white',(self.player_X, self.player_Y), 4)
      # pygame.draw.circle(screen,'white',(self.center_X, self.center_Y), 4)
      self.turns_allowed = check_position(center_X, center_Y)
      if moving:
        self.move_player()
      check_collision(center_X, center_Y)

run_game = True
while run_game:
  timer.tick(fps)
  
  if counter < 19:
    counter += 1
    if counter > 3:
      flicker = False
  else:
    counter = 0
    flicker = True
  
  # active power up
  if power_up and power_counter < 600:
    power_counter += 1
  elif power_up and power_counter >= 600:
    power_counter = 0
    power_up = False
    eaten_ghost = [False] * 4
  
  if start_counter < 120:
    moving = False
    start_counter += 1
  else:
    moving = True
  screen.fill('black')

  mp = Map()
  player = Player.get_player()
  mp.draw_board()
  player.process()
  mp.draw_misc()
  
  # setting up pygame
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run_game = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RIGHT:
        player.direction_command = 0
      if event.key == pygame.K_LEFT:
        player.direction_command = 1
      if event.key == pygame.K_UP:
        player.direction_command = 2
      if event.key == pygame.K_DOWN:
        player.direction_command = 3
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_RIGHT and player.direction_command == 0:
        player.direction_command = player.direction
      if event.key == pygame.K_LEFT and player.direction_command == 1:
        player.direction_command = player.direction
      if event.key == pygame.K_UP and player.direction_command == 2:
        player.direction_command = player.direction
      if event.key == pygame.K_DOWN and player.direction_command == 3:
        player.direction_command = player.direction

    for i in range(4):
      if player.direction_command == i and player.turns_allowed[i]:
        player.direction= i

  pygame.display.flip()
pygame.quit()