from typing import Any
import pygame as pg
from utils.auxiliar import Auxiliar
from constants import *


class Fruit(pg.sprite.Sprite):
    def __init__(self,coord_x: int, coord_y: int):
        super().__init__()

        self.image = pg.image.load("assets/fruits/fruit.png")
        self.rect = self.image.get_rect()
        self.rect.x = coord_x
        self.rect.y = coord_y
        self.moov_up = True
        self.player_move_time = 0
        self.frame_rate = 150
        self.limit_up = self.rect.centery - 2
        self.limit_down = self.rect.centery + 2
        self.move_y = -1


    def limit_movement(self):
        if self.rect.centery < self.limit_up or self.rect.centery > self.limit_down:
            self.moov_up = not self.moov_up

    def do_movement(self,delta_ms):
        self.player_move_time += delta_ms
        if self.player_move_time >= self.frame_rate:
            self.player_move_time = 0
            self.limit_movement()
            if self.moov_up:
                self.rect.y += self.move_y
            else:
                self.rect.y -= self.move_y

    def update(self, delta_ms) -> None:
        self.do_movement(delta_ms)


    def draw(self,screen: pg.surface.Surface):
        if(DEBUG):
            pg.draw.rect(screen,BLUE,self.rect)
        screen.blit(self.image,self.rect)
    
    def do_kill(self):
        self.kill()