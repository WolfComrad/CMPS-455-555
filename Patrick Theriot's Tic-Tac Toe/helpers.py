# This is the helper for TicTacToe.py
import random
import numpy as np

def welcome_screen():
    print("\n\nWELCOME!!! WHAT TIC-TAC-TOE VERSION DO YOU WANT??\n"
          "For graphics type 'graphic'\n"
          "For no graphics type 'plain'\n"
          "Lastly, you can type 'exit' to leave")

def welcome_screen_no_graphics():
    print("\n\nWELCOME TO NO GRAPHICS TIC-TAC-TOE!!\n"
          "Choose what style you want to play\n"
          "type 'm' for multiplayer or 's' for single player\n"
          "type 'back' to go back.")

def draw_board(spots):
    consoleBoard = (f"|{spots[1]}|{spots[2]}|{spots[3]}|\n"
                    f"|{spots[4]}|{spots[5]}|{spots[6]}|\n"
                    f"|{spots[7]}|{spots[8]}|{spots[9]}|")
    print(consoleBoard)
    
def check_turn(turn):
    if turn % 2 == 0:
        return 'O'
    else:
        return 'X'
    
def check_for_win(spots):
    # Checking for horizontal cases
    if (spots[1] == spots[2] == spots[3]) \
        or (spots[4] == spots[5] == spots[6]) \
        or (spots[7] == spots[8] == spots[9]) \
        or (spots[1] == spots[4] == spots[7]) \
        or (spots[2] == spots[5] == spots[8]) \
        or (spots[3] == spots[6] == spots[9]) \
        or (spots[1] == spots[5] == spots[9]) \
        or (spots[3] == spots[5] == spots[7]):
            return True
    else:
        return False

def can_i_loose_player2(spots):
    if ((spots[2] == 'X' and spots[3] == 'X') or (spots[4] == 'X' and spots[7] == 'X') or (spots[5] == 'X' and spots[9] == 'X')) and spots[1] == '1':
        return 1;
    elif ((spots[1] == 'X' and spots[3] == 'X') or (spots[5] == 'X' and spots[8] == 'X')) and spots[2] == '2':
        return 2
    elif ((spots[1] == 'X' and spots[2] == 'X') or (spots[5] == 'X' and spots[7] == 'X') or (spots[6] == 'X' and spots[9] == 'X')) and spots[3] == '3':
        return 3
    elif ((spots[5] == 'X' and spots[6] == 'X') or (spots[1] == 'X' and spots[7] == 'X')) and spots[4] == '4':
        return 4
    elif ((spots[4] == 'X' and spots[6] == 'X') or (spots[2] == 'X' and spots[8] == 'X') or (spots[1] == 'X' and spots[9] == 'X') or (spots[3] == 'X' and spots[7] == 'X')) and spots[5] == '5':
        return 5
    elif ((spots[4] == 'X' and spots[5] == 'X') or (spots[3] == 'X' and spots[9] == 'X')) and spots[6] == '6':
        return 6
    elif ((spots[1] == 'X' and spots[4] == 'X') or (spots[8] == 'X' and spots[9] == 'X') or (spots[5] == 'X' and spots[3] == 'X')) and spots[7] == '7':
        return 7
    elif ((spots[7] == 'X' and spots[9] == 'X') or (spots[2] == 'X' and spots[5] == 'X')) and spots[8] == '8':
        return 8
    elif ((spots[7] == 'X' and spots[8] == 'X') or (spots[3] == 'X' and spots[6] == 'X') or (spots[1] == 'X' and spots[5] == 'X')) and spots[9] == '9':
        return 9
    else:
        return open_spots(spots)
    
def can_i_win_player2(spots):
    if ((spots[2] == 'O' and spots[3] == 'O') or (spots[4] == 'O' and spots[7] == 'O') or (spots[5] == 'O' and spots[9] == 'O')) and spots[1] == '1':
        return 1;
    elif ((spots[1] == 'O' and spots[3] == 'O') or (spots[5] == 'O' and spots[8] == 'O')) and spots[2] == '2':
        return 2
    elif ((spots[1] == 'O' and spots[2] == 'O') or (spots[5] == 'O' and spots[7] == 'O') or (spots[6] == 'O' and spots[9] == 'O')) and spots[3] == '3':
        return 3
    elif ((spots[5] == 'O' and spots[6] == 'O') or (spots[1] == 'O' and spots[7] == 'O')) and spots[4] == '4':
        return 4
    elif ((spots[4] == 'O' and spots[6] == 'O') or (spots[2] == 'O' and spots[8] == 'O') or (spots[1] == 'O' and spots[9] == 'O') or (spots[3] == 'X' and spots[7] == 'X')) and spots[5] == '5':
        return 5
    elif ((spots[4] == 'O' and spots[5] == 'O') or (spots[3] == 'O' and spots[9] == 'O')) and spots[6] == '6':
        return 6
    elif ((spots[1] == 'O' and spots[4] == 'O') or (spots[8] == 'O' and spots[9] == 'O') or (spots[5] == 'O' and spots[3] == 'O')) and spots[7] == '7':
        return 7
    elif ((spots[7] == 'O' and spots[9] == 'O') or (spots[2] == 'O' and spots[5] == 'O')) and spots[8] == '8':
        return 8
    elif ((spots[7] == 'O' and spots[8] == 'O') or (spots[3] == 'O' and spots[6] == 'O') or (spots[1] == 'O' and spots[5] == 'O')) and spots[9] == '9':
        return 9
    else:
        return can_i_loose_player2(spots)
    
