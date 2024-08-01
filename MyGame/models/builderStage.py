import pygame as pg
from constants import *
from models.plataform import Plataform
from utils.auxiliar import Auxiliar
from models.enemy import Enemy
from models.fruits import Fruit
from models.trap import Trap

class BuilderStage():
    def __init__(self, level:str, map: list[list[int]] = None):
        self.json = Auxiliar.readJson()
        self.level = level
        self.map = self.json['stages'][self.level]['map']
        self.enemies = self.json['stages'][self.level]['enemies']
        self.coordinates = []

    def __Get_coordinates(self) -> list[dict]:
        count_row = 0
        count_column = 0
        for row in self.map:
            for column in row:
                if column != 0:
                    dict_aux = {}
                    if column == 1:
                        dict_aux["type"] = "block"                    
                    elif column == 2:
                        dict_aux["type"] = "fruit"
                    dict_aux['x'] = count_column * SIZE_BLOCK
                    dict_aux['y'] = count_row * SIZE_BLOCK
                    self.coordinates.append(dict_aux)
                count_column += 1 
            count_column = 0 
            count_row += 1

    def Build_enemies(self) -> list[Enemy]:
        result = []
        speed_walk = self.enemies["speed_walk"]
        speed_run = self.enemies["speed_run"]
        frame_rate = self.enemies["frame_rate"]
        coordenates = self.enemies["coordenates"]
        for coordenate in coordenates:
            result.append(Enemy(coord_x=coordenate["x"],coord_y=coordenate["y"],speed_walk=speed_walk,speed_run=speed_run,frame_rate=frame_rate))
        return result
    
    def build_trap(self) -> pg.sprite.Group:
        trap_group = pg.sprite.Group()
        if self.level != "level_1":
            data_trap =  self.json["stages"][self.level]["trap"]
            speed = data_trap["speed"] 
            frame = data_trap["frame"] 
            move = data_trap["move_time"]
            coordenates = data_trap["coordenates"]
            for coordenate in coordenates:
                trap_group.add(Trap(pos_x=coordenate["x"],pos_y=coordenate["y"],move_time=move,frame_rate=frame,speed=speed))
        return trap_group


    def Build_Map(self) -> list[pg.sprite.Group]:
        if not self.coordinates:
            self.__Get_coordinates()
        result={}
        blocks = []
        fruits = []
        for coor in self.coordinates:
            if coor["type"] == "block":
                blocks.append(Plataform(coord_x=coor["x"],coord_y=coor["y"]))
            else:
                fruits.append(Fruit(coord_x=coor["x"],coord_y=coor["y"]))
        result["blocks"] = blocks
        result["fruits"] = fruits
        return result

           
        

       
       
    
