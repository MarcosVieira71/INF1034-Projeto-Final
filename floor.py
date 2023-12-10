import pygame as pg

class TileMap:
    def __init__(self, width, height):
        pg.init()
        self.map = []
        self.tile = {}
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((width, height))
        self.platform = pg.image.load("miscellaneous/Platform_A_01.png")
        self.platforms = [(self.platform.get_rect(topleft = [150+i*400, 275])) for i in range(2)] #append 2 retangulos da plataforma.png para ser desenhado no draw

    def load_map(self, filename):
        self.map = []
        file = open(filename, "r")
        for line in file.readlines():
            line = line.rstrip()
            self.map.append(line)
        file.close()

    def load_tiles(self):
        self.tile['A'] = pg.image.load("map/A.png")
        self.tile['B'] = pg.image.load("map/B.png")
        self.tile['C'] = pg.image.load("map/C.png")
        self.tile['D'] = pg.image.load("map/D.png")
        self.tile['E'] = pg.image.load("map/E.png")

    def draw(self, screen):
        for i in range(12):
            for j in range(20):
                self.screen.blit(self.tile[self.map[i][j]], ((j * 64), (i * 60)))
