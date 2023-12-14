import pygame as pg
from constants import *

class Plataform(pg.sprite.Sprite):
    def __init__(self, coord_x: int, coord_y: int):
        super().__init__()
        self.__block_img = pg.image.load("assets/block/block.png")
        self.__rect = self.__block_img.get_rect()
        self.__rect.x = coord_x
        self.__rect.y = coord_y
        self.__rect_collition = pg.Rect(self.__rect.x,self.__rect.y,self.__rect.w, 5)

    def draw(self,screen: pg.surface.Surface):
        screen.blit(self.__block_img,self.__rect)
        if(DEBUG):
            pg.draw.rect(screen,RED,self.__rect_collition)

    def get_rect_collition(self):
        return self.__rect_collition