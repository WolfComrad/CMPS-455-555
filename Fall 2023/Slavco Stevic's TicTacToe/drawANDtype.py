import pygame as p

# Typing x/o into the board array
def typeXO(ttt):
    if ttt.x == True:
        ttt.board[ttt.spot[0]][ttt.spot[1]] = 'x'
        ttt.x = False
        ttt.o = True

    elif ttt.o == True:
        ttt.board[ttt.spot[0]][ttt.spot[1]] = 'o'
        ttt.x = True
        ttt.o = False

# Getting the center of the quadrant our mouse was clicked in
# We need these ccenters for the drawings of X and O
def getCenter(i, j):
    if i == 0 and j == 0:
        return 100, 100
    elif i == 0 and j == 1:
        return 300, 100
    elif i == 0 and j == 2:
        return 500, 100
        
    elif i == 1 and j == 0:
        return 100, 300
    elif i == 1 and j == 1:
        return 300, 300
    elif i == 1 and j == 2:
        return 500, 300
        
    elif i == 2 and j == 0:
        return 100, 500
    elif i == 2 and j == 1:
        return 300, 500
    elif i == 2 and j == 2:
        return 500, 500

# Drawing X and O      
def drawXO(ttt, scr):
    for i in range(3):
        for j in range(3):
            cx, cy = getCenter(i,j)
            # Winning X line
            if ttt.winX == True:
                p.draw.line(scr.buffer, ttt.playerX, (ttt.c1[0], ttt.c1[1]), (ttt.c2[0], ttt.c2[1]), 10)
            
            # Winning O line
            if ttt.winO == True:
                p.draw.line(scr.buffer, ttt.playerO, (ttt.c1[0], ttt.c1[1]), (ttt.c2[0], ttt.c2[1]), 10)
            
            #Drawing X inside the quadrant   
            if ttt.board[i][j] == 'x':
                p.draw.line(scr.buffer, ttt.playerX, (cx - 80, cy - 80), (cx + 80, cy + 80), 5)
                p.draw.line(scr.buffer, ttt.playerX, (cx + 80, cy - 80), (cx - 80, cy + 80), 5)
            
            #Drawing O inside the quadrant    
            elif ttt.board[i][j] == 'o':
                p.draw.circle(scr.buffer, ttt.playerO, (cx, cy), 90, 5)

        