import pygame as pg
import sys
from constants import *
from models.builderStage import BuilderStage
from models.life import Life
from models.player import Player
from models.enemy import Enemy
from models.plataform import Plataform
from models.trap import Trap 
from models.fruits import Fruit


screen = pg.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pg.init()
clock = pg.time.Clock()
imagen_fondo = pg.image.load("assets/background/fondo2.png")
imagen_fondo = pg.transform.scale(imagen_fondo,(ANCHO_VENTANA,ALTO_VENTANA))

builder = BuilderStage("level_1")
map = builder.Build_Map()
blocks : list[Plataform]= map["blocks"]
player = Player(0,480,frame_rate=50, speed_walk=15, speed_run=25, jump=20, gravity=1 ,list_of_plataforms=blocks)

fruits : list[Fruit]= map["fruits"]
fruits_group = pg.sprite.Group()
for fruit in fruits:
    fruits_group.add(fruit)

enemies : list[Enemy] = builder.Build_enemies()
enemies_group = pg.sprite.Group()
for enemy in enemies:
    enemies_group.add(enemy)

lifes_group :pg.sprite.Group = player.get_lifes_group()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    screen.blit(imagen_fondo,imagen_fondo.get_rect())  
    for block in blocks:
        block.draw(screen)

    delta_ms = clock.tick(FPS)

    # enemies_collision = []
    for bullet in player.get_bullets():        
        # enemies_collision = pg.sprite.spritecollide(bullet, enemies_group, True)
        pg.sprite.spritecollide(bullet, enemies_group, True)
        
    for enemy in enemies_group:
        if player.rect.colliderect(enemy.rect) and (not player.is_defending or player.looking_right == enemy.is_looking_right):
            enemy.reboot_position()
            player.reboot_position()
            player.remove_life()
    
    for fruit in fruits:
        if player.rect.colliderect(fruit.rect):
            if player.get_lifes() < 3:
                fruits_group.remove(fruit)
                player.add_life()
    
    lifes_group.update()
    lifes_group.draw(screen)

    enemies = [elemento for elemento in enemies_group]
    fruits = [fruit for fruit in fruits_group]

    for fruit in fruits:
        fruit.update(delta_ms)
        fruit.draw(screen)

    for enemy in enemies:
        enemy.update(delta_ms)
        enemy.draw(screen)
    
    player.update(delta_ms)
    player.draw(screen)
    
    pg.display.update()

    