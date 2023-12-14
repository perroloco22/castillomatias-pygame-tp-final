import pygame as pg
from utils.auxiliar import Auxiliar
from constants import *


class Trap(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()        
        self.__image = self.get_image()
        self.__rect = self.__image.get_rect(center=(pos_x, pos_y))
        self.__speed = 10
        self.__move_time = 0
        self.__frame_rate = 50
        self.__is_looking_right = True


    def get_image(self) -> pg.surface.Surface:
        image = pg.image.load('assets/trap/trap.png')
        image = pg.transform.scale(image,(30,20))        
        return image
    
    def borders_limit(self):
        if self.__rect.right > ANCHO_VENTANA - 2:
            self.__is_looking_right = False
        elif self.__rect.left < 2:
            self.__is_looking_right = True
    

    def do_movement(self,delta_ms):
        self.__move_time += delta_ms
        if self.__move_time >= self.__frame_rate:
            self.__move_time = 0
            self.borders_limit()
            if self.__is_looking_right:
                self.__rect.x += self.__speed                
            else:
                self.__rect.x -= self.__speed                
            

    def update(self,delta_ms):
        self.do_movement(delta_ms)

    def draw(self,screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, RED, self.__rect)
        screen.blit(self.__image,self.__rect)