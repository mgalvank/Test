#Naive method"
#Considering input parameters check for each row col if placing the piece there is safe. If yes place other wise move to next row col"

import copy
import sys

def checkRow(board,row,col,cpu,k):
    temp_board = copy.deepcopy(board)
    temp_board[row][col] = cpu
    count = 0
    # print "row temp board", temp_board
    for i in range(0,N):
        # print "i",i
        if temp_board[row][i] == cpu:
            # print "i in if",i
            # print "item at row",temp_board[row][i]
            count = count + 1
    # print "row count in checkRow",count
    if count == k:
        return False
    else: return True


def checkCol(board,row,col,cpu,k):
    temp_board = copy.deepcopy(board)
    temp_board[row][col] = cpu
    # print "col temp board",temp_board
    count = 0
    for i in range(0,N):
        if temp_board[i][col] == cpu:
            count = count + 1
    if count == k:
        return False
    else: return True

def get_diagonal_count(board, row, col, dir,cpu):
    temp_board = copy.deepcopy(board)
    temp_board[row][col] = cpu
    diagonal = []
    for c in range(0, N):
        r = row - col*dir + c*dir
        if r >= 0 and r < N:
            diagonal.append(temp_board[r][c])
    return diagonal

def checkDiagonal(board,row,col,cpu,k):
    diagonal = get_diagonal_count(board,row,col,1,cpu)
    # print "diagonal", diagonal
    antidiagonal = get_diagonal_count(board,row,col,-1,cpu)
    # print "antidiagonal", antidiagonal
    countd = 0
    countad = 0
    for i in diagonal:
        if i == cpu:
            countd = countd + 1
    # print "countd",countd
    # print "len of diagonal",len(diagonal)
    for i in antidiagonal:
        if i == cpu:
            countad = countad + 1

    if countd == k:
        # print "inside if countd = diagonal"
        return False
    elif countad == k:
        return False
    else :
        # print "Inside else of checkdiagonal"
        return True


def isSafe(board,row,col,cpu,k):
    if board[row][col]!= '.':
        # print "Tile already filled"
        pass

    elif checkRow(board,row,col,cpu,k)==True and checkCol(board,row,col,cpu,k)== True and checkDiagonal(board,row,col,cpu,k) == True:
        return True
    else: return False

    return False

def check_whos_move(board):
    w = 0
    b = 0
    for i in board:
        for j in i:
            if j == "w":
                w += 1
            elif j == "b":
                b += 1
    # print "w count", w
    # print "b count", b
    if w == b:
        return "w"
    elif w>b:
        return "b"
    else : return "w"

def find_nextMove(board,cpu,k):
    for i in range(0,N):
        for j in range(0,N):
            if isSafe(board,i,j,cpu,k):
                board[i][j] = cpu
                return (board,i,j)

    for i in range(0,N):
        for j in range(0,N):
            if board[i][j]==".":
                board[i][j] = cpu
                return (board,i,j)



def displayboard(board,solution_row,solution_col):
    print "Hmm, I'd recommend putting your marble at row %s, column %s." %(solution_row+1,solution_col+1)
    print "New board :"
    # for i in board:
    #     print i
    board_string = "".join("".join(map(str,l)) for l in board)
    print board_string




(n, k, input_string,time_parameter) = sys.argv[1:5]
# N = 3
# K = 3
N = int(n)
K = int(k)
# input_string1 = ""+input_string
# print "input string1",input_string1
# print "N",N
# print "n,k, input_string",(N,K,input_string)
# default_board = [['.' for count in range(N)] for count in range(N) ]
# default_board = [['w', '.', 'w'], ['b', 'w', 'b'], ['b', 'w', 'b']]
# input_string = ".w......b"
# input_string = "bwbwb.wb."
board = [list(input_string[i:i+int(N)]) for i in range(0, len(input_string), int(N))]
cpu = check_whos_move(board)
# print "Next move of ", cpu
# print default_board
solution = find_nextMove(board,cpu,K)
board = solution[0]
solution_row = solution[1]
solution_col = solution[2]


#else loop through all the rest of the


# print "board",default_board
if board == 0:
    print "No place found !"
else : displayboard(board,solution_row,solution_col)







