import pygame as pg
from projectile import Projectile
from functions import spriteList, updateAnimationFrame


class Player(pg.sprite.Sprite):

  def __init__(self, x, y, life, projectiles_group):
    super().__init__()
    self.x, self.y = x, y
    self.speed_x = 3
    self.speed_y = 28
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
        "intro": spriteList('cupheadsprites', "intro", 28, 1),
        "ex" : spriteList('cupheadsprites', 'ex', 13, 1)
    }
    self.index = 0
    self.currentAction = "idle"
    self.image = self.actions[self.currentAction][self.index]
    self.currentFrame = 0
    self.animatedFrame = len(self.actions[self.currentAction])*4
    self.intro = True
    self.hit = False
    self.flip = False
    self.moves = [False, False]
    self.ex = False
    self.jump = False
    self.shoot = False
    self.idle = True
    self.runshoot = False
    self.death = False
    self.states = [
        self.flip, self.moves[0], self.moves[1], self.jump, self.shoot,
        self.idle, self.runshoot, self.hit
    ]
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
    self.generateEx = pg.mixer.Sound("sfx/player_weapon_peashot_ex_0001.wav")
    self.generateEx.set_volume(0.3)
    self.generateExSound = False
    self.charge = 0
    self.gravity = 1
    self.on_ground = False
    self.mask = pg.mask.from_surface(self.image)

  def platformCollide(self, platform1, platform2):
    return self.mask.overlap(platform1.mask, self.offset(platform1)) or self.mask.overlap(platform2.mask, self.offset(platform2))

  def apply_gravity(self):
      self.rect.y += self.gravity
      self.y = self.rect.y

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

    elif self.ex:
      self.currentAction = "ex"

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
  
  def offset(self, mask2):
    return int(mask2.rect.x - self.rect.x), int(mask2.rect.y - self.rect.y)
  
  def immune(self):
    return self.lastCollision > pg.time.get_ticks()  - 3000

  def create_projectile(self, type):
    self.speed = 15
    self.distXplayer = 70
    self.distYplayer = 32
    if self.flip:
      self.speed *= -1
      self.distXplayer *= -1 / 2
    if self.currentAction == "runshoot":
      self.distYplayer += 18
    return Projectile(self.rect.x + self.distXplayer,
                      self.rect.y + self.distYplayer, 2, self.speed, type)


  def draw(self, screen):
    pg.draw.rect(screen, (255, 0, 0), (self.rect), 2)

  def update(self, screen, enemy, platform1, platform2, ground):

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
        if not keys[pg.K_v] or self.index == 12:
          self.ex = False

        if self.on_ground:
          if self.jump:
            self.rect.y -= self.speed_y
            self.y = self.rect.y
            self.speed_y -= 1

            if self.speed_y < 0:
              self.jump = False
              self.on_ground = False
              self.speed_y = 28
              
        if (not self.jump and self.on_ground) or not self.on_ground:
          self.gravity = self.speed_y
          self.falling = True
          self.apply_gravity()

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
          if self.fireRate >= 7.5:
            self.createBulletSound = False
            shoot = self.create_projectile("bullet")
            self.projectiles.add(shoot)
            self.fireRate = 0
            if not self.bulletLoop:
              pg.mixer.Sound.play(self.fireLoopSfx)
              self.bulletLoop = True
          self.shoot = True
          if self.charge <= 500:
            self.charge+=1

        if keys[pg.K_v] and self.charge >= 100:
          self.generateExSound = False
          self.charge -= 100
          self.ex = True
          if not self.generateExSound:
            pg.mixer.Sound.play(self.generateEx)
            self.generateExSound = True
          shoot = self.create_projectile("ex")
          self.projectiles.add(shoot)          
          
    else:
      self.speed_y = 28
      self.rect.y -= self.speed_y/8
      self.y = self.rect.y

    self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)

    if self.mask.overlap(enemy.mask, self.offset(enemy)) or (enemy.boomerang != None and self.mask.overlap(enemy.boomerang.mask, self.offset(enemy.boomerang))):
      if not self.immune() and self.life > 0:
        self.hit = True
        self.life -= 1
        self.lastCollision = pg.time.get_ticks()
      
    else:
      self.hit = False
    
    if self.platformCollide(platform1, platform2):
      self.on_ground = True
      self.rect.y = platform1.y - self.image.get_height()
      self.y = self.rect.y
    
    if self.y >= 600 - self.image.get_height():
      self.on_ground = True
      self.rect.y = ground.y - self.image.get_height()
      self.y = self.rect.y
    
    if self.x < 0:
      self.rect.x = 0
      self.x = self.rect.x
    
    if self.x + self.image.get_width() > 1280:
      self.rect.x = 1280 - self.image.get_width()
      self.x = self.rect.x
  

    for state in self.states:
      self.updateAnimation()
