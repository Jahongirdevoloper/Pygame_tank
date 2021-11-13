from pathlib import Path
import pygame
import random

# Initializing pygame
pygame.init()

# print(help(pygame.Rect))

# Global variables
WIDTH = 1200
HEIGHT = 700
BASE_DIR = Path(__file__).parent
CLOCK_RATE = 60

running = True
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tanks Battle')
clock = pygame.time.Clock()

bg_image = pygame.image.load(BASE_DIR / 'assets' / 'bg.png')

# Tank Class
class Tank:
  images = {
    'RIGHT' : pygame.image.load(BASE_DIR / 'assets' / 'tanks' / 'tank_right.png'),
    'UP' : pygame.image.load(BASE_DIR / 'assets' / 'tanks' / 'tank_up.png'),
    'LEFT' : pygame.image.load(BASE_DIR / 'assets' / 'tanks' / 'tank_left.png'),
    'DOWN' : pygame.image.load(BASE_DIR / 'assets' / 'tanks' / 'tank_down.png'),
  }

  def __init__(self, width, height, x, y, speed):
    self.width = width
    self.height = height
    self.x = x
    self.y = y
    self.speed = speed
    self.direction = "RIGHT"
    self.boolets_t = []
    self.jon =10

  def get_rect(self):
    return pygame.Rect(self.x, self.y, self.width, self.height )

  def inspect_coll(self, sprites):
    fl = False
    rc = self.get_rect()
    for el in sprites:
      if rc.colliderect(el.get_rect()):
        fl = True
    return fl, self.direction

  # def funk(self, bolluts, ob):
  #   fl = False
  #   rc = self.get_rect()
  #   for i in bolluts:
  #     if rc.colliderect(i.get_rect()):
  #       ob.boolets_e.remove(i)
  #       fl = True
  #       return fl




  def draw(self, win: pygame.Surface):
    win.blit(self.images[self.direction], (self.x, self.y))

    for boolet in self.boolets_t:
      boolet.draw(win, self)
      boolet.move(self)


  def move(self, keys, sprites):
    fl, direc = self.inspect_coll(sprites)

    if keys[pygame.K_RIGHT]:
      self.direction = 'RIGHT'
      if self.x < WIDTH - self.width:
        if not (fl and direc == 'RIGHT'):
          self.x += self.speed
    if keys[pygame.K_LEFT]:
      self.direction = 'LEFT'
      if self.x > 0:
        if not (fl and direc == 'LEFT'):
          self.x -= self.speed
    if keys[pygame.K_UP]:
      self.direction = 'UP'
      if self.y > 0:
        if not (fl and direc == 'UP'):
          self.y -= self.speed
    if keys[pygame.K_DOWN]:
      self.direction = 'DOWN'
      if self.y < HEIGHT - self.height:
        if not (fl and direc == 'DOWN'):
          self.y += self.speed
    if keys[pygame.K_SPACE]:
      if len(self.boolets_t) < 10:
        center_x = int(self.x + self.width//2 -2)
        center_y = int(self.y + self.height//2 -3)
        boolet = Boolet(center_x, center_y, self.direction, 30)
        self.boolets_t.append(boolet)
    # for j in sprites:
    #   if self.funk(j.boolets_e, j):
    #     self.jon -= 1
    #     if self.jon < 0:
    #       pass 

    

class Boolet:
  def __init__(self, x, y, direction, speed, radius = 4, color =(255, 255, 255)):
    self.x = x
    self.y = y
    self.direction = direction
    self.speed = speed
    self.radius = radius
    self.color = color
  
  def get_rect(self):
    return pygame.Rect(self.x, self.y, self.width, self.height )

  def draw(self, win: pygame.Surface):
    pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

  def move(self):
    if self.direction == 'RIGHT' and self.x < WIDTH:
      self.x += self.speed
    elif self.direction == 'LEFT' and self.x > 0:
      self.x -= self.speed
    elif self.direction == 'UP' and self.y > 0:
      self.y -= self.speed
    elif self.direction == 'DOWN' and self.y < HEIGHT:
      self.y += self.speed
    else:
      del self 
    


class Enemy(Tank):

  images = {
    'RIGHT' : pygame.image.load(BASE_DIR / 'assets' / 'enemy' / 'enemy_right.png'),
    'UP' : pygame.image.load(BASE_DIR / 'assets' / 'enemy' / 'enemy_up.png'),
    'LEFT' : pygame.image.load(BASE_DIR / 'assets' / 'enemy' / 'enemy_left.png'),
    'DOWN' : pygame.image.load(BASE_DIR / 'assets' / 'enemy' / 'enemy_down.png'),
  }
  
  def __init__(self, width, height, speed):
    super().__init__(width, height, random.randint(WIDTH//2, WIDTH - 80), random.randint(0, HEIGHT - 80), speed)
    self.inter = 30
    self.direction =random.choice(['UP', 'DOWN', 'LEFT'])
    self.boolets_e = []

  def draw(self, win: pygame.Surface):
    win.blit(self.images[self.direction], (self.x, self.y))

    if random.randint(0, 100) % 43== 0:
      if len(self.boolets_e) < 10:
        center_x = int(self.x + self.width//2 -2)
        center_y = int(self.y + self.height//2 -3)
        boolet = Boolet(center_x, center_y, self.direction, 30)
        self.boolets_e.append(boolet)

    for boolet in self.boolets_e:
      boolet.draw(win,self)
      boolet.move(self)

  def move(self, sprites):
    fl, direc = self.inspect_coll(sprites)

    if self.inter > 0:
      self.inter -= 1
    else:
      choice = random.choice([True, False])
      if choice:
        direc = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.direction = direc
      self.inter = 30

    if self.direction == 'LEFT' and self.x > 0:
      if not (fl and 'LEFT' == direc):
        self.x -= self.speed
    elif self.direction == 'RIGHT' and self.x < WIDTH - self.width:
      if not (fl and 'RIGHT' == direc):  
        self.x += self.speed
    elif self.direction == 'UP' and self.y > 0:
      if not (fl and 'UP' == direc):
        self.y -= self.speed
    elif self.direction == 'DOWN' and self.y < HEIGHT - self.height:
      if not (fl and 'DOWN' == direc):
        self.y += self.speed


enemy = Enemy(80, 80, 15)
enemy2 = Enemy(80, 80, 15)

# Our tank object
tank = Tank(80, 80, 40, 40, 16)

# Main drawer function
def drawer():
  global win
  win.blit(bg_image, (0, 0))
  tank.draw(win)
  enemy.draw(win)
  enemy2.draw(win)
  pygame.display.flip()

# Main loop
while running:
  clock.tick(CLOCK_RATE)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      pygame.quit()

  keys = pygame.key.get_pressed()
  tank.move( keys, [enemy, enemy2])
  enemy.move([tank, enemy2])
  enemy2.move([tank, enemy])
  drawer()
