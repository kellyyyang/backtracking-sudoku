# the blank space character
blankSpace = 0

def printBoard(board):
    ''' input:      board, a 9 x 9 two-dimensional array
        returns:    None, but prints the board
    '''
    for i in range(len(board)):
        for j in range(len(board)):
            print(str(board[i][j]) + ' ', end='')
        print('\n', end='')

def isValidSudoku(board):    
    ''' input:      board, a 9 x 9 array
        returns:    True, if the current board is valid
                    False, otherwise
    '''
    def valid(arr):
        ''' input:      arr, a one-dimensional array
            returns:    True, if the array does not contain more than one of each integer from 1 to 9
                        False, otherwise
        '''
        nums = [x for x in arr if x != '.']
        numsSet = set(nums)
        if len(numsSet) != len(nums):
            return False
        else:
            return True
        
    for row in board:
        if valid(row) != True:
            return False
    
    for i in range(len(board)):
        col = [board[j][i] for j in range(len(board))]
        if valid(col) == False:
            return False
    
    for i in range(0, len(board), 3):
        rectangle = board[i:i+3]
        for j in range(0, len(board), 3):
            square = [x[j:j+3] for x in rectangle]
            square1 = sum(square, [])
            if valid(square1) == False:
                return False
    
    return True

def valid(arr):
    ''' input:      arr, a one-dimensional array
        returns:    True, if the array does not contain more than one of each integer from 1 to 9
                    False, otherwise
    '''
    nums = [x for x in arr if x != blankSpace]
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
            if board[i][j] == blankSpace:
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
    if board[row][col] == blankSpace:
        return [True, row, col]
    else:
        for i in range(row, len(board)):
            for j in range(col, len(board)):
                if board[i][j] == blankSpace:
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
        # else:
        #     board[row][col] = blankSpace
    board[row][col] = blankSpace
    return False

grid =  [[3, 1, 6, 5, 0, 8, 4, 0, 0],
        [5, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]]

grid2 =  [[3, 0, 6, 5, 0, 8, 4, 0, 0],
          [5, 2, 0, 0, 0, 0, 0, 0, 0],
          [0, 8, 7, 0, 0, 0, 0, 3, 1],
          [0, 0, 3, 0, 1, 0, 0, 8, 0],
          [9, 0, 0, 8, 6, 3, 0, 0, 5],
          [0, 5, 0, 0, 9, 0, 6, 0, 0],
          [1, 3, 0, 0, 0, 0, 2, 5, 0],
          [0, 0, 0, 0, 0, 0, 0, 7, 4],
          [0, 0, 5, 2, 0, 6, 3, 0, 0]]