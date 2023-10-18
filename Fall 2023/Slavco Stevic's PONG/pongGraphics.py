import pygame as p

def makePongTable(screen, width, height, border):
    myRect = p.Rect(border, border, width-2*border, height-2*border)
    p.draw.rect(screen, (0, 0, 0), myRect, width= 3)