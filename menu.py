import pygame as pg
from functions import spriteList, updateAnimationFrame

class Menu(pg.sprite.Sprite):

    def __init__(self,type, state, time):
        super().__init__()
        self.font = pg.font.Font("miscellaneous/AlegreyaSansSC-Bold.ttf", 50)
        self.x = 0
        self.y = 0
        self.index = 0
        self.type = type
        self.spr = spriteList("title","cuphead_title_screen", 34, 1)
        self.image = self.spr[self.index]
        if self.type == "principal":
            self.background = pg.image.load("title/title_screen_background.png")
            self.pressQ = self.font.render("Q PARA INICIAR", True, "black")
        elif self.type == "tutorial":
            self.background = pg.image.load("miscellaneous/backgroundMenu.png")
            self.board = pg.image.load("miscellaneous/board.png")
            self.board = pg.transform.scale(self.board,(1100,500))
            self.pressZ = self.font.render("APERTE Z PARA ATIRAR", True, "white")
            self.pressQ = self.font.render("APERTE Q PARA INICIAR!", True, "white")
            self.pressSpace = self.font.render("APERTE ESPAÇO PARA PULAR", True, "white")
            self.pressAD = self.font.render("APERTE A E D PARA SE MOVER", True, "white")
            self.pressV = self.font.render("APERTE V PARA USAR SEU ESPECIAL", True, "white")


        self.rect = self.image.get_rect(topleft=[self.x+100, self.y+120])
        self.currentFrame = 0
        self.animatedFrame = 5

    def updateAnimation(self):
        self.image = updateAnimationFrame(self, 2, "menu")     
        

    def draw(self, screen):
        screen.blit(self.background, (0,0))
        if self.type == "principal":
            screen.blit(self.pressQ, (450, 475))
        if self.type == "tutorial":
            screen.blit(self.board, (100,100))
            screen.blit(self.pressQ, (420, 500))
            screen.blit(self.pressSpace,(350,275))
            screen.blit(self.pressAD, (350,200))
            screen.blit(self.pressZ, (420,350))
            screen.blit(self.pressV, (300,425))

            
    def update(self):
        self.updateAnimation()
