from engine.entity import *
from engine.event import Event
import pygame as pg
from engine.ui import *
from engine.text import *


pg.init()
screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)
clock = pg.time.Clock()
running = True

rich_text = RichText([
    "Multi\n",
    StyledText("line\n", italic=True),
    StyledText("and\n", underline=True),
    StyledText("styled\n", bold=True, color="red"),
    "text?",
])

root = Entity([
        HBox([
            Label(text="Hello"),
            Padding(100,100),
            Label(text="Padding!"),
        ]),
        Anchor([Label(text="TR")], topright=lambda: screen.get_rect().topright),
        Anchor([Label(text="BL")], bottomleft=lambda: screen.get_rect().bottomleft),
        Anchor([Label(text="BR")], bottomright=lambda: screen.get_rect().bottomright),
        Anchor([Label(text=rich_text)], center=lambda: screen.get_rect().center),
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