import pygame as pg
from utils.auxiliar import Auxiliar
from constants import *


class Fruit(pg.sprite.Sprite):
    def __init__(self,coord_x: int, coord_y: int):
        self.__img = pg.image.load("assets/fruits/fruit.png")
        self.__rect = self.__img.get_rect()
        self.__rect.x = coord_x
        self.__rect.y = coord_y
    

    def draw(self,screen: pg.surface.Surface):
        if(DEBUG):
            pg.draw.rect(screen,BLUE,self.__rect)
        screen.blit(self.__img,self.__rect)
