import pygame as pg
from functions import spriteList, updateAnimationFrame
class Projectile(pg.sprite.Sprite):

  def __init__(self, x, y, damage, speed, type):
    super().__init__()
    self.x = x
    self.x0 = x
    self.y = y
    self.speed = speed
    self.type = type
    self.damage = damage
    self.startSpr = spriteList('projectiles', "start", 3, 3)
    if self.type == "bullet":
      self.collideSpr = spriteList("projectiles", "collide", 3, 3)
      self.peashotSpr =  spriteList('projectiles', 'peashot', 5, 3)
    elif self.type == "ex":
      self.peashotSpr = spriteList('projectiles', 'ult', 8, 1.5 )
      self.collideSpr = spriteList('projectiles', 'ultFade', 9, 1.5)
      self.damage *=5
    self.currentFrame = 0
    self.collide = False
    self.animatedFrame = 3
    self.index = 0
    self.deltaDist = self.x - self.x0
    self.spr = self.startSpr
    self.image = self.spr[self.index]
    self.image.blit(self.image, (self.x, self.y))
    self.rect = self.image.get_rect(center=[self.x, self.y+30])
    self.mask = pg.mask.from_surface(self.image)

  def offset(self, mask2):
    return int(mask2.rect.x - self.rect.x), int(mask2.rect.y - self.rect.y)

  def updateAnimation(self):
    if self.collide:
      self.spr = self.collideSpr
    elif self.deltaDist > 25:
      self.spr = self.peashotSpr
    self.image = updateAnimationFrame(self, 1, "projectile")
 
    
  def update(self, enemy):
    self.x += self.speed
    self.rect.x = self.x
    self.deltaDist = abs(self.x - self.x0)
    self.updateAnimation()
    if self.deltaDist > 1000:
      self.kill()

    if self.collide:
      if self.index == 2:
        self.kill()  

    if self.mask.overlap(enemy.mask, self.offset(enemy)):
      enemy.life -= self.damage
      self.damage = 0
      self.collide = True
      self.rect.y -= 10
      self.y = self.rect.y