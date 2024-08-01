import pygame as pg

class Score:
    def __init__(self,font_size,font_path,text_color,window_width,datetime="",score=0):
        self.datetime = datetime
        self.score : int = score
        self.font_size = font_size
        self.font_path= font_path
        self.font = pg.font.Font(self.font_path,self.font_size)
        self.text_color = text_color
        self.window_width =window_width

    def run_score(self):
        self.number_surface = self.font.render(f"Puntos: {self.score}", True, self.text_color)
        self.position = self.number_surface.get_rect(center = (500,12))

    def get_surface(self) -> pg.surface.Surface:
        return self.number_surface

    def get_position(self) -> pg.rect.Rect:
        return self.position  
    
    #Getters and setters
    @property
    def Datetime(self):
        return self.datetime
    @Datetime.setter
    def Datetime(self,dt):
        self.datetime = dt

    @property
    def Score(self):
        return self.score
    @Score.setter
    def Score(self, score):
       self.score = score