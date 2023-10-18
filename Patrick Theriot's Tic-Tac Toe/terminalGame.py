from helpers import draw_board, check_turn, check_for_win, welcome_screen_no_graphics, can_i_win_player2, can_i_win_player1
import os, sys

def play_No_Graphics():
    # Playing without graphics
    leave = False
    while leave == False:
        welcome_screen_no_graphics()
        choice = input()
        
        if choice == 'm':
            
            continueGame = "yes"
            
            while continueGame == "yes":
                # Using a dictionary to make my board
                board = {1 : '1', 2 : '2', 3 : '3', 4 : '4', 5 : '5',
                        6 : '6', 7 : '7', 8 : '8', 9 : '9'}
                playing = True
                complete = False
                turn = 0
                prev_turn = -1
                while playing:
                    # Reseting my board/screen
                    os.system('cls' if os.name == 'nt' else 'clear')
                    draw_board(board)
                    # If an invalid turn accurred, let the player know
                    if prev_turn == turn:
                        print("Invalid location selected, please choose another or press q to quit.")
                    prev_turn = turn
                    print("Player " + str((turn % 2) + 1 ) + "'s turn: Pick your "
                          "spot or press q to quit.")
                    # Getting the input from the player
                    choice = input()
                    if choice == 'q':
                        playing = False
                    # Checking to see if the player input a number from 1-9
                    elif str.isdigit(choice) and int(choice) in board:
                        # Checking if the location on the board is already taken
                        if not board[int(choice)] in {"X", "O"}:
                            # If the input is valid, update the board
                            turn += 1
                            board[int(choice)] = check_turn(turn)
                    # Checking to see if the game has ended by ether someone winning or a tie
                    if check_for_win(board):
                        playing, complete = False, True
                    if turn > 8:
                        playing = False
                    
                # Printing the results of the game
                os.system('cls' if os.name == 'nt' else 'clean')
                draw_board(board)
                # If there is a winner, say who won
                if (choice == 'q'):
                    os.system('cls' if os.name == 'nt' else 'clean')
                    print("I'm sad you quit..")
                    continueGame = False
                else:
                    if complete:
                        if check_turn(turn) == 'X':
                            print("Player 1 Wins!!!")
                        else:
                            print("Player 2 Wins!!!")
                    else:
                        print("The Cat Won...")
                    # Checking to see if they wish to play again
                    print("Do you want to play again? (yes/no)")
                    continueGame = input()
                    if (continueGame == "yes"):
                        print("Yay!!!")
            print("Thanks for playing!")
            
        elif choice == 's':
            print("Do you want to go first? (y/n)")
            choice = input()
            if choice == 'y':
                # Using a dictionary to make my board
                board = {1 : '1', 2 : '2', 3 : '3', 4 : '4', 5 : '5',
                        6 : '6', 7 : '7', 8 : '8', 9 : '9'}
                playing = True
                complete = False
                turn = 0
                prev_turn = -1
                while playing:
                    # Reseting my board/screen
                    os.system('cls' if os.name == 'nt' else 'clear')
                    draw_board(board)
                    # If an invalid turn accurred, let the player know
                    #if prev_turn == turn:
                     #   print("Invalid location selected, please choose another or press q to quit.")
                    #prev_turn = turn
                    playerturn = str((turn % 2) + 1 )
                    if playerturn == '1':
                        print("It's your turn: Pick your "
                              "spot or press q to quit.")
                        # Getting the input from the player
                        choice = input()
                        if choice == 'q':
                            playing = False
                        # Checking to see if the player input a number from 1-9
                        elif str.isdigit(choice) and int(choice) in board:
                            # Checking if the location on the board is already taken
                            if not board[int(choice)] in {"X", "O"}:
                                # If the input is valid, update the board
                                turn += 1
                                board[int(choice)] = check_turn(turn)
                        # Checking to see if the game has ended by ether someone winning or a tie
                        if check_for_win(board):
                            playing, complete = False, True
                        if turn > 8:
                            playing = False
                    # The Computer plays
                    elif playerturn == '2':
                        print("It's the computer's turn: Pick your "
                              "spot or press q to quit.")
                        # Checking where to play
                        choice = can_i_win_player2(board)
                        # Update the board
                        turn += 1
                        board[int(choice)] = check_turn(turn)
                        # Checking to see if the game has ended by ether someone winning or a tie
                        if check_for_win(board):
                            playing, complete = False, True
                        if turn > 8:
                            playing = False
                            
            elif choice == 'n':
                # Using a dictionary to make my board
                board = {1 : '1', 2 : '2', 3 : '3', 4 : '4', 5 : '5',
                        6 : '6', 7 : '7', 8 : '8', 9 : '9'}
                playing = True
                complete = False
                turn = 0
                prev_turn = -1
                while playing:
                    # Reseting my board/screen
                    os.system('cls' if os.name == 'nt' else 'clear')
                    draw_board(board)
                    playerturn = str((turn % 2) + 1 )
                    if playerturn == '1':
                        print("It's the computer's turn: Pick your "
                              "spot or press q to quit.")
                        # Checking where to play
                        choice = can_i_win_player1(board)
                        # Update the board
                        turn += 1
                        board[int(choice)] = check_turn(turn)
                        # Checking to see if the game has ended by ether someone winning or a tie
                        if check_for_win(board):
                            playing, complete = False, True
                        if turn > 8:
                            playing = False
                    elif playerturn == '2':
                        print("It's your turn: Pick your "
                              "spot or press q to quit.")
                        # Getting the input from the player
                        choice = input()
                        if choice == 'q':
                            playing = False
                        # Checking to see if the player input a number from 1-9
                        elif str.isdigit(choice) and int(choice) in board:
                            # Checking if the location on the board is already taken
                            if not board[int(choice)] in {"X", "O"}:
                                # If the input is valid, update the board
                                turn += 1
                                board[int(choice)] = check_turn(turn)
                        # Checking to see if the game has ended by ether someone winning or a tie
                        if check_for_win(board):
                            playing, complete = False, True
                        if turn > 8:
                            playing = False
            # Printing the results of the game
            os.system('cls' if os.name == 'nt' else 'clean')
            draw_board(board)
            # If there is a winner, say who won
            if (choice == 'q'):
                os.system('cls' if os.name == 'nt' else 'clean')
                print("I'm sad you quit..")
                continueGame = False
            else:
                if complete:
                    if check_turn(turn) == 'X':
                        print("Player 1 Wins!!!")
                    else:
                        print("Player 2 Wins!!!")
                else:
                    print("The Cat Won...")
                # Checking to see if they wish to play again
                print("Do you want to play again? (yes/no)")
                continueGame = input()
                if (continueGame == "yes"):
                    print("Yay!!!")
                    
            print("Thanks for playing!")
        elif choice == 'back':
            leave = True