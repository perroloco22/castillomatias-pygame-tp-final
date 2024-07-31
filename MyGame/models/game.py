import pygame as pg
import sys
from constants import *
from models.builderStage import BuilderStage
from models.life import Life
from models.player import Player
from models.enemy import Enemy
from models.plataform import Plataform
from models.trap import Trap 
from models.fruits import Fruit
from models.bullet import Bullet
from models.explosion import Explosion
from models.clock import Clock
from utils.auxiliar import Auxiliar



class Game:
    def __init__(self):
        self.config = Auxiliar.readJson()
        self.window_width = self.config["config"]["ancho"]
        self.window_height = self.config["config"]["alto"]
        self.screen = pg.display.set_mode((self.window_width,self.window_height))
        self.backgorund_image_stage = pg.image.load(self.config["config"]["path_background_stage"])
        self.backgorund_image_stage = pg.transform.scale(self.backgorund_image_stage,(self.window_width,self.window_height))
        self.background_image_menu = pg.image.load(self.config["config"]["path_background_menu"])
        self.background_image_menu = pg.transform.scale(self.background_image_menu,(self.window_width,self.window_height))
        self.level_1 :str = "level_1"
        self.level_2 :str= "level_2"
        self.level_3 :str= "level_3"
        self.builder : BuilderStage = None
        self.map : list[pg.sprite.Group] = None
        self.blocks : list[Plataform]= None      
        self.player : Player = None
        self.fruits : list[Fruit]= None
        self.fruits_group = pg.sprite.Group()
        self.enemies : list[Enemy] = None
        self.enemies_group = pg.sprite.Group()
        self.trap_group : pg.sprite.Group = pg.sprite.Group()
        self.lifes_group : pg.sprite.Group = pg.sprite.Group()
        self.explosion_group = pg.sprite.Group()
        self.limit_time :int = self.config["config"]["limit_time"]
        self.fps = self.config["config"]["fps"]
        self.text_color = None
        self.clock = None
        self.delta_ms = None
        self.current_time = None
        self.clock_pg = pg.time.Clock()
        self.build_stage()
        self.init_player()
        self.load_lifes()
        self.load_clock()
        pg.display.set_caption("DBPY")


    def run_level(self):
        while True:
            self.current_time = pg.time.get_ticks()
            self.clock.run_clock(self.current_time)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.screen.blit(self.backgorund_image_stage,self.backgorund_image_stage.get_rect())
            self.screen.blit(self.clock.get_surface(),self.clock.get_position())
            self.draw_blocks()
            self.delta_ms = self.clock_pg.tick(self.fps)

            if self.player.finished_animation_death() or self.is_all_enemies_death():
                pg.quit()
                sys.exit()

            self.update_and_draw_explosions()
            self.collisions_bullet()
            self.collisions_trap()
            self.collisions_enemy()
            self.collisions_fruit()
            self.update_and_draw_lifes()
            self.update_and_draw_trap(self.delta_ms)
            self.update_and_draw_fruits(self.delta_ms)
            self.update_and_draw_enemies(self.delta_ms)
            self.update_and_draw_player(self.delta_ms)

            pg.display.update()
    
    def update_and_draw_player(self,delta):
        self.player.update(delta)
        self.player.draw(self.screen)

    def update_and_draw_enemies(self,delta):
        for enemy in self.enemies_group:
            enemy: Enemy
            enemy.update(delta)
            enemy.draw(self.screen)
        self.enemies = [enemy for enemy in self.enemies_group]

    def update_and_draw_fruits(self,delta):
        self.fruits = [fruit for fruit in self.fruits_group]
        self.fruits_group.update(delta)
        self.fruits_group.draw(self.screen)

    def update_and_draw_trap(self,delta):
        self.trap_group.update(delta)
        self.trap_group.draw(self.screen)        

    def update_and_draw_lifes(self):
        self.lifes_group.update()
        self.lifes_group.draw(self.screen)

    def collisions_fruit(self):
        for fruit in self.fruits:
            fruit : Fruit
            if self.player.rect.colliderect(fruit.rect):
                if self.player.get_lifes() < 3:
                    self.fruits_group.remove(fruit)
                    fruit.do_kill()
                    self.player.add_life()

    def collisions_enemy(self):
        for enemy in self.enemies_group:
            enemy : Enemy
            if self.player.rect.colliderect(enemy.rect) and (not self.player.is_defending or self.player.looking_right == enemy.is_looking_right):
                enemy.reboot_position()
                self.player.reboot_position()
                self.player.remove_life()

    def collisions_trap(self):
        for trap in self.trap_group:
            trap : Trap
            if self.player.rect.colliderect(trap.rect) and trap.do_damage:
                if self.player.is_defending:
                    self.player.remove_life()
                else:
                    self.player.remove_life()
                    self.player.remove_life()
                    self.player.reboot_position()
                if trap.is_looking_right:
                    self.explosion_group.add(Explosion(trap.rect.right-20,trap.rect.top - 20,200))
                else:
                    self.explosion_group.add(Explosion(trap.rect.left-20,trap.rect.top - 20,200))
                trap.do_damage = False

    def collisions_bullet(self):
        for bullet in self.player.get_bullets():        
            bullet:Bullet
            if pg.sprite.spritecollide(bullet, self.enemies_group, True):
                if bullet.direction:
                    self.explosion_group.add(Explosion(bullet.rect.right-20,bullet.rect.top - 20,200))
                else:
                    self.explosion_group.add(Explosion(bullet.rect.left-20,bullet.rect.top - 20,200))
                bullet.do_kill()

    def update_and_draw_explosions(self):
        for exp in self.explosion_group:
            exp : Explosion
            exp.update(self.delta_ms)
            exp.draw(self.screen)

    def is_all_enemies_death(self) -> bool:
        return len(self.enemies) == 0

    def draw_blocks(self):
        for block in self.blocks:
            block.draw(self.screen)

    def build_stage(self,stage = "level_2" ):
        self.builder : BuilderStage = BuilderStage(stage)
        
        self.map = self.builder.Build_Map()
        self.enemies : list[Enemy] = self.builder.Build_enemies()
        self.trap_group = self.builder.build_trap()
        self.blocks : list[Plataform]= self.map["blocks"]        
        self.fruits : list[Fruit] = self.map["fruits"]
        self.load_fruits(self.fruits)
        self.load_enemies(self.enemies)

    def init_player(self):
        self.player = Player(coord_x=self.config["config"]["player"]["init_pos_x"],coord_y=self.config["config"]["player"]["init_pos_y"],frame_rate=self.config["config"]["player"]["frame_rate"], speed_walk=self.config["config"]["player"]["speed_walk"], speed_run=self.config["config"]["player"]["speed_run"], gravity=self.config["config"]["player"]["gravity"] ,list_of_plataforms=self.blocks)

    def load_enemies(self, enemies: list[Enemy]):
        for enemy in enemies:
            self.enemies_group.add(enemy)

    def load_fruits(self, fruits : list[Fruit]):    
        for fruit in fruits:
            self.fruits_group.add(fruit)
    
    def load_lifes(self):
        self.lifes_group = self.player.get_lifes_group()

    def load_limit_time(self):
        self.limit_time = self.config["config"]["limit_time"]

    def load_clock(self):
        normal_color = self.config["config"]["text_color_normal"]
        alert_color = self.config["config"]["text_color_alert"]
        white = (normal_color[0],normal_color[2],normal_color[2])
        red = (alert_color[0],alert_color[1],alert_color[2])
        font_size = self.config["config"]["font_size"]
        font_path = self.config["config"]["font_path"]
        self.clock = Clock(self.limit_time,white,red,font_size,font_path,self.window_width)
    