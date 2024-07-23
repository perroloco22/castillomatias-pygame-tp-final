import pygame as pg
from utils.auxiliar import Auxiliar
from constants import *


class Trap(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()        
        self.image = self.get_image()
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.speed = 10
        self.move_time = 0
        self.frame_rate = 50
        self.is_looking_right = True


    def get_image(self) -> pg.surface.Surface:
        image = pg.image.load('assets/trap/trap.png')
        image = pg.transform.scale(image,(30,20))        
        return image
    
    def borders_limit(self):
        if self.rect.right > ANCHO_VENTANA - 2:
            self.is_looking_right = False
        elif self.rect.left < 2:
            self.is_looking_right = True
    

    def do_movement(self,delta_ms):
        self.move_time += delta_ms
        if self.move_time >= self.frame_rate:
            self.move_time = 0
            self.borders_limit()
            if self.is_looking_right:
                self.rect.x += self.speed                
            else:
                self.rect.x -= self.speed                
            

    def update(self,delta_ms):
        self.do_movement(delta_ms)

    def draw(self,screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, RED, self.rect)
        screen.blit(self.image,self.rect)