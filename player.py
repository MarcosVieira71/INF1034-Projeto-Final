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
        "death": spriteList('cupheadsprites', "death", 24, 1),
        "hit": spriteList('cupheadsprites', "hit", 6, 1),
        "intro": spriteList('cupheadsprites', "intro", 28, 1)
    }
    self.index = 0
    self.currentAction = "idle"
    self.image = self.actions[self.currentAction][self.index]
    self.currentFrame = 0
    self.animatedFrame = len(self.actions[self.currentAction])*2
    self.intro = True
    self.hit = False
    self.flip = False
    self.moves = [False, False]
    self.jump = False
    self.shoot = False
    self.idle = True
    self.runshoot = False
    self.death = False
    self.states = [
        self.flip, self.moves[0], self.moves[1], self.jump, self.shoot,
        self.idle, self.runshoot, self.hit
    ]
    self.frames = 0
    self.playerTime = 0
    self.rect = self.image.get_rect(bottomleft=[self.x, self.y])
    self.fireRate = 0
    self.lastCollision = 0
    self.introSound = False
    self.introSfx = pg.mixer.Sound("sfx/player_intro_cuphead.wav")
    self.introSfx.set_volume(0.2)
    self.fireLoopSfx = pg.mixer.Sound("sfx/loopBullet.mp3")
    self.fireLoopSfx.set_volume(0.3)
    self.hitSound = False
    self.hitSfx = pg.mixer.Sound("sfx/player_damage_crack_level4.wav")
    self.hitSfx.set_volume(0.3)
  def updateAnimation(self):
    
    if self.death:
      self.currentAction = "death"

    elif self.intro:
      self.currentAction = "intro"
      if not self.introSound:
        pg.mixer.Channel(1).play(self.introSfx)
        self.introSound = True

    elif self.hit:
       self.currentAction = "hit"
       self.hitSound = False
       if not self.hitSound and self.life > 0:
         self.hitSfx.play()
         self.hitSound = True
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

    if self.life == 0:
      self.death = True

    if not self.death:

      if self.intro:
        if self.index >= 27:
          self.intro = False
          self.idle = True

      else:

        if not keys[pg.K_z]:
          self.shoot = False

        if self.jump:
          self.rect.y -= self.speed_y
          self.y = self.rect.y
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
          self.bulletLoop = False
          self.fireRate += 1
          if self.fireRate == 5:
            self.createBulletSound = False
            if self.flip:
              shoot = self.create_projectile()
            shoot = self.create_projectile()
            self.projectiles.add(shoot)
            self.fireRate = 0
            if not self.bulletLoop:
              pg.mixer.Sound.play(self.fireLoopSfx)
              self.bulletLoop = True
          self.shoot = True

    else:
      self.speed_y = 20
      self.rect.y -= self.speed_y/8
      self.y = self.rect.y

    self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)

    if pg.sprite.spritecollideany(
        self, enemy_group) != None or pg.sprite.spritecollideany(
            self, boomerang_group) != None:
            if not self.immune() and self.life > 0:
              self.hit = True
              self.life -= 1
              self.lastCollision = pg.time.get_ticks()
    else:
      self.hit = False
    for state in self.states:
      self.updateAnimation()

    self.draw(screen)