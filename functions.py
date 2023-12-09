import pygame as pg

def spriteList(folder, filename, size, c):
  listSpr = []

  #getHeight getWidth e escalonar de acordo com o tamanho de cada imagem da lista.
  for i in range(size):
    zeroExtra = ''
    if i+1 < 10:
      zeroExtra = '0'
    listSpr.append(pg.image.load(f"{folder}/{filename}/{filename}_00{zeroExtra}{str(i+1)}.png"))
      
  listSpr = [pg.transform.scale(sprite, (sprite.get_width()/c, sprite.get_height()/c)) for sprite in listSpr]
    
  return listSpr

def updateAnimationFrame(self, speed, type):
    self.currentFrame += speed

    if self.currentFrame >= self.animatedFrame:
      self.currentFrame = 0

      if type == "entity":
        self.index = (self.index + 1) % len(self.actions[self.currentAction])
        self.image = self.actions[self.currentAction][self.index]

      elif type == "projectile":
        self.index = (self.index + 1) % len(self.spr)
        self.image = self.spr[self.index]
        if self.speed < 0:
          self.image = pg.transform.flip(self.image, True, False)
      else: 
        self.index = (self.index + 1) % len(self.spr)
        self.image = self.spr[self.index]

    return self.image