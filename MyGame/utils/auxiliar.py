import pygame as pg
import json

class Auxiliar:
    @staticmethod
    def getSurfaceFromSpriteSheet(path,columnas,filas,aumentar = 1,flip=False, step = 1) -> list[pg.surface.Surface]:
        lista = []
        surface_imagen = pg.image.load(path)
        if aumentar != 1:
            surface_imagen =  pg.transform.scale(surface_imagen,(surface_imagen.get_width() * aumentar,surface_imagen.get_height() * aumentar))
        fotograma_ancho = int(surface_imagen.get_width()/columnas)
        fotograma_alto = int(surface_imagen.get_height()/filas)
        x = 0
        for columna in range(0,columnas,step):
            for fila in range(filas):
                x = columna * fotograma_ancho
                y = fila * fotograma_alto
                surface_fotograma = surface_imagen.subsurface(x,y,fotograma_ancho,fotograma_alto)
                if(flip):
                    surface_fotograma = pg.transform.flip(surface_fotograma,True,False)
                lista.append(surface_fotograma)
        return lista

    @staticmethod
    def readJson(path):
        with open(path, 'r') as archivo:
            contenido = json.load(archivo)
        return contenido