import pygame as pg
from functions import spriteList, updateAnimationFrame

class Message(pg.sprite.Sprite):
    
    def __init__(self, x, y, folder, type, size, c):
        super().__init__()
        self.x = x
        self.y = y
        self.spr = spriteList(folder,type, size, c)
        self.index = 0
        self.image = self.spr[self.index]
        self.rect = self.image.get_rect(topleft=[self.x, self.y])
        self.currentFrame = 0
        self.animatedFrame = 5
    def updateAnimation(self):
        self.image = updateAnimationFrame(self, 1, "message")


    def update(self):
        
        self.updateAnimation()
        

    