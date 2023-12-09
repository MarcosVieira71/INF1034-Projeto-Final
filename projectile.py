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
      print("a")
      self.collideSpr = spriteList("projectiles", "collide", 5, 3)
      self.peashotSpr =  spriteList('projectiles', 'peashot', 5, 3)
    elif self.type == "ex":
      self.peashotSpr = spriteList('projectiles', 'ult', 8, 1.5 )
      self.collideSpr = spriteList('projectiles', 'ultFade', 9, 1.5)
      self.damage *=5
    self.currentFrame = 0
    self.animatedFrame = 3
    self.index = 0
    self.deltaDist = self.x - self.x0
    self.spr = self.startSpr
    self.image = self.spr[self.index]
    self.image.blit(self.image, (self.x, self.y))
    self.rect = self.image.get_rect(center=[self.x, self.y+30])

  def updateAnimation(self):
    if self.deltaDist > 25:
      self.spr = self.peashotSpr
    self.image = updateAnimationFrame(self, 1, "projectile")
 
    
  def update(self, enemy, projectile_group):
    self.x += self.speed
    self.rect.x = self.x
    self.deltaDist = abs(self.x - self.x0)
    self.updateAnimation()
    if self.deltaDist > 1000:
      self.kill()
    if pg.sprite.spritecollideany(enemy, projectile_group) != None:
        enemy.life -= self.damage
        self.kill()