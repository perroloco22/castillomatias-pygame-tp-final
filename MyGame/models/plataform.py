import pygame as pg
from constants import *

class Plataform(pg.sprite.Sprite):
    def __init__(self, coord_x: int, coord_y: int):
        super().__init__()
        self.image = pg.image.load("assets/block/block.png")
        self.rect = self.image.get_rect()
        self.rect.x = coord_x
        self.rect.y = coord_y
        self.rect_collition = pg.Rect(self.rect.x,self.rect.y,self.rect.w, 18)

    def draw(self,screen: pg.surface.Surface):
        screen.blit(self.image,self.rect)
        if(DEBUG):
            pg.draw.rect(screen,RED,self.rect_collition)

    def get_rect_collition(self):
        return self.rect_collition