import pygame as pg
from utils.auxiliar import Auxiliar
from constants import *

class Enemy(pg.sprite.Sprite):
    def __init__(self, coord_x: int, coord_y: int, speed_walk:int, speed_run: int, frame_rate: int):
        super().__init__()
          

        self.__stay_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/stay/stay.png',6,1)
        self.__stay_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/stay/stay.png',6,1,flip=True)
        self.__birth_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/birth/birth.png',8,1)
        self.__birth_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/birth/birth.png',8,1, flip=True)
        self.__walk_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/walk/walk.png',3,1)
        self.__walk_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/walk/walk.png',3,1,flip=True)
        self.__run_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/run/run.png', 4, 1)
        self.__run_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}enemy/run/run.png', 4, 1, flip=True)
        
        self.__move_x = 0

        self.__count=0
        self.__limit_run = 20
        self.__limit_walk = 100


        self.__is_birth = True
        self.__is_walking = False
        self.__is_run = False

        self.__speed_walk = speed_walk
        self.__speed_run = speed_run
        self.__frame_rate = frame_rate
        self.__player_move_time = 0
        self.__player_animation_time = 0


        self.__is_looking_right = True

        self.__initial_frame = 0
        self.__actual_animation = self.__birth_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__rect.x= coord_x
        self.__rect.y= coord_y

    def borders_limit(self):
        current_direction = self.__is_looking_right        
        if self.__rect.right > ANCHO_VENTANA - 2:
            self.__is_looking_right = False
        elif self.__rect.left < 2:
            self.__is_looking_right = True
        return current_direction == self.__is_looking_right


    def set_speed_and_animation(self,speed_move:int, animations: list[pg.surface.Surface]):        
        if self.__actual_animation != animations:
            self.__initial_frame = 0
            self.__actual_animation = animations
        self.__move_x = speed_move 

    def birth(self):
        if self.__initial_frame == len(self.__birth_l) - 1:
            self.__is_birth = False
            self.__is_walking = True

        if self.__is_looking_right:
            self.set_speed_and_animation(0,self.__birth_r)
        else:
            self.set_speed_and_animation(0,self.__birth_l)

    def stay(self):        
        if self.__is_looking_right:
            self.set_speed_and_animation(0,self.__stay_r)
        else:
            self.set_speed_and_animation(0,self.__stay_l)

    def walk(self):
        if self.__is_looking_right:
            self.set_speed_and_animation(self.__speed_walk,self.__walk_r)
        else:
            self.set_speed_and_animation(-self.__speed_walk,self.__walk_l)
        self.__count += 1
        if self.__count == self.__limit_walk:
            self.__is_run = True
            self.__is_walking = False
            self.__count = 0

    
    def run(self):
        if self.__is_looking_right:
            self.set_speed_and_animation(self.__speed_run,self.__run_r)
        else:
            self.set_speed_and_animation(-self.__speed_run,self.__run_l)
        self.__count += 1
        if self.__count == self.__limit_run:
            self.__is_run = False
            self.__is_walking = True
            self.__count = 0
            
    def get_movements(self):
        if self.__is_birth:
            self.birth()
        else:
            self.borders_limit()
            if self.__is_walking:            
                self.walk()
            elif self.__is_run:
                self.run()


    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0

    
    def do_movement(self, delta_ms):
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            self.__rect.x += self.__move_x
 
    def update(self,delta_ms):
        self.get_movements()
        self.do_animation(delta_ms)
        self.do_movement(delta_ms)
        
        
    def draw(self,screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, RED, self.__rect)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation,self.__rect)