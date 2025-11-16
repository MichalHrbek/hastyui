from engine.entity import TransformedEntity, Entity
from engine.transform import Transform
from typing import Callable
import pygame as pg
from engine.text import draw_text, TextLike

class Label(TransformedEntity):
    def __init__(self, children = None, transform = None, anchor = None, font: pg.font.Font | None = None, auto_rezise = True, text: TextLike = "", color = "cornsilk"):
        super().__init__(children, transform, anchor)
        self.surface = pg.Surface(self.transform.rect.size, pg.SRCALPHA)
        self.auto_rezise = auto_rezise
        if font:
            self.font = font
        else:
            self.font = pg.font.SysFont('monospace', 32)
            self.color = color
        self.text = text
    
    @property
    def text(self) -> TextLike:
        return self._text
    
    @text.setter
    def text(self, value: TextLike):
        self._text = value
        self.redraw()

    def redraw(self):
        if self.auto_rezise:
            self.surface = draw_text(self.text, self.font, self.color)
            self.transform.rect.size = self.surface.get_size()
        else:
            self.surface.fill((0,0,0,0))
            self.surface.blit(draw_text(self.text, self.font, self.color))
    
    def _render(self, screen):
        super()._render(screen)
        screen.blit(self.surface, self.transform.rect)

class Box(TransformedEntity):
    def resize(self):
        minx = 2**30
        miny = 2**30
        maxx = -2**30
        maxy = -2**30
        for i in self.children:
            if not isinstance(i, TransformedEntity):
                continue
            minx = min(minx, i.transform.rect.topleft[0])
            miny = min(miny, i.transform.rect.topleft[1])
            maxx = max(maxx, i.transform.rect.bottomright[0])
            maxy = max(maxy, i.transform.rect.bottomright[1])
        if minx > maxx or miny > maxy:
            self.transform.rect = pg.Rect(0,0,0,0)
        for i in self.children:
            if not isinstance(i, TransformedEntity):
                continue
            i.transform.rect.move_ip(self.transform.rect.topleft[0]-minx, self.transform.rect.topleft[1]-miny)
        self.transform.rect = pg.Rect(self.transform.rect.topleft, (maxx-minx, maxy-miny))

class PadBox(Box):
    def __init__(self, children = None, transform = None, anchor = None, padding: float | tuple[float,float,float,float] = 0):
        super().__init__(children, transform, anchor)
        self.padding = padding
    
    def resize(self):
        if isinstance(self.padding, tuple):
            p_left, p_top, p_right, p_bottom = self.padding
        else:
            p_left, p_top, p_right, p_bottom = (self.padding,)*4
            
        minx = 2**30
        miny = 2**30
        maxx = -2**30
        maxy = -2**30
        for i in self.children:
            if not isinstance(i, TransformedEntity):
                continue
            minx = min(minx, i.transform.rect.topleft[0])
            miny = min(miny, i.transform.rect.topleft[1])
            maxx = max(maxx, i.transform.rect.bottomright[0])
            maxy = max(maxy, i.transform.rect.bottomright[1])
        if minx > maxx or miny > maxy:
            self.transform.rect = pg.Rect(0,0,p_left+p_right,p_top+p_bottom)
        for i in self.children:
            if not isinstance(i, TransformedEntity):
                continue
            i.transform.rect.move_ip(self.transform.rect.topleft[0]-minx+p_left, self.transform.rect.topleft[1]-miny+p_top)
        self.transform.rect = pg.Rect(self.transform.rect.topleft, (maxx-minx+p_left+p_right, maxy-miny+p_top+p_bottom))
    
    def pad_rect(rect: pg.Rect, padding: tuple[float,float,float,float]) -> pg.Rect:
        p_left, p_top, p_right, p_bottom = padding
        new_x = rect.x - p_left
        new_y = rect.y - p_top
        new_width = rect.width + p_left + p_right
        new_height = rect.height + p_top + p_bottom
        return pg.Rect(new_x, new_y, new_width, new_height)
    
    def _render(self, screen):
        self.resize()
        super()._render(screen)

class StyledBox(Box):
    def __init__(self, children = None, transform = None, anchor = None, bg_color = "transparent", border_size = 0, border_color = "transparent", border_radius: int = 0):
        super().__init__(children, transform, anchor)
        self.bg_color = bg_color
        self.border_size = border_size
        self.border_color = border_color
        self.border_radius = border_radius
    
    def _render(self, screen):
        self.resize()
        pg.draw.rect(screen, self.bg_color, self.transform.rect, 0, self.border_radius)
        if self.border_size:
            pg.draw.rect(screen, self.bg_color, self.transform.rect, self.border_size, self.border_radius)
        return super()._render(screen)

class VBox(TransformedEntity):
    def _render(self, screen):
        anchor = self.transform.rect.topleft
        for i in self.children:
            if not isinstance(i, TransformedEntity):
                continue
            i.transform.rect.topleft = anchor
            anchor = i.transform.rect.topright
        super()._render(screen)

class HBox(TransformedEntity):
    def _render(self, screen):
        anchor = self.transform.rect.topleft
        for i in self.children:
            if not isinstance(i, TransformedEntity):
                continue
            i.transform.rect.topleft = anchor
            anchor = i.transform.rect.bottomleft
        super()._render(screen)

class Padding(TransformedEntity):
    def __init__(self, width: float, height: float):
        super().__init__(None, Transform(pg.Rect(0,0,width,height)))

class Button(TransformedEntity):
    def __init__(self, children = None, transform = None, anchor = None, border_size = 1):
        super().__init__(children, transform, anchor)