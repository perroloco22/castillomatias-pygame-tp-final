import pygame as pg
from utils.auxiliar import Auxiliar
from constants import *

class Explosion(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y,frame_rate):
        super().__init__()

        self.explosion = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}explosion/explosion.png',7,1)
        
        self.initial_frame = 0
        self.actual_animation = self.explosion
        self.image = self.actual_animation[self.initial_frame]
        self.rect = self.image.get_rect()
        self.rect.x= pos_x
        self.rect.y= pos_y 

        self.finished = False
        self.player_animation_time = 0
        self.frame_rate = frame_rate

    def is_finished(self):
        return self.finished
    
    def do_animation(self, delta_ms):
        self.player_animation_time += delta_ms
        if self.player_animation_time >= self.frame_rate:
            self.player_animation_time = 0
            if self.initial_frame < len(self.actual_animation) - 1:
                self.initial_frame += 1
            else:
                self.finished = True
                self.do_kill()
    
    def update(self,delta_ms):
        self.do_animation(delta_ms)
    
    def draw(self,screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, RED, self.rect)
        self.image = self.actual_animation[self.initial_frame]
        screen.blit(self.image,self.rect)
    
    def do_kill(self):
        self.kill()