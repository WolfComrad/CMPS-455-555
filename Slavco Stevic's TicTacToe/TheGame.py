from GameLogic import *
import pygame as p
from human import playVShuman
from dumbPC import playVSdpc
from smartPC import playVSspc
from GameGraphics import playGraphics

# I made a class tictactoe so that I can seperate functions into files, that way it is easier to keep track of everything 
# and the class, once created, keeps all values for all attributes needed across other files
class tictactoe:
    def __init__(self, x = True, o = False, spot = [-1, -1], mouse = [-1, -1], c1 = [-1, -1], c2 = [-1, -1], turns = 0, 
                 board = [['#','#','#'],['#','#','#'],['#','#','#']], 
                 playing = True, human = False, dpc = False, spc = False, graphics = False,
                 playerX = (255, 0, 0), playerO = (255, 255, 255), winX = False, winO = False, end = False):
        self.x = x # x's turn
        self.o = o # o's turn
        self.spot = spot # spot on the board after converting the mouse coordinates
        self.mouse = mouse # mouse coordinates
        self.c1 = c1 # corner 1 of the winning line
        self.c2 = c2 # corner 2 of the winning line
        self.turns = turns # countring number of turns
        self.board = board
        self.playing = playing
        self.human = human # human option
        self.dpc = dpc # dumb computer option
        self.spc = spc # smart computer option
        self.graphics = graphics # graphics option
        self.playerX = playerX # x's color
        self.playerO = playerO # o's color
        self.winX = winX # did x win?
        self.winO = winO # did o win?
        self.end = end # end of the game - not of the application

class Screen:
    def __init__(self):
        self.windowSize = (600, 600)
        self.screen = p.display.set_mode(self.windowSize)
        self.buffer = p.Surface(self.windowSize)
    
ttt = tictactoe()

startTheGame(ttt)

scr = Screen()

if ttt.graphics == True:
    playGraphics(ttt, scr)
else:    
    if ttt.human == True:
        playVShuman(ttt)
        
    elif ttt.dpc == True:
        playVSdpc(ttt)
        
    elif ttt.spc == True:
        playVSspc(ttt)
    