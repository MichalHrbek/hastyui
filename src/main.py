from engine.entity import *
from engine.event import Event
import pygame as pg
from engine.ui import *


pg.init()
screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)
clock = pg.time.Clock()
running = True

root = Entity([
        HBox([
            Label(text="Hello"),
            Padding(100,100),
            Label(text="World!"),
        ]),
    ])

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        e = Event(event)
        root._event(e)

    screen.fill("purple")
    
    root._render(screen)

    pg.display.flip()

    clock.tick(60)

pg.quit()