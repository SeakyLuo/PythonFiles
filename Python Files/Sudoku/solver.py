def solve(board):
    for i in range(1, 10):
        for j in range(1, 10):
            if board[i][j] == '.':
                for c in map(str, range(1, 10)):
                    if isValid(board, i, j, c):
                        board[(i, j)] = c # Put c for this cell
                        if solve(board):
                            return True # If it's the solution return True
                        else
                            board[i][j] = '.' #Otherwise go back
                return False
    return True

def isValid(board, row, col, c):
    check = lambda i: board[i][col] != '.' and board[i][col] == c or # check col
                      board[row][i] != '.' and board[row][i] == c or # check row
                      board[3 * (row / 3) + i / 3][ 3 * (col / 3) + i % 3] != '.' and
                      board[3 * (row / 3) + i / 3][3 * (col / 3) + i % 3] == c # check block
    return all(check(i) for i in range(1, 10))