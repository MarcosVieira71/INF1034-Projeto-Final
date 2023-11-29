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

