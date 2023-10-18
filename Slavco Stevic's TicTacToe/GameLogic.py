# Function that lets us choose options when we start the game
def startTheGame(ttt):
    print ("Would you like to play with or without graphics? Type y/n:")
    answering = True
    ans = input()
    while answering:
        if ans == 'y':
            print("Playing with graphics...")
            ttt.graphics = True
            answering = False 
        elif ans == 'n':
            print("Playing without graphics...")
            answering = False
        else:
            print("Please enter a valid input!")
            ans = input()
    
    print ("Would you like to play against a human/dumb pc/smart pc? Type h/dpc/spc:")
    answering = True
    ans = input()
    
    while answering:
        if ans == 'h':
            print("Playing against human...")
            answering = False
            ttt.human = True
            
        elif ans == 'dpc':
            print("Playing against dumb pc...")
            ttt.dpc = True
            answering = False
            
        elif ans == 'spc':
            print("Playing against smart pc...")
            ttt.spc = True
            answering = False 
                
        else:
            print("Please enter a valid input!")
            ans = input()

# Function to show the board
def showBoard(ttt):
    for row in ttt.board:
        print(row)
        
# Function that checks whether a move was valid
def isValid(ttt):
    in_row = ttt.spot[0]
    in_col = ttt.spot[1]
    
    if in_row < 0 or in_col < 0 or in_row > 2 or in_col > 2:
        return False
    else: 
        if ttt.x == True:
            if ttt.board[in_row][in_col] == '#':
                return True
            else:
                return False
        if ttt.o == True:
            if ttt.board[in_row][in_col] == '#':
                return True
            else:
                return False
        
# Function that checks if the win is possible - 3 in a row
def checkWin(ttt):
    win = False
    char = ''
    if ttt.x == False:
        char = 'x'
    else:
        char = 'o'
    
    if ttt.board[0][0] == char and ttt.board[0][1] == char and ttt.board[0][2] == char:
        win = True
        ttt.c1 = [0,100]
        ttt.c2 = [600,100]
    elif ttt.board[1][0] == char and ttt.board[1][1] == char and ttt.board[1][2] == char:
        win = True
        ttt.c1 = [0,300]
        ttt.c2 = [600,300]
    elif ttt.board[2][0] == char and ttt.board[2][1] == char and ttt.board[2][2] == char:
        win = True
        ttt.c1 = [0,500]
        ttt.c2 = [600,500]
    elif ttt.board[0][0] == char and ttt.board[1][1] == char and ttt.board[2][2] == char:
        win = True
        ttt.c1 = [0,0]
        ttt.c2 = [600,600]
    elif ttt.board[0][0] == char and ttt.board[1][0] == char and ttt.board[2][0] == char:
        win = True
        ttt.c1 = [100,0]
        ttt.c2 = [100,600]
    elif ttt.board[0][1] == char and ttt.board[1][1] == char and ttt.board[2][1] == char:
        win = True
        ttt.c1 = [300,0]
        ttt.c2 = [300,600]
    elif ttt.board[0][2] == char and ttt.board[1][2] == char and ttt.board[2][2] == char:
        win = True
        ttt.c1 = [500,0]
        ttt.c2 = [500,600]
    elif ttt.board[0][2] == char and ttt.board[1][1] == char and ttt.board[2][0] == char:
        win = True
        ttt.c1 = [600,0]
        ttt.c2 = [0,600]
    
    if win == True:
        if ttt.x == False:
            ttt.winX = True
        else:
            ttt.winO = True
            
        showBoard(ttt)
        print(f"Player {char} wins!!!")
        quitGame(ttt)
    else:
        checkDraw(ttt)
        
# Function that checks for a draw - 9 turns
def checkDraw(ttt):
    if ttt.turns == 9:
        showBoard(ttt)
        print(f"Draw!!!")
        quitGame(ttt)
        
# Functions for quiting the game
def quitGame(ttt):
    ttt.end = True
    
    if ttt.graphics == True:
        print("Do you want to play a new game? Right click for yer or click exit for no.")
    else:
        print("Do you want to play a new game? Enter y/n:")

        answering = True
        ans = input()
        
        while answering:
            if ans == 'n':
                print("Thank you for playing.")
                ttt.playing = False
                answering = False
                
            elif ans == 'y':
                print("Starting a new game...")
                newGame(ttt)
                answering = False
                
            else:
                print("Please enter a valid input!")
                ans = input()
            
# Function for the new game - reseting all values that are needed for a new game
def newGame(ttt):
    ttt.board = [['#','#','#'],['#','#','#'],['#','#','#']]
    ttt.x = True
    ttt.o = False
    ttt.turns = 0
    ttt.winX = False
    ttt.winO = False
    ttt.end = False
