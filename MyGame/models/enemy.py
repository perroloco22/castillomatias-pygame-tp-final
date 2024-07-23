import pygame as pg
from utils.auxiliar import Auxiliar
from constants import *

class Enemy(pg.sprite.Sprite):
    def __init__(self, coord_x: int, coord_y: int, speed_walk:int, speed_run: int, frame_rate: int):
        super().__init__()

        self.stay_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/stay/stay.png',6,1)
        self.stay_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/stay/stay.png',6,1,flip=True)
        self.birth_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/birth/birth.png',8,1)
        self.birth_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/birth/birth.png',8,1, flip=True)
        self.walk_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/walk/walk.png',3,1)
        self.walk_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/walk/walk.png',3,1,flip=True)
        self.run_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/run/run.png', 4, 1)
        self.run_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/run/run.png', 4, 1, flip=True)
        self.pos_initial_x = coord_x
        self.pos_initial_y = coord_y

        self.move_x = 0

        self.count=0
        self.limit_run = 20
        self.limit_walk = 100

        self.is_birth = True
        self.is_walking = False
        self.is_run = False

        self.speed_walk = speed_walk
        self.speed_run = speed_run
        self.frame_rate = frame_rate
        self.player_move_time = 0
        self.player_animation_time = 0

        self.is_looking_right = True

        self.initial_frame = 0
        self.actual_animation = self.birth_r
        self.image = self.actual_animation[self.initial_frame]
        self.rect = self.image.get_rect()
        self.rect.x= coord_x
        self.rect.y= coord_y

    def reboot_position(self):
        self.rect.x = self.pos_initial_x
        self.rect.y = self.pos_initial_y
        self.is_birth = True

    def borders_limit(self):
        if self.rect.right > ANCHO_VENTANA - 2:
            self.is_looking_right = False
        elif self.rect.left < 2:
            self.is_looking_right = True

    def set_speed_and_animation(self,speed_move:int, animations: list[pg.surface.Surface]):        
        if self.actual_animation != animations:
            self.initial_frame = 0
            self.actual_animation = animations
        self.move_x = speed_move 

    def birth(self):
        if self.initial_frame == len(self.birth_l) - 1:
            self.is_birth = False
            self.is_walking = True

        if self.is_looking_right:
            self.set_speed_and_animation(0,self.birth_r)
        else:
            self.set_speed_and_animation(0,self.birth_l)

    def stay(self):        
        if self.is_looking_right:
            self.set_speed_and_animation(0,self.stay_r)
        else:
            self.set_speed_and_animation(0,self.stay_l)

    def walk(self):
        if self.is_looking_right:
            self.set_speed_and_animation(self.speed_walk,self.walk_r)
        else:
            self.set_speed_and_animation(-self.speed_walk,self.walk_l)
        self.count += 1
        if self.count == self.limit_walk:
            self.is_run = True
            self.is_walking = False
            self.count = 0
    
    def run(self):
        if self.is_looking_right:
            self.set_speed_and_animation(self.speed_run,self.run_r)
        else:
            self.set_speed_and_animation(-self.speed_run,self.run_l)
        self.count += 1
        if self.count == self.limit_run:
            self.is_run = False
            self.is_walking = True
            self.count = 0
            
    def get_movements(self):
        if self.is_birth:
            self.birth()
        else:
            self.borders_limit()
            if self.is_walking:            
                self.walk()
            elif self.is_run:
                self.run()

    def do_animation(self, delta_ms):
        self.player_animation_time += delta_ms
        if self.player_animation_time >= self.frame_rate:
            self.player_animation_time = 0
            if self.initial_frame < len(self.actual_animation) - 1:
                self.initial_frame += 1
            else:
                self.initial_frame = 0
    
    def do_movement(self, delta_ms):
        self.player_move_time += delta_ms
        if self.player_move_time >= self.frame_rate:
            self.player_move_time = 0
            self.rect.x += self.move_x
 
    def update(self,delta_ms):
        self.get_movements()
        self.do_animation(delta_ms)
        self.do_movement(delta_ms)
        
    def draw(self,screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, RED, self.rect)
        self.image = self.actual_animation[self.initial_frame]
        screen.blit(self.image,self.rect)