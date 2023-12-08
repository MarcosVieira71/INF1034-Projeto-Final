import pygame as pg
from cagney import Cagney
from player import Player
from functions import spriteList
from message import Message
pg.init()

clock = pg.time.Clock()

boomerang_group = pg.sprite.GroupSingle()
cagney_group = pg.sprite.GroupSingle()
peashot_group = pg.sprite.Group()
player_group = pg.sprite.GroupSingle()
message_group = pg.sprite.GroupSingle()


def load(): 
  global ground, cagney, jogador, knockout, ready, intro, youDied
  youDied = pg.image.load("youDied.png")
  ground = pg.Rect(0, 600, 1280, 120) 
  cagney = Cagney(900, 510, 10, boomerang_group) 
  cagney_group.add(cagney)
  pg.mixer.init()
  pg.mixer.music.load("FloralFury.mp3")
  pg.mixer.music.play()
  intro = True
  healthPoints = 3
  jogador = Player(100, 600, healthPoints, peashot_group) # unica variavel classe player
  player_group.add(jogador)
  ready = Message(-20, -50, "FightText_GetReady",51, 0.4)
  knockout = Message(0, 0, "FightText_KO", 26, 0.4)




def draw(screen):
  global playerTime, frames, intro
  screen.fill((255,255,0))
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
  if intro:
    message_group.add(ready)
    message_group.update()
    message_group.draw(screen)
    if ready.index == 50:
       message_group.remove(ready)
       intro = False
       message_group.add(knockout)
    
  if cagney.death:
        
        message_group.draw(screen)
        message_group.update()
        if knockout.index == 25:
          message_group.remove(knockout)
  if jogador.death:
    screen.blit(youDied, (125,200))
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