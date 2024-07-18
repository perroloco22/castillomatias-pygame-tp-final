from typing import Any
import pygame as pg
from utils.auxiliar import Auxiliar
from constants import *


class Fruit(pg.sprite.Sprite):
    def __init__(self,coord_x: int, coord_y: int):
        self.__img = pg.image.load("assets/fruits/fruit.png")
        self.__rect = self.__img.get_rect()
        self.__rect.x = coord_x
        self.__rect.y = coord_y
        self.__moov_up = True
        self.__player_move_time = 0
        self.__frame_rate = 150
        self.__limit_up = self.__rect.centery - 2
        self.__limit_down = self.__rect.centery + 2
        self.__move_y = -1


    def limit_movement(self):
        if self.__rect.centery < self.__limit_up or self.__rect.centery > self.__limit_down:
            self.__moov_up = not self.__moov_up

    def do_movement(self,delta_ms):
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            self.limit_movement()
            if self.__moov_up:
                self.__rect.y += self.__move_y
            else:
                self.__rect.y -= self.__move_y

    def update(self, delta_ms) -> None:
        self.do_movement(delta_ms)


    def draw(self,screen: pg.surface.Surface):
        if(DEBUG):
            pg.draw.rect(screen,BLUE,self.__rect)
        screen.blit(self.__img,self.__rect)
