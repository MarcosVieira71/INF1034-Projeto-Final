import pygame as pg
class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pg.image.load("miscellaneous/Platform_A_01.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = [x, y])
        self.mask = pg.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, (self.x,self.y))
        pg.draw.rect(screen, (255,0,0), self.rect, 2)
        