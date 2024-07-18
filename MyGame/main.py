import pygame as pg
import sys
from constants import *
from models.builderPlataform import BuilderPlataform
from models.bullet import Bullet
from models.draw_life import Life
from models.fruits import Fruit
from models.player import Player
from models.enemy import Enemy
from models.plataform import Plataform
from models.trap import Trap

screen = pg.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pg.init()
clock = pg.time.Clock()
imagen_fondo = pg.image.load("assets/background/fondo2.png")
imagen_fondo = pg.transform.scale(imagen_fondo,(ANCHO_VENTANA,ALTO_VENTANA))

enemy = Enemy(700,500,frame_rate=100,speed_run=40,speed_walk=15)
builder_pf = BuilderPlataform()
plataforms = builder_pf.Build_plataform()
player = Player(0,495,frame_rate=70, speed_walk=15, speed_run=30, jump=50, gravity=10,list_of_plataforms=plataforms)
bullet_example = Bullet(50,50,True)
trap_example = Trap(0,500)
life_example1 = Life(0,0)
life_example2 = Life(50,0)
life_example3 = Life(100,0)
fruit_example = Fruit(100,100)


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    screen.blit(imagen_fondo,imagen_fondo.get_rect())  

    for block in plataforms:
        block.draw(screen)

    # if player.finished_shoot():
    #     rect_player = player.get_position()
    #     bullet_coord_y = rect_player.centery + 3
    #     bullet_coord_x = rect_player.right + 8 if player.is_looking_right() else rect_player.left - 8
    #     bullet_example = Bullet(bullet_coord_x,bullet_coord_y,player.is_looking_right())
        


    delta_ms = clock.tick(FPS)
    life_example1.draw(screen)
    life_example2.draw(screen)
    life_example3.draw(screen)
    fruit_example.update(delta_ms)
    fruit_example.draw(screen)
    player.update(delta_ms)
    player.draw(screen)
    # bullet_example.update(delta_ms)
    # bullet_example.draw(screen)
    trap_example.update(delta_ms)
    trap_example.draw(screen)
    enemy.update(delta_ms)
    enemy.draw(screen)
    
    pg.display.update()

    