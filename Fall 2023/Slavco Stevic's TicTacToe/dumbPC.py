from GameLogic import *
from human import human
import numpy as np
from drawANDtype import typeXO

# Dumb computer logic
def dumbPC(ttt):
    validating = True
    while validating:
        # Picking random spot on the board
        ttt.spot[0] = np.random.randint(0, 3)
        ttt.spot[1] = np.random.randint(0, 3)
        
        if isValid(ttt):
            typeXO(ttt)
            ttt.turns += 1
            #showBoard(ttt)
            checkWin(ttt)
            validating = False
              
def playVSdpc(ttt):
    if ttt.graphics == True:
        if ttt.x == True:
            print("X has played")
            dumbPC(ttt)
            
        elif ttt.o == True:
            char = 'o'
            human(ttt, char)
        return
    
    else:
        while (ttt.playing):
            if ttt.x == True:
                print("X has played")
                dumbPC(ttt)
                
            elif ttt.o == True:
                char = 'o'
                human(ttt, char)