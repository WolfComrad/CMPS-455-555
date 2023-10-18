# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 11:52:44 2023

@author: HP
"""
from helpers import check_for_block_graphic, available_square
import os, sys
import pygame
import numpy as np

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
BACKGROUND = (28, 175, 150)
            
# Playing with graphics/multiplayer
def play_With_Graphics_multi():
    screenWidth = 600
    screenHeight = screenWidth
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Graphics Tic-Tac Toe")
    
    # Drawing the screen
    screen.fill(BACKGROUND)
    def make_board():
        pygame.draw.rect(screen, BLACK, (0,0,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE,0,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE*2,0,SQR_SIZE,SQR_SIZE), 3)
        
        pygame.draw.rect(screen, BLACK, (0,SQR_SIZE,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE,SQR_SIZE,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE*2,SQR_SIZE,SQR_SIZE,SQR_SIZE), 3)
        
        pygame.draw.rect(screen, BLACK, (0,SQR_SIZE*2,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE,SQR_SIZE*2,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE*2,SQR_SIZE*2,SQR_SIZE,SQR_SIZE), 3)
    
    # Creating the Board
    BOARD_ROWS = 3
    BOARD_COLS = 3
    SQR_SIZE = screenWidth//BOARD_COLS
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    make_board()
    
    # Method for drawing x and o
    def draw_figures():
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 1:
                    pygame.draw.circle(screen, GREEN, (int(col * SQR_SIZE + SQR_SIZE//2), int(row * SQR_SIZE + SQR_SIZE//2)), SQR_SIZE//2.6, SQR_SIZE//13)
                elif board[row][col] == 2:
                    pygame.draw.line(screen, RED, (col * SQR_SIZE + 40, row * SQR_SIZE + SQR_SIZE - 40), (col * SQR_SIZE + SQR_SIZE - 40, row * SQR_SIZE + 40), 25)
                    pygame.draw.line(screen, RED, (col * SQR_SIZE + 40, row * SQR_SIZE + 40), (col * SQR_SIZE + SQR_SIZE - 40, row * SQR_SIZE + SQR_SIZE - 40), 25)
    
    # Method to place the mark in our array
    def mark_square(row, col, player):
        board[row][col] = player
    
    # Method to see if the board is full
    def is_board_full():
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    return False
        return True
    
    def check_win(player):
        # vertical win check
        for col in range(BOARD_COLS):
            if board[0][col] == player and board[1][col] == player and board[2][col] == player:
                draw_vert_win_line(col, player)
                return True
        # horizontal win check
        for row in range(BOARD_ROWS):
            if board[row][0] == player and board[row][1] == player and board[row][2] == player:
                draw_hor_win_line(row, player)
                return True
        # forword die win check
        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            draw_backword_die_line(player)
            return True
        # backword die win check
        if board[2][0] == player and board[1][1] == player and board[0][2] == player:
            draw_forword_die_line(player)
            return True
        
        return False
    
    def draw_vert_win_line(col, player):
        posX = col * SQR_SIZE + SQR_SIZE//2
        if player == 1:
            color = GREEN
        elif player == 2:
            color = RED
        
        pygame.draw.line(screen, color, (posX, 15), (posX, screenHeight - 15), 15)
    
    def draw_hor_win_line(row, player):
        posY = row * SQR_SIZE + SQR_SIZE//2
        if player == 1:
            color = GREEN
        elif player == 2:
            color = RED
        
        pygame.draw.line(screen, color, (15, posY), (screenWidth - 15, posY), 15)
    
    def draw_forword_die_line(player):
       if player == 1:
           color = GREEN
       elif player == 2:
           color = RED
       
       pygame.draw.line(screen, color, (15, screenHeight - 15), (screenWidth - 15, 15), 15) 
    
    def draw_backword_die_line(player):
        if player == 1:
            color = GREEN
        elif player == 2:
            color = RED
        
        pygame.draw.line(screen, color, (15, 15), (screenWidth - 15, screenHeight - 15), 15)
        
    # Method to see if the spot is open
    def available_square(row, col):
        return board[row][col] == 0
        
    def restart():
        screen.fill(BACKGROUND)
        make_board()
        player = 1
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                board[row][col] = 0
    
    player = 1
    game_over = False
    leave = False
    # Main loop
    while not leave:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                leave = True
                #sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0] # x
                mouseY = event.pos[1] # y
                clicked_row = int(mouseY // SQR_SIZE)
                clicked_col = int(mouseX // SQR_SIZE)
                
                if available_square(clicked_row, clicked_col):
                    if player == 1:
                        mark_square(clicked_row, clicked_col, 1)
                        if check_win(player):
                            game_over = True
                        player = 2
                    elif player == 2:
                        mark_square(clicked_row, clicked_col, 2)
                        if check_win(player):
                            game_over = True
                        player = 1
                        
                    draw_figures()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    game_over = False
                    
        pygame.display.update()
    pygame.display.quit()
    os.system('cls' if os.name == 'nt' else 'clean')
    
    
    
    
    
    
    
    
    
    
    
    
    
# Playing with graphics/single player
def play_With_Graphics_single():
    screenWidth = 600
    screenHeight = screenWidth
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Graphics Tic-Tac Toe")
    
    # Drawing the screen
    screen.fill(BACKGROUND)
    def make_board():
        pygame.draw.rect(screen, BLACK, (0,0,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE,0,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE*2,0,SQR_SIZE,SQR_SIZE), 3)
        
        pygame.draw.rect(screen, BLACK, (0,SQR_SIZE,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE,SQR_SIZE,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE*2,SQR_SIZE,SQR_SIZE,SQR_SIZE), 3)
        
        pygame.draw.rect(screen, BLACK, (0,SQR_SIZE*2,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE,SQR_SIZE*2,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE*2,SQR_SIZE*2,SQR_SIZE,SQR_SIZE), 3)
    
    # Creating the Board
    BOARD_ROWS = 3
    BOARD_COLS = 3
    SQR_SIZE = screenWidth//BOARD_COLS
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    make_board()
    
    # Method for drawing x and o
    def draw_figures():
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 1:
                    pygame.draw.circle(screen, GREEN, (int(col * SQR_SIZE + SQR_SIZE//2), int(row * SQR_SIZE + SQR_SIZE//2)), SQR_SIZE//2.6, SQR_SIZE//13)
                elif board[row][col] == 2:
                    pygame.draw.line(screen, RED, (col * SQR_SIZE + 40, row * SQR_SIZE + SQR_SIZE - 40), (col * SQR_SIZE + SQR_SIZE - 40, row * SQR_SIZE + 40), 25)
                    pygame.draw.line(screen, RED, (col * SQR_SIZE + 40, row * SQR_SIZE + 40), (col * SQR_SIZE + SQR_SIZE - 40, row * SQR_SIZE + SQR_SIZE - 40), 25)
    
    # Method to place the mark in our array
    def mark_square(row, col, player):
        board[row][col] = player
        
    def PC_mark_square(): #Player = 2
        print("mark")
        check_for_block_graphic(board)
    
    # Method to see if the board is full
    def is_board_full():
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    return False
        return True
    
    def check_win(player):
        # vertical win check
        for col in range(BOARD_COLS):
            if board[0][col] == player and board[1][col] == player and board[2][col] == player:
                draw_vert_win_line(col, player)
                return True
        # horizontal win check
        for row in range(BOARD_ROWS):
            if board[row][0] == player and board[row][1] == player and board[row][2] == player:
                draw_hor_win_line(row, player)
                return True
        # forword die win check
        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            draw_backword_die_line(player)
            return True
        # backword die win check
        if board[2][0] == player and board[1][1] == player and board[0][2] == player:
            draw_forword_die_line(player)
            return True
        
        return False
    
    def draw_vert_win_line(col, player):
        posX = col * SQR_SIZE + SQR_SIZE//2
        if player == 1:
            color = GREEN
        elif player == 2:
            color = RED
        
        pygame.draw.line(screen, color, (posX, 15), (posX, screenHeight - 15), 15)
    
    def draw_hor_win_line(row, player):
        posY = row * SQR_SIZE + SQR_SIZE//2
        if player == 1:
            color = GREEN
        elif player == 2:
            color = RED
        
        pygame.draw.line(screen, color, (15, posY), (screenWidth - 15, posY), 15)
    
    def draw_forword_die_line(player):
       if player == 1:
           color = GREEN
       elif player == 2:
           color = RED
       
       pygame.draw.line(screen, color, (15, screenHeight - 15), (screenWidth - 15, 15), 15) 
    
    def draw_backword_die_line(player):
        if player == 1:
            color = GREEN
        elif player == 2:
            color = RED
        
        pygame.draw.line(screen, color, (15, 15), (screenWidth - 15, screenHeight - 15), 15)
        
    def restart():
        screen.fill(BACKGROUND)
        make_board()
        player = 1
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                board[row][col] = 0
    
    player = 1
    game_over = False
    leave = False
    # Main loop
    while not leave:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                leave = True
                #sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0] # x
                mouseY = event.pos[1] # y
                clicked_row = int(mouseY // SQR_SIZE)
                clicked_col = int(mouseX // SQR_SIZE)
                
                if player == 1:                    
                    if available_square(clicked_row, clicked_col, board):
                        mark_square(clicked_row, clicked_col, 1)
                        print(board)
                        if check_win(player):
                            game_over = True
                        player = 2
                    draw_figures()
                elif player == 2:
                    print("hey")
                    PC_mark_square()
                    print(board)
                    if check_win(player):
                        game_over = True
                    player = 1
                            
                    draw_figures()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    game_over = False
                    
        pygame.display.update()
    pygame.display.quit()
    os.system('cls' if os.name == 'nt' else 'clean')