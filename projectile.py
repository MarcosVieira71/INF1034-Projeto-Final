import pygame as pg
from functions import spriteList
class Projectile(pg.sprite.Sprite):

  def __init__(self, x, y, damage, speed, width, height):
    super().__init__()
    self.x = x
    self.x0 = x
    self.y = y
    self.speed = speed
    self.startSpr = spriteList('projectiles', "start", 3, 3)
    self.collideSpr = spriteList("projectiles", "collide", 5, 3)
    self.peashotSpr =  spriteList('projectiles', 'peashot', 5, 3)
    self.currentFrame = 0
    self.animatedFrame = 3
    self.index = 0
    self.deltaDist = self.x - self.x0
    self.spr = self.startSpr
    self.image = self.spr[self.index]
    self.image.blit(self.image, (self.x, self.y))
    self.damage = damage
    self.rect = self.image.get_rect(center=[self.x, self.y+30])

  def updateAnimationFrame(self):
    if self.deltaDist > 20:
      self.spr = self.peashotSpr
    self.currentFrame += 1
    if self.currentFrame >= self.animatedFrame:
      self.currentFrame = 0
      self.index = (self.index+1) % len(self.spr)
      self.image = self.spr[self.index]
      if self.speed < 0:
        self.image = pg.transform.flip(self.image, True, False)

    
  def update(self, enemy, projectile_group):
    self.x += self.speed
    self.rect.x = self.x
    self.deltaDist = abs(self.x - self.x0)
    self.updateAnimationFrame()
    if self.deltaDist > 1000 or pg.sprite.spritecollideany(enemy, projectile_group) != None:
      enemy.life -= self.damage
      self.kill()


      
      