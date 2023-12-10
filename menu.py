import pygame as pg
from functions import spriteList, updateAnimationFrame

class Menu(pg.sprite.Sprite):

    def __init__(self,type, stars, time):
        super().__init__()
        self.font = pg.font.Font("miscellaneous/AlegreyaSansSC-Bold.ttf", 50)
        self.x = 0
        self.y = 0
        self.index = 0
        self.stars = stars
        self.type = type
        self.time = time
        if self.type == "principal":
            self.background = pg.image.load("title/title_screen_background.png")
            self.pressQ = self.font.render("Q PARA INICIAR", True, "black")
            self.spr = spriteList("title","cuphead_title_screen", 34, 1)
            self.image = self.spr[self.index]
            self.rect = self.image.get_rect(topleft=[self.x+100, self.y+120])

        elif self.type == "tutorial":
            
            self.background = pg.image.load("miscellaneous/backgroundMenu.png")
            self.background = pg.transform.scale(self.background, (1280, 720))
            self.board = pg.image.load("miscellaneous/board.png")
            self.board = pg.transform.scale(self.board,(1100,600))
            self.pressZ = self.font.render("APERTE Z PARA ATIRAR", True, "white")
            self.pressQ = self.font.render("APERTE Q PARA INICIAR!", True, "white")
            self.pressSpace = self.font.render("APERTE ESPAÇO PARA PULAR", True, "white")
            self.pressAD = self.font.render("APERTE A E D PARA SE MOVER", True, "white")
            self.pressV = self.font.render("APERTE V PARA USAR SEU ESPECIAL", True, "white")
        
        if self.type == "win":
            self.font = pg.font.Font("miscellaneous/AlegreyaSansSC-Bold.ttf", 35)
            self.time = self.font.render(f"VOCÊ LEVOU {self.time[0]}:{self.time[1]} PARA VENCER!", True, "yellow")
            self.parabens = self.font.render("PARABÉNS!", True, "yellow")
            self.lifes = self.font.render(f"{self.stars}/3 VIDAS", True, "yellow")
            self.background = pg.image.load("win/winscreen_bg.png")
            self.background = pg.transform.scale(self.background, (1280,720))
            self.board = pg.image.load("win/winscreen_board.png")
            self.resultTitle = pg.image.load("win/resultados.png")
            self.star = pg.image.load("win/winscreen_main_star_a.png")
            self.star = pg.transform.scale(self.star, (50, 50))
            self.spr = spriteList("win","winscreen_ch", 7, 1)
            self.image = self.spr[self.index]
            self.rect = self.image.get_rect(topleft=[self.x+100, self.y+120])
            

        self.currentFrame = 0
        self.animatedFrame = 5

    def updateAnimation(self):
        self.image = updateAnimationFrame(self, 2, "menu")     
        

    def draw(self, screen):
        screen.blit(self.background, (0,0))
        if self.type == "principal":
            screen.blit(self.pressQ, (450, 450))
        if self.type == "tutorial":
            screen.blit(self.board, (100,50))
            screen.blit(self.pressQ, (400, 470))
            screen.blit(self.pressSpace,(330,245))
            screen.blit(self.pressAD, (330,170))
            screen.blit(self.pressZ, (400,320))
            screen.blit(self.pressV, (280,395))
        if self.type == "win":
            screen.blit(self.background, (0,0))
            screen.blit(self.board, (600,200))
            screen.blit(self.resultTitle, (200, 30))
            screen.blit(self.time, (660, 300))
            screen.blit(self.parabens, (790, 420))
            screen.blit(self.lifes, (810, 360))
            for i in range(self.stars):
                screen.blit(self.star, (790 +75*i, 500))
                
    def update(self):
        self.updateAnimation()
