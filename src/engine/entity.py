from engine.event import Event
from engine.transform import Transform
from typing import Callable
import pygame as pg

class Entity:
    def __init__(self, children: list['Entity'] | None = None):
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

DynPos = Callable[[],tuple[float,float] | tuple[int,int] | pg.Vector2] | None
class Anchor:
    def __init__(self, size: DynPos = None, topleft: DynPos = None, topright: DynPos = None, bottomleft: DynPos = None, bottomright: DynPos = None, center: DynPos = None):
        self.size = size
        self.topleft = topleft
        self.topright = topright
        self.bottomleft = bottomleft
        self.bottomright = bottomright
        self.center = center
    
    def apply(self, transform: Transform):
        if self.size:
            transform.rect.size = self.size()
        if self.topleft:
            transform.rect.topleft = self.topleft()
        if self.topright:
            transform.rect.topright = self.topright()
        if self.bottomleft:
            transform.rect.bottomleft = self.bottomleft()
        if self.bottomright:
            transform.rect.bottomright = self.bottomright()
        if self.center:
            transform.rect.center = self.center()

class TransformedEntity(Entity):
    def __init__(self, children = None, transform: Transform | None = None, anchor: Anchor | None = None):
        super().__init__(children)
        self._transform = transform if transform is not None else Transform()
        self.anchor = anchor
    
    @property
    def transform(self):
        return self._transform
    
    @transform.setter
    def transform(self, value):
        self._transform = value

    def _event(self, e):
        super()._event(e)
    
    def _render(self, screen):
        if self.anchor:
            self.anchor.apply(self.transform)
        return super()._render(screen)
    
    # def _render(self, screen):
    #     super()._render(screen)
    #     pg.draw.rect(screen, "green", self.transform.rect, 1)