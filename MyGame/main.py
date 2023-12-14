import pygame as pg
import sys
from constants import *
from models.builderPlataform import BuilderPlataform
from models.bullet import Bullet
from models.player import Player
from models.enemy import Enemy
from models.plataform import Plataform
from models.trap import Trap

screen = pg.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pg.init()
clock = pg.time.Clock()
imagen_fondo = pg.image.load("assets/background/fondo2.png")
imagen_fondo = pg.transform.scale(imagen_fondo,(ANCHO_VENTANA,ALTO_VENTANA))

player = Player(0,495,frame_rate=70, speed_walk=15, speed_run=30, jump=50, gravity=10)
enemy = Enemy(700,500,frame_rate=100,speed_run=40,speed_walk=15)
builder_pf = BuilderPlataform()
plataforms = builder_pf.Build_plataform()


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    screen.blit(imagen_fondo,imagen_fondo.get_rect())  

    for block in plataforms:
        block.draw(screen)

    delta_ms = clock.tick(FPS)
    player.update(delta_ms,plataforms)
    player.draw(screen)
    enemy.update(delta_ms)
    enemy.draw(screen)
    
    pg.display.update()

    