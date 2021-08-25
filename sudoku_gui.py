import pygame, sys
from pygame.event import clear
from pygame.locals import *
pygame.init()

#####################################
#     GLOBAL VARIABLES - START
#####################################

BLANK_SPACE = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (175, 175, 175)
GRAY = (125, 125, 125)
DARK_BLUE = (0, 51, 102)
TEA_GREEN = (134, 194, 156)
DARK_GREEN = (115, 175, 140)
RED = (161, 40, 48)

WIDTH, HEIGHT = 500, 500
MONT_FONT = pygame.font.SysFont('montserratregular', 15)
CLOCK = pygame.time.Clock()
FPS = 10

LINE_START = 475
LINE_END = 25
SQUARE_SIZE = int((LINE_START - LINE_END) / 9)

POSITION1 = (0, 0)

GRID = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]]

GRID_COPY = [row[:] for row in GRID]

SOLVING_GRID = [row[:] for row in GRID]

#####################################
#     GLOBAL VARIABLES - END
#####################################

#####################################
#       SUDOKU SOLVER - START
#####################################

def valid(arr):
    ''' input:      arr, a one-dimensional array
        returns:    True, if the array does not contain more than one of each integer from 1 to 9
                    False, otherwise
    '''
    nums = [x for x in arr if x != BLANK_SPACE]
    numsSet = set(nums)
    if len(numsSet) != len(nums):
        return False
    else:
        return True
    
def spanThree(x):
    ''' input:      x, an integer that indicates an index in an array of length 9
        returns:    an array that indicates the starting and stopping index (of length 3) of a length 9 array where x is located
    '''
    if x < 3:
        return [0, 3]
    elif x > 5:
        return [6, 9]
    else:
        return [3, 6]

def isValidRCB(board, i, j):
    ''' inputs:     board, a 9 x 9 two-dimensional array
                    i, the index of the current row
                    j, the index of the current column
        returns:    True, if the current row, column, and box are valid
                    False, otherwise
    '''
    col = [board[x][j] for x in range(len(board))]
    rectangle = board[spanThree(i)[0]:spanThree(i)[1]]
    square1 = [y[spanThree(j)[0]:spanThree(j)[1]] for y in rectangle]
    square = sum(square1, [])
    return (valid(board[i])) and (valid(col)) and valid(square)

def fullGrid(board):
    ''' input:      board, a 9 x 9 two-dimensional array
        returns:    True, if the board is full
                    False, otherwise
    '''
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == BLANK_SPACE:
                return False
    return True

def emptyLoc(board, row, col):
    ''' input:      board, a 9 x 9 two-dimensional array
                    row, the index of the current row in the board
                    col, the index of the current column in the board
        returns:    True, if there exists an empty location on the board
                    False, otherwise
                    Also finds the first empty location (top to bottom, left to right) on the board
    '''
    if board[row][col] == BLANK_SPACE:
        return [True, row, col]
    else:
        for i in range(row, len(board)):
            for j in range(col, len(board)):
                if board[i][j] == BLANK_SPACE:
                    row = i
                    col = j
                    return [True, row, col]
    return [False, row, col]

def solveSudoku(board):
    ''' input:      board, a 9 x 9 two-dimensional array
        returns:    True, if the board is solved
                    False, if the board cannot be solved
    '''
    row = 0
    col = 0
    
    if not emptyLoc(board, row, col)[0]:
        return True
    
    row, col = emptyLoc(board, row, col)[1], emptyLoc(board, row, col)[2]
    
    for num in range(1, len(board)+1):
        board[row][col] = num
        if isValidRCB(board, row, col):
            if solveSudoku(board):
                return True
    board[row][col] = BLANK_SPACE
    return False

solveSudoku(GRID_COPY) # solved GRID

# [[5, 3, 4, 6, 7, 8, 9, 1, 2],
#  [6, 7, 2, 1, 9, 5, 3, 4, 8],
#  [1, 9, 8, 3, 4, 2, 5, 6, 7],
#  [8, 5, 9, 7, 6, 1, 4, 2, 3],
#  [4, 2, 6, 8, 5, 3, 7, 9, 1],
#  [7, 1, 3, 9, 2, 4, 8, 5, 6],
#  [9, 6, 1, 5, 3, 7, 2, 8, 4],
#  [2, 8, 7, 4, 1, 9, 6, 3, 5],
#  [3, 4, 5, 2, 8, 6, 1, 7, 9]]

#####################################
#       SUDOKU SOLVER - END
#####################################

def solveSudokuGraphic(board, screen):
    ''' input:      board, a 9 x 9 two-dimensional array
        returns:    True, if the board is solved
                    False, if the board cannot be solved
                    Renders the fully solved sudoku board
    '''
    row = 0
    col = 0
    
    if not emptyLoc(board, row, col)[0]:
        return True
    
    row, col = emptyLoc(board, row, col)[1], emptyLoc(board, row, col)[2]
    
    for num in range(1, len(board)+1):
        board[row][col] = num
        if isValidRCB(board, row, col):
            draw_grid(screen)
            pygame.display.update()
            pygame.time.wait(100)
            if solveSudoku(board):
                return True
            else:
                board[row][col] = BLANK_SPACE 
            screen.fill(WHITE)
            draw_grid(screen)
            pygame.display.update()
    return False

