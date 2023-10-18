from GameLogic import *
from drawANDtype import *

# Function for human gameplay
def human(ttt, char):
    showBoard(ttt)
    print(f"It is {char}'s turn")
    
    if ttt.graphics == True:
        if isValid(ttt):
            typeXO(ttt)
            ttt.turns += 1
            showBoard(ttt)
            checkWin(ttt)
        else:
            print("Invalid input!!! Try again.")
            
    else:
        # We input coordinates on the board in console
        ttt.spot[0] = int(input())
        ttt.spot[1] = int(input())
        
        if isValid(ttt):
            typeXO(ttt)
            ttt.turns += 1
            #showBoard(ttt)
            checkWin(ttt)
            
        else:
            print("Invalid input!!! Try again.")

# Function for the human gameplay
def playVShuman(ttt):
    if ttt.graphics == True:
        if ttt.x == True:
            char = 'x'
            human(ttt, char)
            
        elif ttt.o == True:
            char = 'o'
            human(ttt, char)
        return
            
    else: 
        while (ttt.playing):
            if ttt.x == True:
                char = 'x'
                human(ttt, char)
                
            elif ttt.o == True:
                char = 'o'
                human(ttt, char)