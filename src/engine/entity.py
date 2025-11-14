from engine.event import Event
from engine.transform import Transform
from typing import Self
import pygame as pg

class Entity:
    def __init__(self, children: list[Self] | None = None):
        self.children = children if children is not None else []

    def _event(self, e: Event):
        for i in self.children:
            i._event(e)
            if e.consumed:
                return
    
    def _tick(self, delta: float):
        for i in self.children:
            i._tick(delta)

    def _render(self, screen: pg.Surface):
        for i in self.children:
            i._render(screen)

class TransformedEntity(Entity):
    def __init__(self, children = None, transform: Transform | None = None):
        super().__init__(children)
        self._transform = transform if transform is not None else Transform()
    
    @property
    def transform(self):
        return self._transform
    
    @transform.setter
    def transform(self, value):
        self._transform = value

    def _event(self, e):
        super()._event(e)
        if e.e.type in [pg.MOUSEMOTION, pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN]:
            e.e.tpos = self.transform.transform_point(e.e.pos)
            self._transformed_event(e)

    def _transformed_event(self, e: Event):
        pass