def mouseDown(screen, event, active, cell_x, cell_y, position1):
    ''' inputs:     screen, the display window
                    event, the pygame event
                    active, a boolean that signifies whether the box is active
                    cell_x, the x-position of the mouse
                    cell_y, the y-position of the mouse
                    position1, the previous position of the mouse (default = (0, 0))
        returns:    nothing, but draws a green box where the mouse clicked
    '''
    rectangle = pygame.Rect(cell_x*50 + 31, cell_y*50 + 31, SQUARE_SIZE-10, SQUARE_SIZE-10)
    rectangle1 = pygame.Rect(position1[0]*50 + 31, position1[1]*50 + 31, SQUARE_SIZE-10, SQUARE_SIZE-10)
    draw_grid(screen)
    if active:
        pygame.draw.rect(screen, WHITE, rectangle1, 3)
        pygame.draw.rect(screen, TEA_GREEN, rectangle, 3)
        position1 = (cell_x, cell_y)
        # print('position 1: ', position1)
        return position1
    else:
        pygame.draw.rect(screen, WHITE, rectangle, 3)

def keyDown(screen, event, active, cell_x, cell_y):
    ''' inputs:     screen, the display window
                    event, the pygame event
                    active, a boolean that signifies whether the box is active
                    cell_x, the x-position of the mouse
                    cell_y, the y-position of the mouse
        returns:    nothing, but performs actions based on the pressed down key
    '''
    global SOLVING_GRID
    global GRID
    text = ''
    if GRID[cell_y][cell_x] != BLANK_SPACE:
        pass
    elif active:
        rectangle1 = pygame.Rect(cell_x*50 + 27, cell_y*50 + 27, SQUARE_SIZE-5, SQUARE_SIZE-5)
        rectangle = pygame.Rect(cell_x*50 + 31, cell_y*50 + 31, SQUARE_SIZE-10, SQUARE_SIZE-10)
        pygame.draw.rect(screen, WHITE, rectangle1)
        pygame.draw.rect(screen, TEA_GREEN, rectangle, 3)
        if event.key == pygame.K_BACKSPACE:
            text = ''
            SOLVING_GRID[cell_y][cell_x] = 0
        if event.key == pygame.K_SPACE:
            SOLVING_GRID = [row[:] for row in GRID]
            solveSudokuGraphic(SOLVING_GRID, screen)
        if event.key == pygame.K_r:
            SOLVING_GRID = [row[:] for row in GRID]
            clear_board(screen)
        if event.key == pygame.K_1:
            text = '1'
            SOLVING_GRID[cell_y][cell_x] = int(text)
        if event.key == pygame.K_2:
            text = '2'
            SOLVING_GRID[cell_y][cell_x] = int(text)
        if event.key == pygame.K_3:
            text = '3'
            SOLVING_GRID[cell_y][cell_x] = int(text)
        if event.key == pygame.K_4:
            text = '4'
            SOLVING_GRID[cell_y][cell_x] = int(text)
        if event.key == pygame.K_5:
            text = '5'
            SOLVING_GRID[cell_y][cell_x] = int(text)
        if event.key == pygame.K_6:
            text = '6'
            SOLVING_GRID[cell_y][cell_x] = int(text)
        if event.key == pygame.K_7:
            text = '7'
            SOLVING_GRID[cell_y][cell_x] = int(text)
        if event.key == pygame.K_8:
            text = '8'
            SOLVING_GRID[cell_y][cell_x] = int(text)
        if event.key == pygame.K_9:
            text = '9'
            SOLVING_GRID[cell_y][cell_x] = int(text)
    draw_grid(screen)  
        
def draw_board(screen):
    ''' input:      screen, the display window
        returns:    None, but draws the Sudoku lines onto the screen
    '''
    for i in range(LINE_START, 0, -SQUARE_SIZE):
        if i == LINE_START or i == LINE_START - SQUARE_SIZE*3 or i == LINE_START - SQUARE_SIZE*6 or i == LINE_START - SQUARE_SIZE*9:
            pygame.draw.line(screen, BLACK, (LINE_END, i), (LINE_START, i), 2)
            pygame.draw.line(screen, BLACK, (i, LINE_START), (i, LINE_END), 2)
        else:
            pygame.draw.line(screen, LIGHT_GRAY, (LINE_END, i), (LINE_START, i), 1)
            pygame.draw.line(screen, LIGHT_GRAY, (i, LINE_START), (i, LINE_END), 1)
    return None

