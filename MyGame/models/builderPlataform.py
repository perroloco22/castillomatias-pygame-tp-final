import pygame as pg
from constants import *
from models.plataform import Plataform
from utils.auxiliar import Auxiliar



class BuilderPlataform():
    def __init__(self, map: list[list[int]] = None):
        self.__map = Auxiliar.readJson()['stages']['level_1']['map']
        self.__coordinates = []



    def __Get_coordinates(self) -> list[dict]:
        count_row = 0
        count_column = 0
        for row in self.__map:
            for column in row:
                if column == 1:
                    dict_aux = {}
                    dict_aux['x'] = count_column * SIZE_BLOCK
                    dict_aux['y'] = count_row * SIZE_BLOCK
                    print(dict_aux['x'] == 280)
                    print(dict_aux['y'] == 240 )
                    self.__coordinates.append(dict_aux)
                count_column += 1 
            
            count_column = 0 
            count_row += 1
        

    def Build_plataform(self) -> list[Plataform]:
        if not self.__coordinates:
            self.__Get_coordinates()        
        blocks = []
        
        for coor in self.__coordinates:            
            block = Plataform(coord_x=coor['x'],coord_y=coor['y'])
            blocks.append(block)
        
        return blocks
        
        

       
       
    
