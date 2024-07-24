import pygame as pg
from utils.auxiliar import Auxiliar
from constants import *

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction: bool):
        super().__init__()        
        self.image = self.get_image(direction)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.speed = 20
        self.direction = direction
        self.move_time = 0
        self.frame_rate = 50
        self.out = False

    def get_image(self,direction:bool) -> pg.surface.Surface:
        image = pg.image.load('assets/bullet/bullet.png')
        image = pg.transform.scale(image,(30,30))
        if not direction:
            image = pg.transform.flip(image,True,False)
        return image

    def do_movement(self,delta_ms):
        self.move_time += delta_ms
        if self.move_time >= self.frame_rate:
            self.move_time = 0
            if self.direction:
                self.rect.x += self.speed                
            else:
                self.rect.x -= self.speed                
            if self.rect.x < 0 or self.rect.x > ANCHO_VENTANA:
                self.do_kill()

    def is_out(self) -> bool:
        return self.out

    def update(self,delta_ms):
        self.do_movement(delta_ms)

    def draw(self,screen: pg.surface.Surface):
        if(DEBUG):
            pg.draw.rect(screen,BLUE,self.rect)
        screen.blit(self.image,self.rect)

    def do_kill(self):
        self.out = True
        self.kill()