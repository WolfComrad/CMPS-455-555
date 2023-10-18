import sys, random, copy, os
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

WIDTH = 600
HEIGHT = WIDTH
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BACKGROUND)
# Creating the Board
BOARD_ROWS = 3
BOARD_COLS = 3
SQR_SIZE = WIDTH//BOARD_COLS
cir_width = 15
radius = SQR_SIZE // 2.7
    
class Board:
    def __init__(self):
        self.board_sqr = np.zeros((BOARD_ROWS,BOARD_COLS))
        self.empty_sqrs = self.board_sqr
        self.marked_sqrs = 0
    
    def mark_sqr(self, row, col, player):
        self.board_sqr[row][col] = player
        self.marked_sqrs += 1
        
    def empty_sqr(self, row, col):
        return self.board_sqr[row][col] == 0
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs
    
    def is_full(self):
        return self.marked_sqrs == 9
    
    def is_empty(self):
        return self.marked_sqrs == 0
    
    def final_state(self, show = False):
        # vertical wins
        for col in range(BOARD_COLS):
           if self.board_sqr[0][col] == self.board_sqr[1][col] == self.board_sqr[2][col] != 0:
               if show:
                   color = GREEN if self.board_sqr[0][col] == 1 else RED
                   posX = col * SQR_SIZE + SQR_SIZE//2
                   pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), 15)
               return self.board_sqr[0][col]
        # Horizontal wins
        for row in range(BOARD_ROWS):
           if self.board_sqr[row][0] == self.board_sqr[row][1] == self.board_sqr[row][2] != 0:
               if show:
                   color = GREEN if self.board_sqr[row][0] == 1 else RED
                   posY = row * SQR_SIZE + SQR_SIZE//2
                   pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), 15)
               return self.board_sqr[row][0]
        # Diagonals
        if self.board_sqr[0][0] == self.board_sqr[1][1] == self.board_sqr[2][2] != 0:
            if show:
                   color = GREEN if self.board_sqr[0][0] == 1 else RED
                   pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)
            return self.board_sqr[0][0]
        if self.board_sqr[2][0] == self.board_sqr[1][1] == self.board_sqr[0][2] != 0:
            if show:
                   color = GREEN if self.board_sqr[2][0] == 1 else RED
                   pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)
            return self.board_sqr[2][0]
        # No wins
        return 0

class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player
        
    def eval(self, board):
        if self.level == 0:
            eval = 'random'
            move = self.random(board)
        else:
            eval, move = self.minimax(board, False)
        print(f'AI has chosen to mark the square in pos {move} with an eval of {eval}')
        return move
        
    def random(self, board):
        empty_sqrs = board.get_empty_sqrs()
        index = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[index]
    
    def minimax(self, board, maximizing):
        # Terminal case
        case = board.final_state()
        # Player 1 wins
        if case == 1:
            return 1, None
        # Player 2 wins
        if case == 2:
            return -1, None
        # Cat got the game
        elif board.is_full():
            return 0, None
        if maximizing:
            max_eval = -10
            best_move = None
            empty_sqrs = board.get_empty_sqrs()
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move
        elif not maximizing:
            min_eval = 10
            best_move = None
            empty_sqrs = board.get_empty_sqrs()
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move

class Game:    
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 # 1-circle # 2-cross
        self.gamemode = 'singlePlayer' #singlePlayer
        self.running = True
        self.boxes()
        
    def reset(self):
        self.__init__()
        
    def make_move(self, row, col):
        self.board.mark_sqr(row,col,self.player)
        self.draw_figures(row,col)
        self.change_turn()
        
    def boxes(self):
        screen.fill(BACKGROUND)
        pygame.draw.rect(screen, BLACK, (0,0,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE,0,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE*2,0,SQR_SIZE,SQR_SIZE), 3)
        
        pygame.draw.rect(screen, BLACK, (0,SQR_SIZE,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE,SQR_SIZE,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE*2,SQR_SIZE,SQR_SIZE,SQR_SIZE), 3)
        
        pygame.draw.rect(screen, BLACK, (0,SQR_SIZE*2,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE,SQR_SIZE*2,SQR_SIZE,SQR_SIZE), 3)
        pygame.draw.rect(screen, BLACK, (SQR_SIZE*2,SQR_SIZE*2,SQR_SIZE,SQR_SIZE), 3)
        
    def change_turn(self):
        self.player = self.player % 2 + 1
        
    def draw_figures(self, row, col):
        if self.player == 1:
            center = (col * SQR_SIZE + SQR_SIZE // 2, row * SQR_SIZE + SQR_SIZE // 2)
            pygame.draw.circle(screen, GREEN, center, radius, cir_width)
        elif self.player == 2:
            pygame.draw.line(screen, RED, (col * SQR_SIZE + 40, row * SQR_SIZE + SQR_SIZE - 40), (col * SQR_SIZE + SQR_SIZE - 40, row * SQR_SIZE + 40), 25)
            pygame.draw.line(screen, RED, (col * SQR_SIZE + 40, row * SQR_SIZE + 40), (col * SQR_SIZE + SQR_SIZE - 40, row * SQR_SIZE + SQR_SIZE - 40), 25)

    def change_gamemode(self):
        self.gamemode = 'singlePlayer' if self.gamemode == 'multiPlayer' else 'multiPlayer'

    def is_over(self):
        return self.board.final_state(show = True) != 0 or self.board.is_full()

def main():
    game = Game()
    board = game.board
    ai = game.ai
    leave = False
    # Main loop
    while not leave:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                leave = True
                # pygame.quit()
                # sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQR_SIZE
                col = pos[0] // SQR_SIZE
                if board.empty_sqr(row,col) and game.running:
                    game.make_move(row,col)
                    if game.is_over():
                        game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                if event.key == pygame.K_g:
                    game.change_gamemode()
                if event.key == pygame.K_0:
                    ai.level = 0
                if event.key == pygame.K_1:
                    ai.level = 1
        if game.gamemode == 'singlePlayer' and game.player == ai.player and game.running:
            pygame.display.update()
            row, col = ai.eval(board)
            game.make_move(row,col)
            if game.is_over():
                    game.running = False
        pygame.display.update()
    pygame.display.quit()
    os.system('cls' if os.name == 'nt' else 'clean')
# main()