import pygame as pg
from functions import spriteList

class Boomerang(pg.sprite.Sprite):
  def __init__(self, x, y, speed, width, height):
    super().__init__()
    self.x = x
    self.x0 = x
    self.y = y
    self.speed = -speed
    self.spr = spriteList('cagneyCarnation', 'Boomerang', 9, 1)
    self.currentFrame = 0
    self.animatedFrame = 3
    self.index = 0
    self.deltaDist = self.x - self.x0
    self.image = self.spr[self.index]
    self.image.blit(self.image, (self.x, self.y))
    self.damage = 1
    self.rect = self.image.get_rect(center=[self.x, self.y])

  def updateAnimationFrame(self):

    self.currentFrame += 1
    if self.currentFrame >= self.animatedFrame:
      self.currentFrame = 0
      self.index = (self.index + 1) % len(self.spr)
      self.image = self.spr[self.index]
      if self.speed > 0:
        self.image = pg.transform.flip(self.image, True, False)

  def update(self):
    if self.x < -200:
      self.y += 100
      self.rect.y = self.y
      self.speed *= -1
    self.x += self.speed
    self.rect.x = self.x
    self.deltaDist = abs(self.x - self.x0)
    if self.x > 1280:
      self.kill()
    self.updateAnimationFrame()
