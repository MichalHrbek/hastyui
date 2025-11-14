import pygame as pg

class Transform:
    def __init__(self, rect: pg.Rect | None = None, scale: float = 1.0):
        self.rect = rect if rect is not None else pg.Rect(0,0,0,0)
        self.scale = scale
    
    @property
    def scaled_rect(self) -> pg.Rect:
        if self.scale == 1.0:
            return self.rect
        return pg.Rect(self.rect.topleft, self.rect.size*self.scale)
    
    @scaled_rect.setter
    def scaled_rect(self, value: pg.Rect):
        if self.scale == 1.0:
            self.rect = value
            return
        self.rect = pg.Rect(value.topleft, value/self.scale)
        
    
    def transform_point(self, global_pos: pg.math.Vector2) -> pg.math.Vector2:
        return (pg.math.Vector2(global_pos)-pg.math.Vector2(self.rect.topleft))*self.scale
    