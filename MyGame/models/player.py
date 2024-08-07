import pygame as pg
from models.bullet import Bullet
from models.plataform import Plataform
from utils.auxiliar import Auxiliar
from models.life import Life
from constants import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, coord_x: int, coord_y: int, speed_walk:int, speed_run: int, frame_rate: int, gravity: int, list_of_plataforms: list[Plataform]):
        super().__init__()

        self.stay_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/stay/iddle.png',4,1,aumentar=1.1)
        self.stay_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/stay/iddle.png',4,1,flip=True,aumentar=1.1)
        self.walk_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/walk/walk.png',4,1,aumentar=1.1)
        self.walk_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/walk/walk.png',4,1,flip=True,aumentar=1.1)
        self.run_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/run/run.png', 4, 1,aumentar=1.1)
        self.run_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/run/run.png', 4, 1, flip=True,aumentar=1.1)
        self.jump_up_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/jump/jump_up.png', 6, 1,aumentar=1.1)
        self.jump_up_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/jump/jump_up.png', 6, 1, flip=True,aumentar=1.1)
        self.shoot_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/shoot/shoot.png', 11, 1,aumentar=1.1)
        self.shoot_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/shoot/shoot.png', 11, 1, flip=True,aumentar=1.1)
        self.defense_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/defense/defense.png', 3, 1,aumentar=1.1)
        self.defense_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/defense/defense.png', 3, 1, flip=True,aumentar=1.1)
        self.death_r = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/death/death.png', 11, 1,aumentar=1.1)
        self.death_l = Auxiliar.getSurfaceFromSpriteSheet(f'{IMAGES_PATH}player/death/death.png', 11, 1,flip=True,aumentar=1.1)

        self.initial_frame = 0
        self.actual_animation = self.stay_r
        self.image = self.actual_animation[self.initial_frame]
        self.rect = self.image.get_rect()
        self.direction = vec(0,0)
        self.pos = vec((coord_x,coord_y))
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.pos_initial_x = coord_x
        self.pos_initial_y = coord_y

        self.is_defending = False

        self.speed_walk = speed_walk
        self.speed_run = speed_run

        self.frame_rate = frame_rate
        self.player_move_time = 0
        self.player_animation_time = 0

        self.initial_jump = -20
        self.gravity = gravity
        self.list_of_plataforms = list_of_plataforms
        self.on_ground = None

        self.looking_right = True
        self.rect_collition = pg.Rect(self.rect.x + self.rect.w/10 ,self.rect.y + self.rect.h - 10,self.rect.w/1.18, 10)

        self.rect_energy_back = pg.Rect(700,0,100,25)
        self.rect_energy_blue = pg.Rect(700,0,100,25)


        self.ready = True
        self.shoot_time = 0
        self.shoot_cooldown = 600
        self.bullet_list : list[Bullet] = [];

        self.frame_rate_death = 150 
        self._is_dead = False
        self.amount_lifes = 3
        self.lifes_group = pg.sprite.Group()
        self.lifes_list = []
        self.create_life(self.amount_lifes)
    
    def finished_animation_death(self):
        return self._is_dead and self.initial_frame == len(self.death_r) - 1
 
    def get_lifes_group(self):
        return self.lifes_group

    def create_life(self,count:int):
        count_life_x = 0
        for life in range(count):
            life = Life(count_life_x,0)
            self.lifes_group.add(life)
            self.lifes_list.append(life)
            count_life_x += 50
    
    def set_width_energy_blue(self, new_width):
        self.rect_energy_blue.width=new_width

    def add_life(self):
        if self.amount_lifes < 3:
            count_life_x = self.amount_lifes * 50
            life = Life(count_life_x,0)
            self.lifes_group.add(life)
            self.lifes_list.append(life)
            self.amount_lifes += 1

    def quit_life(self):
        self.amount_lifes -= 1

    def remove_life(self):
        self.quit_life()        
        if self.lifes_list:
            life_deleted : Life= self.lifes_list.pop()
            self.lifes_group.remove(life_deleted)
            life_deleted.do_kill()

    def get_lifes(self):
        return self.amount_lifes
    
    def reboot_position(self):
        if self.amount_lifes > 0:
            self.pos.x = self.pos_initial_x
            self.pos.y = self.pos_initial_y
            self.direction.x = 0
            self.direction.y = 0
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y
            self.rect_collition.x = self.rect.x + self.rect.w/10 
            self.rect_collition.y = self.rect.y + self.rect.h - 10
                
    def set_speed_x(self,speed_move):
        self.direction.x = speed_move

    def set_speed_y(self,speed_move):     
        self.direction.y = speed_move

    def add_x(self,delta_x):
        self.pos.x = delta_x
        self.rect.x += self.pos.x
        self.rect_collition.x += self.pos.x
    
    def add_y(self,delta_y):
        self.pos.x = delta_y
        self.rect.y += self.pos.x
        self.rect_collition.y += self.pos.x

    def set_animation(self,animations: list[pg.surface.Surface]):        
        if self.actual_animation != animations:
            self.initial_frame = 0
            self.actual_animation = animations

    def check_limit(self):
        return self.check_limit_x() and self.check_limit_y()
    
    def check_limit_x(self):
        validate = False
        if self.direction.x > 0 and self.rect.right <= ANCHO_VENTANA - self.direction.x :
            validate = True
        if self.direction.x < 0 and self.rect.left >= 0 - self.direction.x:
            validate = True
        return validate
    
    def check_limit_y(self):
        validate = False
        if self.direction.y > 0 and self.rect.bottom  <= ALTO_VENTANA :
            validate = True
        if self.direction.y < 0 and self.rect.top  >= 25:
            validate = True
        return validate
    
    def death(self):
        self.is_defending = True   
        if self.looking_right:
            self.set_animation(self.death_r)
        else:
            self.set_animation(self.death_l)
        self.set_speed_x(0)
        # self.set_speed_y(0)

    def defense(self):
        self.is_defending = True   
        if self.looking_right:
            self.set_animation(self.defense_r)
        else:
            self.set_animation(self.defense_l)
        self.set_speed_x(0)

    def stay(self):
        self.is_defending = False   
        if self.looking_right:
            self.set_animation(self.stay_r)
        else:
            self.set_animation(self.stay_l)
        self.set_speed_x(0)
    
    def walk(self, direction: str):
        self.is_defending = False   

        if direction == 'r':
            self.looking_right = True
            self.set_animation(self.walk_r)
            self.set_speed_x(self.speed_walk)
        else:
            self.looking_right = False
            self.set_animation(self.walk_l)
            self.set_speed_x(-self.speed_walk)

    def run(self, direction: str):
        self.is_defending = False   

        if direction == 'r':
            self.looking_right = True
            self.set_animation(self.run_r)
            self.set_speed_x(self.speed_run)
        else:
            self.looking_right = False
            self.set_animation(self.run_l)
            self.set_speed_x(-self.speed_run)      

    def jump(self):
        self.is_defending = False   
        if self.on_ground:
            if(self.actual_animation != self.jump_up_l and self.actual_animation != self.jump_up_r):
                if self.looking_right:
                    self.set_animation(self.jump_up_r)
                else:
                    self.set_animation(self.jump_up_l)
                
    def shoot(self):
        self.is_defending = False
        if self.looking_right:
            self.set_animation(self.shoot_r)
        else:
            self.set_animation(self.shoot_l)
        self.set_speed_x(0)

    def recharge(self):
        if not self.ready:
            self.rect_energy_blue.width += 10
            curent_time = pg.time.get_ticks()
            if curent_time - self.shoot_time >= self.shoot_cooldown:
                self.ready = True
                self.rect_energy_blue.width = 100

    def is_shooting(self) -> bool:
        return self.actual_animation == self.shoot_l or self.actual_animation == self.shoot_r

    def finished_shoot(self) -> bool:
        return self.is_shooting() and self.initial_frame == len(self.shoot_l) - 4

    def update_position_bullets(self,delta_ms):
        for bullet in self.bullet_list:
            bullet: Bullet
            bullet.update(delta_ms)

    def draw_positions_bullets(self, screen: pg.surface.Surface):
        for bullet in self.bullet_list:
            bullet: Bullet
            bullet.draw(screen)
    
    def update_amount_bullets(self):
        self.bullet_list = [elemento for elemento in self.bullet_list if not elemento.is_out()]
    
    def get_bullets(self) -> list[Bullet]:
        return self.bullet_list

    def get_position(self):
        return self.rect
    
    def is_looking_right(self):
        return self.looking_right

    def get_movements(self):
        if self.amount_lifes >= 0:
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
            if keys_pressed[pg.K_SPACE] and self.on_ground:
                self.jump()
                self.direction.y = self.initial_jump
                self.on_ground = False
            if keys_pressed[pg.K_RCTRL] and self.ready and self.on_ground:
                self.shoot()
                self.ready = False
                self.shoot_time = pg.time.get_ticks()
        else:
            self.death()
            self.frame_rate = self.frame_rate_death
            self._is_dead = True

    def collisions_plataforms(self):
        for plataform in self.list_of_plataforms:
            if(self.rect_collition.colliderect(plataform.get_rect_collition())):
                self.rect.bottom = plataform.rect.top
                self.rect_collition.bottom = plataform.rect.top
                self.pos.y = self.rect.y
                self.direction.y = 0
                self.on_ground = True
                break
            else:
                self.on_ground = False
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.pos.y += self.direction.y
        self.rect.y = self.pos.y
        self.rect_collition.y = self.rect.bottom - 10

    def movement_horizontal(self):
        if self.check_limit_x():
                self.add_x(self.direction.x)
        else:
            self.set_speed_x(0)
            self.add_x(self.direction.x)
            
    def movement_vertical(self):
        if self.check_limit_y():
                self.add_y(self.direction.y)
        else:
            self.set_speed_y(0)
            self.add_y(self.direction.y)
        self.apply_gravity()
        self.collisions_plataforms()

    def do_movement(self, delta_ms):
        self.player_move_time += delta_ms
        if self.player_move_time >= self.frame_rate:
            self.player_move_time = 0
            self.movement_horizontal()
            self.movement_vertical()

    def do_animation(self, delta_ms):
            self.player_animation_time += delta_ms
            if self.player_animation_time >= self.frame_rate:
                self.player_animation_time = 0
                if self.finished_shoot():
                    self.set_width_energy_blue(0)
                    bullet_coord_y = self.rect.centery + 3
                    bullet_coord_x = self.rect.right + 8 if self.looking_right else self.rect.left - 8
                    self.bullet_list.append(Bullet(bullet_coord_x,bullet_coord_y,self.looking_right))
                if self.initial_frame < len(self.actual_animation) - 1:
                    self.initial_frame += 1
                else:
                    self.initial_frame = 0
    
    def update(self,delta_ms):
        self.get_movements()
        self.recharge()
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
        self.update_amount_bullets()
        self.update_position_bullets(delta_ms)
        
    def draw(self,screen: pg.surface.Surface):
        if(DEBUG):
            pg.draw.rect(screen,BLUE,self.rect)
            pg.draw.rect(screen,GREEN,self.rect_collition)
        self.image = self.actual_animation[self.initial_frame]
        self.draw_positions_bullets(screen)
        pg.draw.rect(screen,NEGRO,self.rect_energy_back)
        pg.draw.rect(screen,CELESTE,self.rect_energy_blue)
        screen.blit(self.image,self.rect)
    
    