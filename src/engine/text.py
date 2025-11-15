import pygame as pg


class StyledText:
    def __init__(self, text: str, bold: bool = False, italic: bool = False, underline: bool = False, strikethrough: bool = False, color = None):
        self.text = text
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.strikethrough = strikethrough
        self.color = color

class RichText:
    def __init__(self, parts: list[str | StyledText]):
        self.parts = parts

TextLike = str | StyledText | RichText

def draw_text(text: TextLike, font: pg.font.Font, color, antialias = True) -> pg.Surface:
    if isinstance(text, str):
        rt = RichText([StyledText(text)])
    elif isinstance(text, StyledText):
        rt = RichText([text])
    elif isinstance(text, RichText):
        rt = text
    else:
        raise ValueError("Invalid text type")
    
    parts = rt.parts.copy()
    mw = 0
    mh = 0
    y = 0
    x = 0
    textfeed = ""
    mlh = 0
    font.bold, font.italic, font.underline, font.strikethrough = False, False, False, False
    while len(parts) or textfeed:
        if not textfeed:
            p = parts.pop(0)
            if isinstance(p, StyledText):
                font.bold, font.italic, font.underline, font.strikethrough = p.bold, p.italic, p.underline, p.strikethrough
                textfeed = p.text
            else:
                font.bold, font.italic, font.underline, font.strikethrough = False, False, False, False
                textfeed = p
        
        newline = False
        if "\n" in textfeed:
            t, textfeed = textfeed.split("\n", 1)
            newline = True
        else:
            t, textfeed = textfeed, ""
        
        s = font.size(t)
        mlh = max(mlh, s[1])
        x += s[0]
        mw = max(mw, x)
        mh = max(mh, y+mlh)

        if newline:
            x = 0
            y += mlh
            mlh = 0
    
    surface = pg.Surface((mw, mh), pg.SRCALPHA)
    parts = rt.parts.copy()
    y = 0
    x = 0
    textfeed = ""
    mlh = 0
    font.bold, font.italic, font.underline, font.strikethrough = False, False, False, False
    cc = color
    while len(parts) or textfeed:
        if not textfeed:
            p = parts.pop(0)
            if isinstance(p, StyledText):
                font.bold, font.italic, font.underline, font.strikethrough = p.bold, p.italic, p.underline, p.strikethrough
                cc = p.color if p.color else color
                textfeed = p.text
            else:
                font.bold, font.italic, font.underline, font.strikethrough = False, False, False, False
                cc = color
                textfeed = p
        
        newline = False
        if "\n" in textfeed:
            t, textfeed = textfeed.split("\n", 1)
            newline = True
        else:
            t, textfeed = textfeed, ""
        
        s = font.size(t)
        surface.blit(font.render(t, antialias, cc), (x,y))
        mlh = max(mlh, s[1])
        x += s[0]

        if newline:
            x = 0
            y += mlh
            mlh = 0
    
    return surface