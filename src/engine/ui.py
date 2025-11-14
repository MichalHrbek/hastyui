from engine.entity import TransformedEntity
from engine.transform import Transform
import pygame as pg

class Label(TransformedEntity):
    def __init__(self, children = None, transform = None, font: pg.font.Font | None = None, auto_rezise = True, text: str = "", color = "cornsilk"):
        super().__init__(children, transform)
        self.surface = pg.Surface(self.transform.rect.size, pg.SRCALPHA)
        self.auto_rezise = auto_rezise
        if font:
            self.font = font
        else:
            self.font = pg.font.SysFont('monospace', 32)
            self.color = color
        self.text = text
    
    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, value: str):
        self._text = value
        self.redraw()

    def redraw(self):
        lines = self.text.split('\n')
        if self.auto_rezise:
            mh = self.font.get_linesize()*len(lines)+1 # (1 if self.font.underline else 0)
            mw = 0
            for i in lines:
                mw = max(mw, self.font.size(i)[0])
            
            if mh > self.surface.get_height() or mw > self.surface.get_width():
                self.surface = pg.Surface((mw,mh), pg.SRCALPHA)
            
            self.transform.rect.size = (mw,mh)
        
        self.surface.fill((0,0,0,0))
        for i, line in enumerate(self._text.split('\n')):
            self.surface.blit(self.font.render(line, 1, self.color), (0,self.font.get_linesize()*i))
    
    def _render(self, screen):
        super()._render(screen)
        screen.blit(self.surface, self.transform.rect)
    
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