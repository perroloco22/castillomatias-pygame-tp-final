import pygame as pg

class Clock:
    def __init__(self, limit_time, text_color_normal,text_color_alert,font_size,font_path,window_width):
      self.limit_time = limit_time
      self.text_color_normal = text_color_normal
      self.text_color_current = text_color_normal
      self.text_color_alert = text_color_alert
      self.lapse_time = 0
      self.font_size = font_size
      self.font_path= font_path
      self.font = pg.font.Font(self.font_path,self.font_size)
      self.number_surface = None
      self.position = None
      self.window_width = window_width

    def run_clock(self,curren_time):
        self.lapse_time = (self.limit_time - curren_time )//1000
        if self.lapse_time <= 10:
            self.text_color_current = self.text_color_alert 
        self.number_surface = self.font.render(f"Tiempo: {self.lapse_time}s", True, self.text_color_current)
        self.position = self.number_surface.get_rect(center = (300,12))

    def get_surface(self) -> pg.surface.Surface:
        return self.number_surface

    def get_position(self) -> pg.rect.Rect:
        return self.position  
    
    def get_lapse_time(self)->bool:
        return self.lapse_time