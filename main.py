import pygame as pg
from cagney import Cagney
from player import Player
from message import Message
from floor import TileMap
from plataforma import Platform
from menu import Menu

pg.init()

clock = pg.time.Clock()

boomerang_group = pg.sprite.GroupSingle()
cagney_group = pg.sprite.GroupSingle()
peashot_group = pg.sprite.Group()
player_group = pg.sprite.GroupSingle()
message_group = pg.sprite.GroupSingle()
menu_group = pg.sprite.GroupSingle()
  
def load(status, stars, time): 
  global ground, enemy, jogador, platform1, platform2, knockout, ready, intro, youDied, readySound, youDiedSound, knockoutSound, healthDead, ultIcon, tile_map, menu, background, life
  youDied = pg.image.load("miscellaneous/youDied.png").convert_alpha()
  ultIcon = pg.image.load("projectiles/ult/ult_0001.png").convert_alpha()
  ultIcon = pg.transform.scale(ultIcon, (50,25))
  pg.mixer.init()
  if status == "win":
     menu = Menu("win", stars, time)
     menu_group.add(menu)
     pg.mixer.music.load("win/victoryTunes.mp3")
     pg.mixer.music.set_volume(0.3)
     pg.mixer.music.play(-1)

  elif status == "start":
    menu = Menu("principal", None, None)
    menu_group.add(menu)
    pg.mixer.music.load("miscellaneous/naoMexaComOCapeta.mp3")
    pg.mixer.music.set_volume(0.3)
    pg.mixer.music.play(-1)

  elif status == "tutorial":
     menu_group.remove(menu)
     menu = Menu("tutorial", None,None)
     pg.mixer.music.load("miscellaneous/naoMexaComOCapetaInstrumental.mp3")
     pg.mixer.music.set_volume(0.3)
     pg.mixer.music.play(-1)
     
  elif status == "playing":
    ground = pg.Rect(0, 600, 1280, 120) 
    background = pg.image.load('miscellaneous/background.png').convert_alpha()
    tile_map = TileMap(1280, 720)
    tile_map.load_map("map/file.txt")
    tile_map.load_tiles()
    enemy = Cagney(1110, 500,100, boomerang_group) 
    cagney_group.add(enemy)
    intro = True
    jogador = Player(10, 600, 3, peashot_group) 
    player_group.add(jogador)
    platform1 = Platform(150, 275)
    platform2 = Platform(550, 275)
    ready = Message(-20, -50, "messages","FightText_GetReady",51, 0.4)
    knockout = Message(0, 0, "messages", "FightText_KO", 26, 0.4)
    knockoutSound = False
    readySound = False
    youDiedSound = False 
    pg.mixer.music.load("miscellaneous/FloralFury.mp3")
    pg.mixer.music.set_volume(0.3)
    pg.mixer.music.play(-1)
    


def draw(screen,status):
  global health, background

  if status == "win":
     menu.draw(screen)
     menu_group.draw(screen)

  elif status == "start":
      menu.draw(screen)
      menu_group.draw(screen)

  elif status == "tutorial":
      menu.draw(screen)
      
  elif status == "playing":
    screen.blit(background, (0, 0))
    tile_map.draw(screen)
    health = pg.image.load(f"miscellaneous/health{jogador.life}.png").convert_alpha()
    cagney_group.draw(screen)
    boomerang_group.draw(screen)
    player_group.draw(screen)
    platform1.draw(screen)
    platform2.draw(screen)
    for i in range(jogador.charge//100):
      screen.blit(ultIcon, (100+50*i,680))
    peashot_group.draw(screen)
    screen.blit(health, (0,680))
  
  



def update(status):
    global intro, readySound, knockoutSound, youDiedSound

    if status == "win":
      menu.update()

    elif status == "start":
        menu.update()

    elif status == "playing":
      enemy.update(screen)
      boomerang_group.update()  
      jogador.update(screen, enemy, platform1, platform2, ground)
      peashot_group.update(enemy)

      if intro:
        
        message_group.add(ready)
        message_group.update()
        message_group.draw(screen)
        if not readySound: 
          announcer1 = pg.mixer.Sound("sfx/announcerCuphead.mp3")
          announcer1.set_volume(0.4)
          pg.mixer.Sound.play(announcer1)
          readySound = True
        if ready.index == 50:
          message_group.remove(ready)
          intro = False
          message_group.add(knockout)
    
      if enemy.death: 
          message_group.draw(screen)
          if not knockoutSound:
            announcer2 = pg.mixer.Sound("sfx/announcer_knockout_0004.wav")
            announcer2.set_volume(0.4)
            pg.mixer.Sound.play(announcer2)
            knockoutSound = True
          message_group.update()
          if knockout.index == 25:
            knockout.index = 25
            message_group.remove(knockout)
      elif jogador.death:
        if not youDiedSound:
          deathsound = pg.mixer.Sound("sfx/player_death_01.wav")
          pg.mixer.Sound.play(deathsound)
          deathsound.set_volume(0.3)
          youDiedSound = True
        screen.blit(youDied, (125,200))


status = "start"
screen = pg.display.set_mode((1280, 720))
running = True
stars = 3
time = 0
load(status, stars, time)
qCount = 0
while running:
  clock.tick(60)
  for e in pg.event.get():
      if e.type == pg.QUIT:
          running = False
          break
      elif e.type == pg.KEYDOWN:
        if e.key == pg.K_SPACE:
          jogador.jump = True
        if e.key == pg.K_q:
           if qCount == 0:
              status = "tutorial"
           elif qCount == 1:
              status = "playing"
              time = pg.time.get_ticks()
           elif qCount == 2:
              if enemy.death:
                 timeWin = pg.time.get_ticks()
                 time = (timeWin - time)//1000
                 timemin = time//60
                 timesec = time%60
                 time = [timemin, timesec]
                 stars = jogador.life
                 status = "win"
              else:
                status = "start"  
                qCount = 0
           qCount+=1
           load(status, stars, time)


  dt = clock.get_time()
  draw(screen, status)
  update(status)
  pg.display.update()

pg.quit()