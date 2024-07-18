import pygame as pg
from utils.auxiliar import Auxiliar
from constants import *

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction: bool):
        super().__init__()        
        self.__image = self.get_image(direction)
        self.__rect = self.__image.get_rect(center=(pos_x, pos_y))
        self.__speed = 20
        self.__direction = direction
        self.__move_time = 0
        self.__frame_rate = 50
        self.__is_out = False

    def get_image(self,direction:bool) -> pg.surface.Surface:
        image = pg.image.load('assets/bullet/bullet.png')
        image = pg.transform.scale(image,(30,30))
        if not direction:
            image = pg.transform.flip(image,True,False)
        return image

    def do_movement(self,delta_ms):
        self.__move_time += delta_ms
        if self.__move_time >= self.__frame_rate:
            self.__move_time = 0
            if self.__direction:
                self.__rect.x += self.__speed                
            else:
                self.__rect.x -= self.__speed                
            if self.__rect.x < 0 or self.__rect.x > ANCHO_VENTANA:
                self.kill()
                self.__is_out = True

    def is_out(self) -> bool:
        return self.__is_out

    def update(self,delta_ms):
        self.do_movement(delta_ms)

    def draw(self,screen: pg.surface.Surface):
        if(DEBUG):
            pg.draw.rect(screen,BLUE,self.__rect)
        screen.blit(self.__image,self.__rect)