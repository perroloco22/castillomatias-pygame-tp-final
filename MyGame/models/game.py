import pygame as pg
import sys
from constants import *
from models.builderStage import BuilderStage
from models.player import Player
from models.enemy import Enemy
from models.plataform import Plataform
from models.trap import Trap 
from models.fruits import Fruit
from models.bullet import Bullet
from models.explosion import Explosion
from models.clock import Clock
from utils.auxiliar import Auxiliar
from models.dbConnection import DbConnection
from models.score import Score
from datetime import datetime




class Game:
    def __init__(self):
        self.config = Auxiliar.readJson()
        self.window_width = self.config["config"]["ancho"]
        self.window_height = self.config["config"]["alto"]
        self.screen = pg.display.set_mode((self.window_width,self.window_height))
        self.background_image_stage = pg.image.load(self.config["config"]["path_background_stage"])
        self.background_image_stage = pg.transform.scale(self.background_image_stage,(self.window_width,self.window_height))
        self.background_image_menu = pg.image.load(self.config["config"]["path_background_menu"])
        self.background_image_menu = pg.transform.scale(self.background_image_menu,(self.window_width,self.window_height))
        self.background_image_table = pg.image.load(self.config["config"]["path_background_table"])
        self.level_1 :str = "level_1"
        self.level_2 :str = "level_2"
        self.level_3 :str = "level_3"
        self.current_level = None
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
        self.font_path_menu = self.config["config"]["font_path_menu"]
        self.font_title = pg.font.Font(self.font_path_menu,self.config["config"]["font_title_size"])
        self.font_menu_options = pg.font.Font(self.font_path_menu,self.config["config"]["font_menu_options_size"])
        self.font_score = pg.font.Font(self.font_path_menu,self.config["config"]["font_score_size"])
        self.yellow = (self.config["config"]["text_color_title"][0],self.config["config"]["text_color_title"][1],self.config["config"]["text_color_title"][2])
        self.red = (self.config["config"]["text_color_alert"][0],self.config["config"]["text_color_alert"][1],self.config["config"]["text_color_alert"][2])
        self.title_surface = self.font_title.render("DRAGON BALL PY",True,(self.yellow))
        self.title_rect = self.title_surface.get_rect(center=(self.window_width//2,self.window_height//4))
        self.text_color = None
        self.clock : Clock = None
        self.delta_ms = None
        self.current_time = None
        self.start_time = None
        self.clock_pg = pg.time.Clock()
        self.win = True
        self.running_level = True 
        self.flag_menu = True
        self.flag_level = True
        self.menu_options = self.config["config"]["menu_options"]
        self.selected_option = 0
        self.lose_life = False
        self.connection : DbConnection = DbConnection()
        self.score : Score = None
        self.lista_puntajes = self.connection.Get_top_five_scores()
        self.load_score()
        pg.display.set_caption("DBPY")
        self.connection.CreateTable()

    def run_game(self):
        while True:
            if self.flag_menu:
                self.score.Score = 0
                self.score.Datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.run_main()
            else:
                # print(f'1-CURRENT LEVEL = {self.current_level}')
                result = self.run_level()
                if result :
                    if self.current_level == self.level_1:
                        # print(f'3-CURRENT LEVEL = {self.current_level}')
                        self.load_level(self.level_2)
                        # print(f'4-CURRENT LEVEL = {self.current_level}')
                    elif self.current_level == self.level_2:
                        # print(f'5-CURRENT LEVEL = {self.current_level}')
                        self.load_level(self.level_3)
                        # print(f'6-CURRENT LEVEL = {self.current_level}')
                    else:
                        print("7-GANO EL JUEGO COMPLETO")
                        print(f'SCORE: {self.score.Score}')
                        if not self.lose_life:
                            self.score.Score += 3000
                        self.loading_score()
                        self.flag_menu = True
                        pg.time.delay(3000)
                elif not result or self.current_level == self.level_3:
                    self.loading_score()
                    print("PERDIO")
                    print(f'SCORE: {self.score.Score}')
                    self.current_level = self.level_1
                    self.enemies = []
                    self.clean_groups()
                    self.flag_menu = True
                    pg.time.delay(3000)

    def run_main(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.KEYDOWN:
                    self.flag_menu = False
                    if event.key == pg.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pg.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key == pg.K_RETURN:
                        if self.selected_option == 0:
                            self.load_level()
                            return  
                        elif self.selected_option == 1:
                            # self.flag_menu = True
                            print("HACER ESTADISITICAS")
                            self.run_statistics()
                        elif self.selected_option == 2:
                            pg.quit()
                            quit()
                    elif event.key == pg.K_1:
                        self.flag_menu = False
                        self.load_level()
                        return
                    elif event.key == pg.K_2:
                        self.flag_menu = False
                        self.load_level(level=self.level_2)
                        return
                    elif event.key == pg.K_3:
                        self.flag_menu = False
                        self.load_level(level=self.level_3)
                        return

            self.screen.blit(self.background_image_menu, self.background_image_menu.get_rect())
            self.screen.blit(self.title_surface,self.title_rect)            
            self.draw_options_menu()
            pg.display.update()

    def run_statistics(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return
            
            # print(self.lista_puntajes[0][0])
            # date_surface = self.font_score.render(f'{self.lista_puntajes[0][0]}',True,(0,0,0),(120,120,120))
            self.screen.blit(self.background_image_menu, self.background_image_menu.get_rect())
            self.screen.blit(self.background_image_table, self.background_image_table.get_rect(center=(self.window_width//2,300)))
            self.draw_score()
            # self.screen.blit(date_surface,date_surface.get_rect(center=(500,300)))
            pg.display.update()

    def draw_score(self):
        lista_puntajes = self.connection.Get_top_five_scores()
        y = 200
        for registro in lista_puntajes:
            print(f'{registro[0]}   -   {registro[1]}')
            date_surface = self.font_menu_options.render(registro[0],True,(0,0,0),(120,120,120))
            score_surface = self.font_menu_options.render(str(registro[1]),True,(0,0,0),(120,120,120))
            self.screen.blit(date_surface,date_surface.get_rect(center=(300,y)))
            self.screen.blit(score_surface,score_surface.get_rect(center=(400,y)))
            y+=20
        
    def loading_score(self):
        print("CARGANDO DATOS")
        self.connection.Add_Register(self.score.Datetime,self.score.Score)

    def draw_options_menu(self):
        for i, option in enumerate(self.menu_options):
            color = self.red if i == self.selected_option else self.yellow
            text_surface = self.font_menu_options.render(option, True, color)
            text_rect = text_surface.get_rect(center=((self.window_width / 2)-40, self.window_height // 2 + i * 50))
            self.screen.blit(text_surface, text_rect) 

    def run_level(self):
        print(f'2-RUN LEVEL: {self.current_level}')
        self.start_time = pg.time.get_ticks() + 1000
        while self.running_level:
            self.current_time = pg.time.get_ticks() - self.start_time            
            self.clock.run_clock(self.current_time)
            self.score.run_score()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.blit(self.background_image_stage,self.background_image_stage.get_rect())
            self.screen.blit(self.clock.get_surface(),self.clock.get_position())
            self.screen.blit(self.score.get_surface(),self.score.get_position())
            self.draw_blocks()
            self.delta_ms = self.clock_pg.tick(self.fps)

            if self.player.finished_animation_death() or self.clock.get_lapse_time() == 0:
                self.win = False
                self.running_level = False

            if self.is_all_enemies_death():
                self.running_level = False
                self.win = True

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

        self.running_level = True
        self.fruits_group.empty()
        self.explosion_group.empty() 
        self.trap_group.empty()
        self.enemies_group.empty()
        self.enemies = []
        return self.result_level()
    
    def clean_groups(self):
        self.fruits_group.empty()
        self.explosion_group.empty()
        self.trap_group.empty()
        self.enemies_group.empty()

    def result_level(self) -> bool:
        return self.win

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
                    self.score.score += 50
                    self.fruits_group.remove(fruit)
                    fruit.do_kill()
                    self.player.add_life()

    def collisions_enemy(self):
        for enemy in self.enemies_group:
            enemy : Enemy
            if self.player.rect.colliderect(enemy.rect) and (not self.player.is_defending or self.player.looking_right == enemy.is_looking_right):
                self.lose_life = True
                self.score.score -= 35
                enemy.reboot_position()
                self.player.reboot_position()
                self.player.remove_life()

    def collisions_trap(self):
        for trap in self.trap_group:
            trap : Trap
            if self.player.rect.colliderect(trap.rect) and trap.do_damage:
                self.lose_life = True
                if self.player.is_defending:
                    self.player.remove_life()
                    self.score.score -= 5
                else:
                    self.score.score -= 20
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
                self.score.score += 100
                if bullet.direction:
                    self.explosion_group.add(Explosion(bullet.rect.right-20,bullet.rect.top - 20,200))
                else:
                    self.explosion_group.add(Explosion(bullet.rect.left-20,bullet.rect.top - 20,200))
                bullet.do_kill()
            # else:
            #     self.score.score -= 5

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

    def build_stage(self,stage ):
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
        font_path = self.config["config"]["font_path_time"]
        self.clock = Clock(self.limit_time,white,red,font_size,font_path,self.window_width)

    def load_score(self):
        font_size = self.config["config"]["font_size"]
        font_path = self.config["config"]["font_path_time"]
        normal_color = self.config["config"]["text_color_normal"]
        self.score = Score(font_size=font_size,font_path=font_path,text_color=normal_color,window_width=self.window_width)

    def load_level(self, level = "level_1"):
        self.current_level = level
        self.build_stage(level)
        self.init_player()
        self.load_lifes()
        self.load_clock()