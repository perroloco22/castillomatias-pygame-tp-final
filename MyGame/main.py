import pygame as pg
from models.game import Game
import sys

pg.init()

game = Game()

game.run_level()


'''
from constants import *
from models.builderStage import BuilderStage
from models.life import Life
from models.player import Player
from models.enemy import Enemy
from models.plataform import Plataform
from models.trap import Trap 
from models.fruits import Fruit
from models.bullet import Bullet
from models.explosion import Explosion
from models.clock import Clock


screen = pg.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pg.init()
pg.display.set_caption("DBPY")

clock = pg.time.Clock()
imagen_fondo = pg.image.load("assets/background/fondo2.png")
imagen_fondo = pg.transform.scale(imagen_fondo,(ANCHO_VENTANA,ALTO_VENTANA))

builder = BuilderStage("level_3")
map = builder.Build_Map()

blocks : list[Plataform]= map["blocks"]
player = Player(0,480,frame_rate=50, speed_walk=15, speed_run=25, gravity=1 ,list_of_plataforms=blocks)
# player_group = pg.sprite.GroupSingle(player)

fruits : list[Fruit]= map["fruits"]
fruits_group = pg.sprite.Group()
for fruit in fruits:
    fruits_group.add(fruit)

enemies : list[Enemy] = builder.Build_enemies()
enemies_group = pg.sprite.Group()
for enemy in enemies:
    enemies_group.add(enemy)

trap_group = builder.build_trap()

lifes_group :pg.sprite.Group = player.get_lifes_group()

explosion_group = pg.sprite.Group()
primera = True
limit_time = 30000
text_color = (255, 255, 255)
clock2 = Clock(limit_time,text_color,(255, 0, 0),25,'font/font.ttf',800)

while True:
    curren_time = pg.time.get_ticks()
    clock2.run_clock(curren_time)
    # lapse_time = (limit_time - curren_time )//1000
    # font = pg.font.Font("font/font.ttf",25)
    # if lapse_time <= 10:
    #     text_color = (255, 0, 0)  # Rojo
    # # else:
    # #     text_color = (255, 255, 255)  # Blanco
    # number = font.render(f"Tiempo: {lapse_time}s", True, text_color)
    # position = number.get_rect(center = (ANCHO_VENTANA/2,15))

    print(clock2.get_lapse_time())
    # print(lapse_time)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    screen.blit(imagen_fondo,imagen_fondo.get_rect())  
    # screen.blit(number,position)
    screen.blit(clock2.get_surface(),clock2.get_position())
    for block in blocks:
        block.draw(screen)

    delta_ms = clock.tick(FPS)

    if player.finished_animation_death():
        pg.quit()
        sys.exit()
    
    for exp in explosion_group:
        print("HAY EXPLOSIONES")
        if primera:
            primera = not primera
            print("EXPLOSION")
        exp.update(delta_ms)
        exp.draw(screen)

    for bullet in player.get_bullets():        
        # enemies_collision = pg.sprite.spritecollide(bullet, enemies_group, True)
        bullet:Bullet
        if pg.sprite.spritecollide(bullet, enemies_group, True):
            if bullet.direction:
                explosion_group.add(Explosion(bullet.rect.right-20,bullet.rect.top - 20,200))
            else:
                explosion_group.add(Explosion(bullet.rect.left-20,bullet.rect.top - 20,200))
            bullet.do_kill()
    
    for trap in trap_group:
        trap : Trap
        if player.rect.colliderect(trap.rect) and trap.do_damage:
            if player.is_defending:
                player.remove_life()
            else:
                player.remove_life()
                player.remove_life()
                player.reboot_position()
            if trap.is_looking_right:
                explosion_group.add(Explosion(trap.rect.right-20,trap.rect.top - 20,200))
            else:
                explosion_group.add(Explosion(trap.rect.left-20,trap.rect.top - 20,200))
            trap.do_damage = False

        
    for enemy in enemies_group:
        enemy : Enemy
        if player.rect.colliderect(enemy.rect) and (not player.is_defending or player.looking_right == enemy.is_looking_right):
            enemy.reboot_position()
            player.reboot_position()
            player.remove_life()
    
    for fruit in fruits:
        fruit : Fruit
        if player.rect.colliderect(fruit.rect):
            if player.get_lifes() < 3:
                fruits_group.remove(fruit)
                fruit.do_kill()
                player.add_life()
    
    lifes_group.update()
    lifes_group.draw(screen)

    trap_group.update(delta_ms)
    trap_group.draw(screen)

    fruits = [fruit for fruit in fruits_group]

    fruits_group.update(delta_ms)
    fruits_group.draw(screen)
    

    for enemy in enemies_group:
        enemy: Enemy
        enemy.update(delta_ms)
        enemy.draw(screen)

    enemies = [enemy for enemy in enemies_group]
    print("CANTIDAD DE ENEMIGOS")
    print(len(enemies))
    player.update(delta_ms)
    player.draw(screen)
    
    pg.display.update()

'''
    