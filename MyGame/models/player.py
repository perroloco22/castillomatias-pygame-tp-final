import pygame as pg
from utils.auxiliar import Auxiliar
from constants import *

class Player(pg.sprite.Sprite):
    def __init__(self, coord_x: int, coord_y: int, speed_walk:int, speed_run: int, frame_rate: int, jump: int, gravity: int):
        super().__init__()
          

        self.__stay_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/stay/iddle.png',4,1,aumentar=1.2)
        self.__stay_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/stay/iddle.png',4,1,flip=True,aumentar=1.2)
        self.__walk_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/walk/walk.png',4,1,aumentar=1.2)
        self.__walk_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/walk/walk.png',4,1,flip=True,aumentar=1.2)
        self.__run_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/run/run.png', 4, 1,aumentar=1.2)
        self.__run_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/run/run.png', 4, 1, flip=True,aumentar=1.2)
        self.__jump_up_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/jump/jump_up.png', 6, 1,aumentar=1.2)
        self.__jump_up_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/jump/jump_up.png', 6, 1, flip=True,aumentar=1.2)
        self.__jump_down_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/jump/jump_down.png', 5, 1,aumentar=1.2)
        self.__jump_down_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/jump/jump_down.png', 5, 1, flip=True,aumentar=1.2)
        self.__defense_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/defense/defense.png', 3, 1,aumentar=1.2)
        self.__defense_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/defense/defense.png', 3, 1, flip=True,aumentar=1.2)
        self.__move_x = 0
        self.__move_y = 0

        self.__initial_frame = 0
        self.__actual_animation = self.__stay_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__rect.x = coord_x
        self.__rect.y = coord_y

        self.__is_defending = False

        self.__speed_walk = speed_walk
        self.__speed_run = speed_run

        self.__frame_rate = frame_rate
        self.__player_move_time = 0
        self.__player_animation_time = 0


        self.__is_jumping = False
        self.__speed_jump = jump
        self.__gravity = gravity

        

        self.__is_looking_right = True

        
   
                
    def set_speed_x(self,speed_move):     
        self.__move_x = speed_move

    def set_speed_y(self,speed_move):     
        self.__move_y = speed_move

    def set_animation(self,animations: list[pg.surface.Surface]):        
        if self.__actual_animation != animations:
            self.__initial_frame = 0
            self.__actual_animation = animations

    def check_limit(self):
        return self.check_limit_x() and self.check_limit_y()
    
    def check_limit_x(self):
        validate = False
        if self.__move_x > 0 and self.__rect.right <= ANCHO_VENTANA - self.__move_x :
            validate = True
        if self.__move_x < 0 and self.__rect.left >= 0 - self.__move_x:
            validate = True
        return validate
    
    def check_limit_y(self):
        validate = False
        if self.__move_y > 0 and self.__rect.bottom  <= ALTO_VENTANA - self.__move_y:
            validate = True
        if self.__move_y < 0 and self.__rect.top  >= 0 - self.__move_y:
            validate = True
        return validate
    
    def defense(self):
        if self.__is_looking_right:
            self.set_animation(self.__defense_r)
        else:
            self.set_animation(self.__defense_l)
        self.set_speed_x(0)



    def stay(self):        
        if self.__is_looking_right:
            self.set_animation(self.__stay_r)
        else:
            self.set_animation(self.__stay_l)
        self.set_speed_x(0)
        
    
    def walk(self, direction: str):
        if direction == 'r':
            self.__is_looking_right = True
            self.set_animation(self.__walk_r)
            self.set_speed_x(self.__speed_walk)
        else:
            self.__is_looking_right = False
            self.set_animation(self.__walk_l)
            self.set_speed_x(-self.__speed_walk)


    def run(self, direction: str):
        if direction == 'r':
            self.__is_looking_right = True
            self.set_animation(self.__run_r)
            self.set_speed_x(self.__speed_run)
        else:
            self.__is_looking_right = False
            self.set_animation(self.__run_l)
            self.set_speed_x(-self.__speed_run)      

    def jump(self):        
        if not self.__is_jumping:
            if(self.__actual_animation != self.__jump_up_l and self.__actual_animation != self.__jump_up_r):
                self.__is_jumping = True
                self.set_speed_y(-self.__speed_jump)
                if self.__is_looking_right:
                    print("entra 1")
                    self.set_animation(self.__jump_up_r)
                else:
                    print("entra 2")
                    self.set_animation(self.__jump_up_l)
                


        


    def get_movements(self):
        keys_pressed = pg.key.get_pressed()
        if not keys_pressed[pg.K_RIGHT] and not keys_pressed[pg.K_LEFT] and not keys_pressed[pg.K_LCTRL] and not keys_pressed[pg.K_SPACE]:
            self.stay()
        if keys_pressed[pg.K_RIGHT] and keys_pressed[pg.K_LEFT]:
            self.stay() 
        if keys_pressed[pg.K_LCTRL] and not keys_pressed[pg.K_RIGHT] and not keys_pressed[pg.K_LEFT]:
            self.defense()        
        if keys_pressed[pg.K_RIGHT] and not keys_pressed[pg.K_LEFT] and not keys_pressed[pg.K_LCTRL] :
            self.walk(direction='r')
        if keys_pressed[pg.K_LEFT] and not keys_pressed[pg.K_RIGHT] and not keys_pressed[pg.K_LCTRL] :
            self.walk(direction='l')        
        if keys_pressed[pg.K_RIGHT] and keys_pressed[pg.K_LSHIFT] and not keys_pressed[pg.K_LEFT] and not keys_pressed[pg.K_LCTRL]:
            self.run('r')
        if keys_pressed[pg.K_LEFT] and keys_pressed[pg.K_LSHIFT] and not keys_pressed[pg.K_RIGHT] and not keys_pressed[pg.K_LCTRL]:
            self.run('l')
        if keys_pressed[pg.K_SPACE]:
            self.jump()
         
    
    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0

    
    def do_movement(self, delta_ms):
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0

            if self.__is_jumping:
                self.__rect.y += self.__move_y
                self.__move_y += self.__gravity
                if self.__move_y == self.__speed_jump + self.__gravity:
                    self.__is_jumping = False
                    self.__move_y = 0
                    self.__move_x = 0   
                    self.stay()            

            if self.check_limit_x():
                self.__rect.x += self.__move_x
            else:
                self.__rect.x += 0            
 
    def update(self,delta_ms):
        self.get_movements()
        self.do_animation(delta_ms)
        self.do_movement(delta_ms)
        
        
    def draw(self,screen: pg.surface.Surface):
        if(DEBUG):
            pg.draw.rect(screen,BLUE,self.__rect)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation,self.__rect)

