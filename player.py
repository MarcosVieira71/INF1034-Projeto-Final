import pygame as pg
from projectile import Projectile
from functions import spriteList, updateAnimationFrame


class Player(pg.sprite.Sprite):

  def __init__(self, x, y, life, projectiles_group):
    super().__init__()
    self.x, self.y = x, y
    self.speed_x = 3
    self.speed_y = 20
    self.life = life
    self.projectiles = projectiles_group
    self.actions = {
        "idle": spriteList('cupheadsprites', "idle", 9, 1),
        "jump": spriteList('cupheadsprites', "jump", 8, 1),
        "shoot": spriteList('cupheadsprites', "shoot", 3, 1),
        "run": spriteList('cupheadsprites', "run", 16, 1),
        "runshoot": spriteList('cupheadsprites', "shooting", 16, 1),
        "death": spriteList('cupheadsprites', "death", 16, 1),
        "hit": spriteList('cupheadsprites', "hit", 6, 1)
    }
    self.index = 0
    self.currentAction = "idle"
    self.image = self.actions[self.currentAction][self.index]
    self.currentFrame = 0
    self.animatedFrame = len(self.actions[self.currentAction])*2
    self.hit = False
    self.flip = False
    self.moves = [False, False]
    self.jump = False
    self.shoot = False
    self.idle = True
    self.runshoot = False
    self.states = [
        self.flip, self.moves[0], self.moves[1], self.jump, self.shoot,
        self.idle, self.runshoot, self.hit
    ]
    self.frames = 0
    self.playerTime = 0
    # self.rect = self.image.get_rect(midleft = [self.x, self.y])
    self.rect = self.image.get_rect(bottomleft=[self.x, self.y])
    self.fireRate = 0
    self.lastCollision = 0

  def updateAnimation(self):
    
    if self.hit:
       self.currentAction = "hit"

    elif self.jump:
      self.currentAction = "jump"

    elif (self.moves[0] or self.moves[1]) and self.shoot:
      self.currentAction = "runshoot"

    elif self.moves[0]:
      self.currentAction = "run"

    elif self.moves[1]:
      self.currentAction = "run"

    elif self.shoot:
      self.currentAction = "shoot"

    elif self.idle:
      self.currentAction = "idle"
    self.image = updateAnimationFrame(self, 1, "entity")
    if self.flip:
        self.image = pg.transform.flip(self.image, True, False)
  
  def immune(self):
    return self.lastCollision > pg.time.get_ticks()  - 3000

  def create_projectile(self):
    self.speed = 25
    self.distXplayer = 70
    self.distYplayer = 32
    if self.flip:
      self.speed *= -1
      self.distXplayer *= -1 / 2
    if self.currentAction == "runshoot":
      self.distYplayer += 18
    return Projectile(self.rect.x + self.distXplayer,
                      self.rect.y + self.distYplayer, 5, self.speed)

  def draw(self, screen):
    pg.draw.rect(screen, (255, 0, 0), (self.rect), 2)

  def update(self, screen, enemy_group, boomerang_group):
    keys = pg.key.get_pressed()

    if not keys[pg.K_z]:
      self.shoot = False

    if self.jump:
      self.rect.y -= self.speed_y
      self.speed_y -= 1

      if self.speed_y < -20:
        self.jump = False
        self.speed_y = 20

    if keys[pg.K_d]:
      self.flip = False
      self.idle = False
      self.moves[0] = True
      self.x += self.speed_x
      self.rect.x = self.x

    elif keys[pg.K_a]:
      self.moves[1] = True
      self.flip = True
      self.idle = False
      self.x -= self.speed_x
      self.rect.x = self.x

    else:
      self.shoot = False
      self.idle = True
      self.moves = [False for i in range(2)]

    if keys[pg.K_z]:
      self.fireRate += 1
      if self.fireRate == 5:
        if self.flip:
          shoot = self.create_projectile()
        shoot = self.create_projectile()
        self.projectiles.add(shoot)
        self.fireRate = 0

      self.shoot = True

    self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)

    if pg.sprite.spritecollideany(
        self, enemy_group) != None or pg.sprite.spritecollideany(
            self, boomerang_group) != None:
            self.hit = True
            if not self.immune():
              self.life -= 1
              self.lastCollision = pg.time.get_ticks()
    else:
      self.hit = False
    for state in self.states:
      self.updateAnimation()

    self.draw(screen)