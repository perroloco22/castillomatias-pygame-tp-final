import pygame as pg
import sys
from constants import *
from models.player import Player
from models.enemy import Enemy

screen = pg.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pg.init()
clock = pg.time.Clock()
imagen_fondo = pg.image.load("assets/background/fondo2.png")
imagen_fondo = pg.transform.scale(imagen_fondo,(ANCHO_VENTANA,ALTO_VENTANA))

player = Player(0,200,frame_rate=70, speed_walk=15, speed_run=30, jump=40, gravity=10)
enemy = Enemy(0,0,frame_rate=100,speed_run=40,speed_walk=15)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        
 

    screen.blit(imagen_fondo,imagen_fondo.get_rect())  

    delta_ms = clock.tick(FPS)
    player.update(delta_ms)
    player.draw(screen)
    enemy.update(delta_ms)
    enemy.draw(screen)
    pg.display.update()

    