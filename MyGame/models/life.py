import pygame as pg
from utils.auxiliar import Auxiliar
from constants import *

class Life(pg.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.image = self.get_image()
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def get_image(self) -> pg.surface.Surface:
        image = pg.image.load('assets/life/life.png')
        image = pg.transform.scale(image,(50,25))        
        return image

    def draw(self,screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, RED, self.rect)
        screen.blit(self.image,self.rect)
    
    def do_kill(self):
        self.kill()