import pygame as pg
from cagney import Cagney
from player import Player
pg.init()

clock = pg.time.Clock()

boomerang_group = pg.sprite.GroupSingle()
cagney_group = pg.sprite.GroupSingle()
peashot_group = pg.sprite.Group()
player_group = pg.sprite.GroupSingle()


def load(): 
  global ground, cagney, jogador
  ground = pg.Rect(0, 600, 1280, 120) 
  cagney = Cagney(1000, 400, 200, boomerang_group) 
  cagney_group.add(cagney)
  healthPoints = 3
  jogador = Player(100, 550, healthPoints, peashot_group) # unica variavel classe player
  player_group.add(jogador)

def draw(screen):
  global playerTime, frames
  screen.fill((255,255,255))
  pg.draw.rect(screen,(255,0,0), (ground),2)

  cagney.update(screen)
  cagney_group.draw(screen)
  boomerang_group.draw(screen)
  boomerang_group.update()  
  jogador.update(screen, cagney_group, boomerang_group)
  player_group.draw(screen)
  peashot_group.draw(screen)
  enemy = cagney
  peashot_group.update(enemy, peashot_group)  #projectiles group parametro ->  speed:
      
screen = pg.display.set_mode((1280, 720))
running = True
load()

while running:
  clock.tick(60)
  for e in pg.event.get():
      
      if e.type == pg.QUIT:
          running = False
          break
      elif e.type == pg.KEYDOWN:
        if e.key == pg.K_SPACE:
          jogador.jump = True
      
        
  dt = clock.get_time()
  draw(screen)
  pg.display.update()

pg.quit()