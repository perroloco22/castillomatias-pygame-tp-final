import pygame as pg
from models.bullet import Bullet
from models.plataform import Plataform
from utils.auxiliar import Auxiliar
from constants import *

class Player(pg.sprite.Sprite):
    def __init__(self, coord_x: int, coord_y: int, speed_walk:int, speed_run: int, frame_rate: int, jump: int, gravity: int):
        super().__init__()
          

        self.__stay_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/stay/iddle.png',4,1,aumentar=1.1)
        self.__stay_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/stay/iddle.png',4,1,flip=True,aumentar=1.1)
        self.__walk_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/walk/walk.png',4,1,aumentar=1.1)
        self.__walk_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/walk/walk.png',4,1,flip=True,aumentar=1.1)
        self.__run_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/run/run.png', 4, 1,aumentar=1.1)
        self.__run_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/run/run.png', 4, 1, flip=True,aumentar=1.1)
        self.__jump_up_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/jump/jump_up.png', 6, 1,aumentar=1.1)
        self.__jump_up_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/jump/jump_up.png', 6, 1, flip=True,aumentar=1.1)
        self.__shoot_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/shoot/shoot.png', 11, 1,aumentar=1.1)
        self.__shoot_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/shoot/shoot.png', 11, 1, flip=True,aumentar=1.1)
        self.__defense_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/defense/defense.png', 3, 1,aumentar=1.1)
        self.__defense_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/defense/defense.png', 3, 1, flip=True,aumentar=1.1)
        self.__move_x = 0
        self.__move_y = 0
        self.__amount_lives = 3

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
        self.__rect_collition = pg.Rect(self.__rect.x + self.__rect.w/10 ,self.__rect.y + self.__rect.h - 10,self.__rect.w/1.18, 10)

        self.ready = True
        self.shoot_time = 0
        self.shoot_cooldown = 600

        
    def get_lives(self):
        return self.__amount_lives
                
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
                
    def shoot(self):
        if self.__is_looking_right:
            self.set_animation(self.__shoot_r)
        else:
            self.set_animation(self.__shoot_l)
        self.set_speed_x(0)

        
    def recharge(self):
        if not self.ready:
            curent_time = pg.time.get_ticks()
            if curent_time - self.shoot_time >= self.shoot_cooldown:
                self.ready = True

    def get_movements(self):
        keys_pressed = pg.key.get_pressed()
        if not keys_pressed[pg.K_RIGHT] and not keys_pressed[pg.K_LEFT] and not keys_pressed[pg.K_LCTRL] and not keys_pressed[pg.K_SPACE] and not keys_pressed[pg.K_RCTRL]:
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
        if keys_pressed[pg.K_RCTRL] and self.ready:
            self.shoot()
            self.ready = False
            self.shoot_time = pg.time.get_ticks()
         
    
    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
                print(self.__initial_frame)
            else:
                self.__initial_frame = 0

    
    def do_movement(self, delta_ms,list_of_plataforms: list[Plataform]):
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            if not self.is_on_plataform(list_of_plataforms) and not self.__is_jumping:
                self.add_y(self.__gravity)

            if self.__is_jumping:
                self.add_y(self.__move_y)
                self.__move_y += self.__gravity
                if self.is_on_plataform(list_of_plataforms) or self.__move_y == self.__speed_jump + self.__gravity :
                    self.__is_jumping = False
                    self.__move_y = 0
                    self.__move_x = 0   
                    self.stay()            

            if self.check_limit_x():
                self.add_x(self.__move_x)
            else:
                self.add_x(0)


    def is_on_plataform(self,list_of_plataforms: list[Plataform]):
        result = False
        for plataform in list_of_plataforms:
            if(self.__rect_collition.colliderect(plataform.get_rect_collition())):
                result = True
                break

        return result

    def add_x(self,delta_x):
        self.__rect.x += delta_x
        self.__rect_collition.x += delta_x
    
    def add_y(self,delta_y):
        self.__rect.y += delta_y
        self.__rect_collition.y += delta_y


    def update(self,delta_ms,list_of_plataforms: list[Plataform]):
        self.get_movements()
        self.recharge()
        self.do_animation(delta_ms)
        self.do_movement(delta_ms,list_of_plataforms)
        
        
    def draw(self,screen: pg.surface.Surface):
        if(DEBUG):
            pg.draw.rect(screen,BLUE,self.__rect)
            pg.draw.rect(screen,GREEN,self.__rect_collition)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation,self.__rect)

