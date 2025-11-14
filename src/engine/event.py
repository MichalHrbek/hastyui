import pygame.event

class Event:
    def __init__(self, e: pygame.event.Event, consumed: bool = False):
        self.e = e
        self.consumed = consumed
    
    def consume(self):
        self.consumed = True