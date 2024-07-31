import pygame as pg
from utils.auxiliar import Auxiliar
from constants import *

class Trap(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y,move_time,frame_rate,speed):
        super().__init__()        
        self.image = self.get_image()
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.speed = speed
        self.move_time = move_time
        self.frame_rate = frame_rate
        self.is_looking_right = True
        self.do_damage = True
        self.limite_pause_damage = 1500
        self.init_pause = 0

    def pause_damage(self,delta_ms):
        if not self.do_damage:
            self.init_pause+=delta_ms
            if self.init_pause >= self.limite_pause_damage:
                self.init_pause = 0
                self.do_damage = True

    def get_image(self) -> pg.surface.Surface:
        image = pg.image.load('assets/trap/trap.png')
        image = pg.transform.scale(image,(40,30))        
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
        self.pause_damage(delta_ms)

    def draw(self,screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, RED, self.rect)
        screen.blit(self.image,self.rect)