def draw_grid(screen):
    ''' input:      screen, the display window
        returns:    nothing, but re-renders the display window so that the SOLVING_GRID shows up
    '''
    draw_board(screen)
    # print(SOLVING_GRID)
    for i in range(9):
        for j in range(9):
            if SOLVING_GRID[j][i] != BLANK_SPACE:
                try:
                    num = int(SOLVING_GRID[j][i])
                    montFont = pygame.font.SysFont('montserratregular', 24)
                    numInBox = montFont.render(str(num), True, BLACK) if GRID[j][i] != 0 else montFont.render(str(num), True, GRAY)
                    numBox = numInBox.get_rect()
                    numBox.center = (i*50 + 50, j*50 + 50)
                    screen.blit(numInBox, numBox)
                    draw_board(screen)
                    pygame.display.update()
                except:
                    pass
                
def clear_board(screen):
    ''' input:      screen, the display window
        returns:    nothing, but re-renders the display window so the initial GRID shows up
    '''
    screen.fill(WHITE)
    draw_board(screen)
    for i in range(9):
        for j in range(9):
            if GRID[j][i] != BLANK_SPACE:
                num = int(GRID[j][i])
                montFont = pygame.font.SysFont('montserratregular', 24)
                numInBox = montFont.render(str(num), True, BLACK)
                numBox = numInBox.get_rect()
                numBox.center = (i*50 + 50, j*50 + 50)
                screen.blit(numInBox, numBox)
                draw_board(screen)
                pygame.display.update()

def check_grid():
    ''' input:      None
        returns:    True, if SOLVED_GRID == SOLVING_GRID
                    False, otherwise
    '''
    for i in range(9):
        for j in range(9):
            if GRID_COPY[i][j] != SOLVING_GRID[i][j]:
                return False
    return True
    

def print_instructions(screen):
    font1 = pygame.font.Sysfont('montserratregular', 18)
    instruction1 = font1.render('Press R to reset the board to its initial state.')
    instruction2 = font1.render('Press C to completely clear the board.')
    instruction3 = font1.render('Press SPACE to use the sudoku solver to solve the board.')
    
def main():
    
    pygame.init()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Solver")
    screen.fill(WHITE)
    
    global SOLVING_GRID
    global GRID
    global GRID_COPY
    
    # draw_board(screen)
    draw_grid(screen)
    pygame.display.flip()
    
    done = False
    
    active = False
    
    position1 = (0, 0)
    position2 = (0, 0)
    
    cell_x = 0
    cell_y = 0
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_y >= 25 and mouse_y <= 475 and mouse_x >= 25 and mouse_x <= 475:
                    draw_grid(screen)
                    cell_y = (mouse_y - 25) // SQUARE_SIZE
                    cell_x = (mouse_x - 25) // SQUARE_SIZE
                    position2 = (cell_x, cell_y)
                    # print(position2) # for debugging
                    active = True
                    if GRID[cell_y][cell_x] == BLANK_SPACE:
                        position1 = mouseDown(screen, event, active, cell_x, cell_y, position1)
                    else:
                        pass
            if (event.type == pygame.KEYDOWN):
                # press the ESC key to exit the pygame window
                if event.key == pygame.K_ESCAPE:
                    done = True
                    pygame.quit()
                    return
                # press the SPACE key to have the program solve the puzzle
                if event.key == pygame.K_SPACE:
                    SOLVING_GRID = [row[:] for row in GRID]
                    solveSudokuGraphic(SOLVING_GRID, screen)
                # press the R key to clear the board back to the original GRID
                if event.key == pygame.K_r:
                    SOLVING_GRID = [row[:] for row in GRID]
                    clear_board(screen)
                else:
                    keyDown(screen, event, active, cell_x, cell_y)
        if fullGrid(SOLVING_GRID):
            montFont = pygame.font.SysFont('montserratregular', 24)
            if check_grid():
                draw_board(screen)
                for i in range(9):
                    for j in range(9):
                        num = int(SOLVING_GRID[j][i])
                        numInBox = montFont.render(str(num), True, DARK_GREEN)
                        numBox = numInBox.get_rect()
                        numBox.center = (i*50 + 50, j*50 + 50)
                        screen.blit(numInBox, numBox)
                        draw_board(screen)
                        pygame.display.update()
            else:
                draw_board(screen)
                for i in range(9):
                    for j in range(9):
                        num = int(SOLVING_GRID[j][i])
                        numInBox = montFont.render(str(num), True, BLACK)
                        numBox = numInBox.get_rect()
                        numBox.center = (i*50 + 50, j*50 + 50)
                        screen.blit(numInBox, numBox)
                        if num != GRID_COPY[j][i]:
                            wrong_rectangle = pygame.Rect(i*50 + 31, j*50 + 31, SQUARE_SIZE-10, SQUARE_SIZE-10)
                            pygame.draw.rect(screen, RED, wrong_rectangle, 3)
                        montFont = pygame.font.SysFont('montserratregular', 24)
                        draw_board(screen)
                        pygame.display.update()   

        pygame.display.update()
        CLOCK.tick(FPS)
        
    pygame.time.delay
    
if __name__ == "__main__":
    main()