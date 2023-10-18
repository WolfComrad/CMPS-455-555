# This is Patrick Theriot's Tic-Tac Toe Game

from graphicsGame import main
from helpers import welcome_screen
from terminalGame import play_No_Graphics

leave = False
while leave == False:
    welcome_screen()
    choice = input()
    
    if (choice == "graphic"):
            print("\nSWEET!!\nUse your mouse and click on the spot you want to go.\n"
                  "If you wish to restart click the 'r' key\n"
                  "when you are finished click the 'x' button on the top left corner.\n"
                  "There are a couple of different functions that can be used.\n"
                  "The game is set to single player. If you want multi player click 'g' to change game modes.\n"
                  "If you play single player, click '0' or '1' to change AI difficulty.\n"
                  " HAVE FUN!!")
            main()
    elif (choice == "plain"):
        play_No_Graphics()
    elif (choice == "exit"):
        leave = True
    else:
        print("I'm sorry could you type it again.")