def can_i_win_player1(spots):
    if ((spots[2] == 'X' and spots[3] == 'X') or (spots[4] == 'X' and spots[7] == 'X') or (spots[5] == 'X' and spots[9] == 'X')) and spots[1] == '1':
        return 1;
    elif ((spots[1] == 'X' and spots[3] == 'X') or (spots[5] == 'X' and spots[8] == 'X')) and spots[2] == '2':
        return 2
    elif ((spots[1] == 'X' and spots[2] == 'X') or (spots[5] == 'X' and spots[7] == 'X') or (spots[6] == 'X' and spots[9] == 'X')) and spots[3] == '3':
        return 3
    elif ((spots[5] == 'X' and spots[6] == 'X') or (spots[1] == 'X' and spots[7] == 'X')) and spots[4] == '4':
        return 4
    elif ((spots[4] == 'X' and spots[6] == 'X') or (spots[2] == 'X' and spots[8] == 'X') or (spots[1] == 'X' and spots[9] == 'X') or (spots[3] == 'X' and spots[7] == 'X')) and spots[5] == '5':
        return 5
    elif ((spots[4] == 'X' and spots[5] == 'X') or (spots[3] == 'X' and spots[9] == 'X')) and spots[6] == '6':
        return 6
    elif ((spots[1] == 'X' and spots[4] == 'X') or (spots[8] == 'X' and spots[9] == 'X') or (spots[5] == 'X' and spots[3] == 'X')) and spots[7] == '7':
        return 7
    elif ((spots[7] == 'X' and spots[9] == 'X') or (spots[2] == 'X' and spots[5] == 'X')) and spots[8] == '8':
        return 8
    elif ((spots[7] == 'X' and spots[8] == 'X') or (spots[3] == 'X' and spots[6] == 'X') or (spots[1] == 'X' and spots[5] == 'X')) and spots[9] == '9':
        return 9
    else:
        return can_i_loose_player1(spots)
    
def can_i_loose_player1(spots):
    if ((spots[2] == 'O' and spots[3] == 'O') or (spots[4] == 'O' and spots[7] == 'O') or (spots[5] == 'O' and spots[9] == 'O')) and spots[1] == '1':
        return 1;
    elif ((spots[1] == 'O' and spots[3] == 'O') or (spots[5] == 'O' and spots[8] == 'O')) and spots[2] == '2':
        return 2
    elif ((spots[1] == 'O' and spots[2] == 'O') or (spots[5] == 'O' and spots[7] == 'O') or (spots[6] == 'O' and spots[9] == 'O')) and spots[3] == '3':
        return 3
    elif ((spots[5] == 'O' and spots[6] == 'O') or (spots[1] == 'O' and spots[7] == 'O')) and spots[4] == '4':
        return 4
    elif ((spots[4] == 'O' and spots[6] == 'O') or (spots[2] == 'O' and spots[8] == 'O') or (spots[1] == 'O' and spots[9] == 'O') or (spots[3] == 'X' and spots[7] == 'X')) and spots[5] == '5':
        return 5
    elif ((spots[4] == 'O' and spots[5] == 'O') or (spots[3] == 'O' and spots[9] == 'O')) and spots[6] == '6':
        return 6
    elif ((spots[1] == 'O' and spots[4] == 'O') or (spots[8] == 'O' and spots[9] == 'O') or (spots[5] == 'O' and spots[3] == 'O')) and spots[7] == '7':
        return 7
    elif ((spots[7] == 'O' and spots[9] == 'O') or (spots[2] == 'O' and spots[5] == 'O')) and spots[8] == '8':
        return 8
    elif ((spots[7] == 'O' and spots[8] == 'O') or (spots[3] == 'O' and spots[6] == 'O') or (spots[1] == 'O' and spots[5] == 'O')) and spots[9] == '9':
        return 9
    else:
        return open_spots(spots)

def open_spots(spots):
    array = []
    for count in spots:
        if spots[count] == str(count):
            array.append(count)
            count += 1
        else:
            count += 1
    return random.choice(array)