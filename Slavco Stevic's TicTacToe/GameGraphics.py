import pygame as p
from GameLogic import *
from human import playVShuman
from dumbPC import playVSdpc
from smartPC import playVSspc
from drawANDtype import drawXO
        
# Window size is 600x600 so we divide coordinates by 200 to get the positions on the board array
def getSpot(ttt): 
    ttt.spot[0] = ttt.mouse[1] // 200
    ttt.spot[1] = ttt.mouse[0] // 200
         
# Graphics logic
def playGraphics(ttt, scr):
    if ttt.graphics == True:
        p.init()
        bg = (0, 0, 0) # background
        lines = (0, 255, 255)
        
        clock = p.time.Clock()
        
        while ttt.playing:
            clock.tick(120)
            # I am using a buffer instead of screen because it is easier to keep all the drawings on the screen while playing
            # How it works is whatever we draw on the buffer will be applied each frame onto the screen
            # This way we don't have to draw one by one thing but we can draw everything at once onto buffer and then apply it onto the screen
            scr.buffer.fill(bg) 
            scr.screen.blit(scr.buffer, (0, 0))
            
            p.draw.line(scr.buffer, lines, (200,0), (200, 600), 3)
            p.draw.line(scr.buffer, lines, (405,0), (405, 600), 3)
            p.draw.line(scr.buffer, lines, (0,200), (600, 200), 3)
            p.draw.line(scr.buffer, lines, (0,405), (600, 405), 3)
            
            p.display.flip()
            
            # Logic that checks what type of game are we playing
            # It also checks when the left mouse click is pressed and where
            if ttt.human == True and ttt.end == False:
                for event in p.event.get():
                    if event.type == p.QUIT:
                        ttt.playing = False
                        
                    elif event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                        ttt.mouse[0], ttt.mouse[1] = p.mouse.get_pos()
                        getSpot(ttt)
                        playVShuman(ttt)
                        
                    elif event.type == p.MOUSEBUTTONDOWN and event.button == 3:
                        if ttt.end == True:
                            newGame(ttt)
                    
                drawXO(ttt, scr)
                scr.screen.blit(scr.buffer, (0, 0))            
                p.display.flip()
                
            elif ttt.dpc == True and ttt.end == False:
                if ttt.x == True:
                    playVSdpc(ttt)
                    
                for event in p.event.get():
                    if event.type == p.QUIT:
                        ttt.playing = False
                        
                    elif event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                        ttt.mouse[0], ttt.mouse[1] = p.mouse.get_pos()
                        getSpot(ttt)
                        playVSdpc(ttt)
                        
                    elif event.type == p.MOUSEBUTTONDOWN and event.button == 3:
                        if ttt.end == True:
                            newGame(ttt)
                    
                drawXO(ttt, scr)
                scr.screen.blit(scr.buffer, (0, 0))            
                p.display.flip()
            
            elif ttt.spc == True and ttt.end == False:
                if ttt.x == True:
                    playVSspc(ttt)
                    
                for event in p.event.get():
                    if event.type == p.QUIT:
                        ttt.playing = False
                        
                    elif event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                        ttt.mouse[0], ttt.mouse[1] = p.mouse.get_pos()
                        getSpot(ttt)
                        playVSspc(ttt)
                        
                    elif event.type == p.MOUSEBUTTONDOWN and event.button == 3:
                        if ttt.end == True:
                            newGame(ttt)
                    
                drawXO(ttt, scr)
                scr.screen.blit(scr.buffer, (0, 0))            
                p.display.flip()
                
            elif ttt.end == True:
                for event in p.event.get():
                    if event.type == p.QUIT:
                        ttt.playing = False
                        
                    elif event.type == p.MOUSEBUTTONDOWN and event.button == 3:
                        if ttt.end == True:
                            newGame(ttt)
                
                drawXO(ttt, scr)
                scr.screen.blit(scr.buffer, (0, 0))            
                p.display.flip()  
        
        p.quit()
        