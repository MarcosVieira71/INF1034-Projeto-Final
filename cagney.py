import random
import pygame as pg
from boomerang import Boomerang
from functions import spriteList, updateAnimationFrame


class Cagney(pg.sprite.Sprite):
  def __init__(self, x, y, life, projectiles_group):
    super().__init__()
    self.x, self.y = x, y 
    self.life = life
    self.projectiles = projectiles_group
    self.actions =  {
      "intro": spriteList('cagneyCarnation', "Intro", 20, 1.5),
      "idle": spriteList('cagneyCarnation', "Idle", 46, 1.5),
      "creatingObjects": spriteList('cagneyCarnation', "Create", 29, 1.5),
      "faceAttackLow": spriteList('cagneyCarnation', "FA_Low", 30,  1.5),
      "faceAttackHigh": spriteList('cagneyCarnation', "FA_High", 30, 1.5),
      "death": spriteList('cagneyCarnation', "Death", 12, 1.5)
    }
    
    self.laughs = {
        1 : pg.mixer.Sound("sfx/flower_laugh_01.wav"),
        2 : pg.mixer.Sound("sfx/flower_laugh_02.wav"),
        3 : pg.mixer.Sound("sfx/flower_laugh_03.wav"),
        4 : pg.mixer.Sound("sfx/flower_laugh_04.wav"),
        5 : pg.mixer.Sound("sfx/flower_laugh_05.wav")
        }

    self.index = 0
    self.currentAction = "intro"
    self.image = self.actions[self.currentAction][self.index]
    self.currentFrame = 0
    self.animatedFrame = len(self.actions[self.currentAction])/1.25
    self.intro = True
    self.idle = False
    self.firingObjects = False
    self.creatingObjects = False
    self.faceAttackHigh = False
    self.faceAttackLow = False
    self.death = False
    self.states = [self.idle, self.firingObjects, self.creatingObjects, self.faceAttackLow, self.faceAttackHigh, self.death]
    self.frames = 0
    self.rect = self.image.get_rect(center = [self.x, self.y-100])
    self.attackState = False
    self.attackRate = 0
    self.fireRate = 0
    self.hold = False
    self.holdCD = 0
    self.laughSound = False
    self.deathSound = False
    self.randomizerLaugh = 1
    self.laughSfx = self.laughs[self.randomizerLaugh]
    self.laughSfx.set_volume(0.3)
    self.mask = pg.mask.from_surface(self.image)
    self.boomerang = None


  def updateAnimation(self):

    if self.death:
      self.currentAction = "death"
      if not self.deathSound:
        self.laughDeathSfx = pg.mixer.Sound("sfx/flower_phase2_death_scream.wav")
        self.laughDeathSfx.set_volume(0.3)
        pg.mixer.Sound.play(self.laughDeathSfx)
        self.deathSound = True
    elif self.intro:
      self.currentAction = "intro"

    elif self.idle:
      self.currentAction = "idle"
      
    elif self.creatingObjects:
      self.currentAction = "creatingObjects"
      
    elif self.faceAttackLow:
      self.currentAction = "faceAttackLow"
    
    elif self.faceAttackHigh:
      self.currentAction = "faceAttackHigh"
    
    
    
    self.image = updateAnimationFrame(self, 7, "entity")
  
  def create_projectile(self):
     return Boomerang(self.rect.x, self.rect.y+300, 10)
    

  def draw(self, screen):
     pg.draw.rect(screen, (255,0,0), (self.rect), 2)

  def update(self, screen):
    
    if not self.attackState:
      self.laughSound = False
      self.attackRate += 1
      if self.attackRate >= 300:
        self.attackState = True
    if self.attackState and self.index == 0:
      self.attack = random.randint(1,3)
      self.randomizerLaugh = random.randint(1,5)
      self.attackState = False
      self.attackRate = 0
      self.idle =  False    
      if not self.laughSound: 
        pg.mixer.Sound.play(self.laughSfx)
        self.laughSound = True
      if self.attack == 1:
        self.faceAttackHigh = True
      elif self.attack == 2:
        self.faceAttackLow = True
      else : 
        self.creatingObjects =  True

    self.rect = self.image.get_rect(bottomright = self.rect.bottomright)


    if self.intro:
      if self.index >= 19:
        self.intro = False
        self.idle = True
        
    elif self.creatingObjects:
      if self.index == 22:
        self.boomerang = self.create_projectile()
        self.projectiles.add(self.boomerang)
      if self.index == 28:
        self.creatingObjects = False
        self.idle = True

    elif self.faceAttackHigh or self.faceAttackLow:

      self.mask = pg.mask.Mask((self.image.get_width(), self.image.get_height()/2), True)
      
      if self.index == 6:
        self.hold = True
      if self.hold == True:
        self.index = 6
        self.holdCD += 1
      if self.holdCD > 25:
        self.hold = False
        self.holdCD = 0
        self.index = 7
      if self.index == 29:
        self.faceAttackHigh, self.faceAttackLow = False, False
        self.idle = True
    if self.life <= 0:
      self.death = True

    self.updateAnimation()
    

    self.draw(screen)