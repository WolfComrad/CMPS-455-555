from GameLogic import *
from dumbPC import dumbPC
from human import human

# Winning logic for the smart computer
def tryWin(ttt):
    #rows
    for j in range(3):
        if (ttt.board[j][0] == 'x' and ttt.board[j][1] == 'x' and ttt.board[j][2] == '#'): # xx# rows
            ttt.board[j][2] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        
        elif (ttt.board[j][0] == '#' and ttt.board[j][1] == 'x' and ttt.board[j][2] == 'x'): # #xx rows
            ttt.board[j][0] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        
        elif (ttt.board[j][0] == 'x' and ttt.board[j][1] == '#' and ttt.board[j][2] == 'x'): # #xx rows
            ttt.board[j][1] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
    
    #cols
    for j in range(3):
        if (ttt.board[0][j] == 'x' and ttt.board[1][j] == 'x' and ttt.board[2][j] == '#'): # xx# cols
            ttt.board[2][j] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        
        elif (ttt.board[0][j] == '#' and ttt.board[1][j] == 'x' and ttt.board[2][j] == 'x'): # #xx cols
            ttt.board[0][j] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        
        elif (ttt.board[0][j] == 'x' and ttt.board[1][j] == '#' and ttt.board[2][j] == 'x'): # #xx cols
            ttt.board[1][j] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
    
    #cross
    if ttt.board[1][1] == 'x':
        if (ttt.board[0][0] == 'x' and ttt.board[2][2] == '#'): # xx# left-right cross
            ttt.board[2][2] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        elif (ttt.board[0][0] == '#' and ttt.board[2][2] == 'x'): # #xx left-right cross
            ttt.board[0][0] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        elif (ttt.board[0][2] == 'x' and ttt.board[2][0] == '#'): # xx# right-left cross
            ttt.board[2][0] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        elif (ttt.board[0][2] == '#' and ttt.board[2][0] == 'x'): # #xx right-left cross
            ttt.board[0][2] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
    
    elif ttt.board[1][1] == '#':
        if (ttt.board[0][0] == 'x' and ttt.board[2][2] == 'x'): # xx# left-right cross
            ttt.board[1][1] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        elif (ttt.board[0][0] == 'x' and ttt.board[2][2] == 'x'): # #xx left-right cross
            ttt.board[1][1] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        elif (ttt.board[0][2] == 'x' and ttt.board[2][0] == 'x'): # xx# right-left cross
            ttt.board[1][1] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        elif (ttt.board[0][2] == 'x' and ttt.board[2][0] == 'x'): # #xx right-left cross
            ttt.board[1][1] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True

# Blocking logic for the smart computer      
def tryBlock(ttt):
    for j in range(3):
        if (ttt.board[j][0] == 'o' and ttt.board[j][1] == 'o' and ttt.board[j][2] == '#'): # xx# rows
            ttt.board[j][2] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        
        elif (ttt.board[j][0] == '#' and ttt.board[j][1] == 'o' and ttt.board[j][2] == 'o'): # #xx rows
            ttt.board[j][0] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
    
        elif (ttt.board[j][0] == 'o' and ttt.board[j][1] == '#' and ttt.board[j][2] == 'o'): # #xx rows
            ttt.board[j][1] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
    
    #cols
    for j in range(3):
        if (ttt.board[0][j] == 'o' and ttt.board[1][j] == 'o' and ttt.board[2][j] == '#'): # xx# cols
            ttt.board[2][j] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        
        elif (ttt.board[0][j] == '#' and ttt.board[1][j] == 'o' and ttt.board[2][j] == 'o'): # #xx cols
            ttt.board[0][j] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        
        elif (ttt.board[0][j] == 'o' and ttt.board[1][j] == '#' and ttt.board[2][j] == 'o'): # #xx cols
            ttt.board[1][j] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
    
    #cross
    if ttt.board[1][1] == 'o':
        if (ttt.board[0][0] == 'o' and ttt.board[2][2] == '#'): # xx# left-right cross
            ttt.board[2][2] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        elif (ttt.board[0][0] == '#' and ttt.board[2][2] == 'o'): # #xx left-right cross
            ttt.board[0][0] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        elif (ttt.board[0][2] == 'o' and ttt.board[2][0] == '#'): # xx# right-left cross
            ttt.board[2][0] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        elif (ttt.board[0][2] == '#' and ttt.board[2][0] == 'o'): # #xx right-left cross
            ttt.board[0][2] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        
    elif ttt.board[1][1] == '#':
        if (ttt.board[0][0] == 'o' and ttt.board[2][2] == 'o'): # xx# left-right cross
            ttt.board[1][1] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        elif (ttt.board[0][0] == 'o' and ttt.board[2][2] == 'o'): # #xx left-right cross
            ttt.board[1][1] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        elif (ttt.board[0][2] == 'o' and ttt.board[2][0] == 'o'): # xx# right-left cross
            ttt.board[1][1] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True
        elif (ttt.board[0][2] == 'o' and ttt.board[2][0] == 'o'): # #xx right-left cross
            ttt.board[1][1] = 'x'
            ttt.x = False
            ttt.o = True
            ttt.turns += 1
            return True

# Function for the smart computer to decide whether to try to block or to try to win                   
def playVSspc(ttt):
    if ttt.graphics == True:
        if ttt.x == True:
            print("X has played")
            if ttt.turns < 4:
                dumbPC(ttt)
                
            else:
                win = tryWin(ttt)
                if win == True:
                    checkWin(ttt)
                else:
                    block = tryBlock(ttt)
                    if block == True:
                        checkWin(ttt)
                    else:
                        dumbPC(ttt)
            
        elif ttt.o == True:
            char = 'o'
            human(ttt, char)
        return
    
    else:
        while (ttt.playing):
            if ttt.x == True:
                print("X has played")
                if ttt.turns < 3:
                    dumbPC(ttt)
                    
                else:
                    block = tryBlock(ttt)
                    if block == True:
                        checkWin(ttt)
                    else:
                        win = tryWin(ttt)
                        if win == True:
                            checkWin(ttt)
                        else:
                            dumbPC(ttt)
                
            elif ttt.o == True:
                char = 'o'
                human(ttt, char)
