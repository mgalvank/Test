# Simple tetris program! v0.2
# D. Crandall, Sept 2016

from AnimatedTetris import *
from SimpleTetris import *
from kbinput import *
import time, sys
import copy
import Queue




class HumanPlayer:
    def get_moves(self, tetris):
        print "Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\nThen press enter. E.g.: bbbnn\n"
        moves = raw_input()
        return moves

    def control_game(self, tetris):
        while 1:
            c = get_char_keyboard()
            commands = {"b": tetris.left, "n": tetris.rotate, "m": tetris.right, " ": tetris.down}
            commands[c]()


#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. tetris is an object that lets you inspect the board, e.g.:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #

    #Input parameter - state_config is a list containing the best col position for current piece and the best rotation for current piece
    def get_config_string(self,state_config):
        col1 = state_config[1]
        rotation = state_config[2]
        final_config = []
        k = 0

        #calculated how many times to rotate the current piece. 0 - 0, 1 - 90,2- 180,3 - 270
        while k == 0:
            if rotation == 0:
                k = 1
            elif rotation == 1:
                final_config.append("n")
                k = 1
            elif rotation == 2:
                final_config.append("nn")
                k = 1
            elif rotation == 3:
                final_config.append("nnn")
                k = 1

        #get current piece column
        tetris_col = tetris.col
        #calculated how many times to move the current piece to left or right depending on the best col position that we recieved from input
        #paramet
        g = 0
        while g == 0:
            if (col1 < tetris_col):
                final_config.append("b")
                tetris_col -= 1
            elif (col1 > tetris_col):
                final_config.append("m")
                tetris_col += 1
            else:
                g = 1

        # print "final string ",final_config
        #concatenate the list into a string
        final_config_string = ''.join(final_config)
        print "final string 1", final_config_string
        # raw_input()

        #return final set of moves required to place the current piece in the best position
        return final_config_string


    #calculated heuristic.
    #input parameter - a tetris object
    #grab the board from the input object
    #iterate through the board to find various parameters necessary to calculate height
    #parameters - aggregate height,holes, smpty cells, trenches,cleared lines
    def calculate_heuristic(self,heutetris):
        heuristic1 = 0
        state_board = heutetris.get_board()


        #Calculate aggregate col height for the given state object board
        #Used Prof crandall's code to retrieve column heights then tweaked it as per my need.
        column_heights = [
            min([r for r in range(len(state_board[0]) - 1, 0, -1) if state_board[r][c] == "x"] + [100, ]) for c
            in range(0, len(state_board[0]))]
        column_heights_updated = []
        for i in column_heights:
            if i == 100:
                each_col_height = 0
            else:
                each_col_height = 20 - i
            column_heights_updated.append(each_col_height)

        aggre_col_height = sum(column_heights_updated)

        # check for holes
        # if a block in board is empty check above it. it there's a piece , count it as a hole.
        holes = 0
        holes = 0
        for row in range(19, 0, -1):
            for col in range(0, 10):
                if state_board[row][col] == " " and state_board[row - 1][col] == 'x':
                    holes += 1

        # check for trench
        # sum of the abs diff between all the adjacent columns
        trench_list = []
        for i in range(0, len(column_heights_updated) - 1):
            s = abs(column_heights_updated[i] - column_heights_updated[i + 1])
            trench_list.append(s)
        trench = sum(trench_list)

        # check for complete lines - naive way
        row_cleared = 0
        for row in range(19, 0, -1):
            filled = 0
            for col in range(0, 10):
                if state_board[row][col] == 'x':
                    filled += 1
            if filled == 10:
                row_cleared += 1

        #Calculate special empty cells to the left, middle and right of the board
        # 1. An empty cell to the left of a column in which the topmost cell is at the
        # same height or above the empty cell in question.
        # 2. An empty cell under the topmost filled cell in the same column.
        # 3. An empty cell to the right of a column in which the topmost cell is at the
        # same height or above the empty cell in question.
        # References : - http://www.diva-portal.org/smash/get/diva2:815662/FULLTEXT01.pdf
        state_piece = copy.deepcopy(heutetris.get_piece())
        for col in range(0, 10):
            for row in range(len(state_piece[0]), 20):
                if state_board[row][col] == ' ':
                    if col != 0:
                        if state_board[row][col - 1] == 'x':
                            heuristic1 += (20 - row)
                        elif state_board[row][col] == 'x':
                            heuristic1 += (20 - row)
                if state_board[row][col] == ' ':
                    if state_board[row - 1][col] == 'x':
                        heuristic1 += (20 - row) ** 2
                if state_board[row][col] == ' ':
                    if col != 9:
                        if state_board[row][col + 1] == 'x':
                            heuristic1 += (20 - row)
                        elif state_board[row][col] == 'x':
                            heuristic1 += (20 - row)


        # print "aggre height", aggre_col_height
        # print "row cleared", row_cleared
        # print "holes", holes
        # print "trench", trench


        # calculate heuristic
        # a *(Aggregate Height) + b * (Complete Lines) + c *(Holes) + d *(trench)
        # Reference : - https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
        heuristic2 = (-0.5100666 * aggre_col_height) + (0.760666 * row_cleared) + (-0.35663 * holes) + (-0.184483 * trench)
        heuristic3 = heuristic1 * 2 + heuristic2

        return (heuristic1,heuristic3)


    def get_moves(self, tetris):

        next_piece_heuristic = 0
        temp_heu_state = []
        current_piece_heuristic = 0
        heuristic_for_states = []
        newtetris = copy.deepcopy(tetris)
        board = copy.deepcopy(newtetris.get_board())
        current_piece = copy.deepcopy(newtetris.get_piece())
        next_piece = copy.deepcopy(newtetris.get_next_piece())
        current_piece_rotations = []
        next_piece_rotations = []
        possible_state_with_heuristic = Queue.PriorityQueue()

        rotation_angles = [90, 180, 270]
        # calculate all possible rotations for current piece and append it to a list
        current_piece_rotations.append(copy.deepcopy(current_piece)[0])
        for i in rotation_angles:
            current_piece_rotations.append(TetrisGame.rotate_piece(current_piece[0], i))

        # calculate all possible rotations for next piece and append it to a list
        next_piece_rotations.append(copy.deepcopy(next_piece))
        for i in rotation_angles:
            next_piece_rotations.append(TetrisGame.rotate_piece(next_piece, i))

        # print "next piece rotations",next_piece_rotations

        #Iterating through all the current piece possible rotations
        for piece in current_piece_rotations:
            #Iterating through the board and placing piece on each possible position
            for col_main in range(0,11 - len(piece[0])):
                current_piece_heuristic = 0
                #Created a new tetris object to find the best position for current piece
                temptetris = copy.deepcopy(tetris)
                temptetris_piece = copy.deepcopy(temptetris.get_piece())
                # print "temptetris",temptetris_piece
                temptetris_piece_col = temptetris_piece[2]
                temptetris.piece = copy.deepcopy(piece)
                n = 0
                #Move the piece left or right till it reaches the desired position
                while (n == 0):
                    if (col_main < temptetris_piece_col):
                        temptetris.left()
                        temptetris_piece_col -= 1
                    elif (col_main > temptetris_piece_col):
                        temptetris.right()
                        temptetris_piece_col += 1
                    else:
                        #Code for breaking for some reason, hence added a argument parameter to .down() to make program differentiate
                        #between temp down calls and real down calls.
                        temptetris.down("heu")
                        current_state_board = copy.deepcopy(temptetris.get_board())
                        # print "state_board in for loop"
                        # for i in current_state_board:
                        #     print i
                        current_piece_heuristic = self.calculate_heuristic(copy.deepcopy(temptetris))
                        # print "current heuristic,col,rotation_index",(current_piece_heuristic,col_main,current_piece_rotations.index(piece))
                        n = 1

                #Iterate through all the pieces in the next_piece possible rotations and calculate heuristic for each possible
                #state on the board
                for next_piece in next_piece_rotations:
                    for col in range(0, 10 - len(next_piece[0])):
                        next_piece_heuristic = 0
                        temp_heu_state[:] = []
                        temptetris1 = copy.deepcopy(temptetris)
                        temptetris_piece1 = copy.deepcopy(temptetris1.get_piece())
                        temptetris_piece_col1 = temptetris_piece1[2]
                        temptetris.piece = copy.deepcopy(next_piece)
                        d = 0
                        while (d == 0):
                            if (col < temptetris_piece_col1):
                                temptetris1.left()
                                temptetris_piece_col1 -= 1
                            elif (col > temptetris_piece_col1):
                                temptetris1.right()
                                temptetris_piece_col1 += 1
                            else:
                                temptetris1.down("heu")
                                next_state_board = copy.deepcopy(temptetris1.get_board())
                                # print "state_board in for loop"
                                # for i in next_state_board:
                                #     print i
                                next_piece_heuristic = self.calculate_heuristic(copy.deepcopy(temptetris1))
                                temp_heu_state.append(current_piece_heuristic + next_piece_heuristic)
                                temp_heu_state.append(col_main)
                                temp_heu_state.append(current_piece_rotations.index(piece))
                                # print "heu for next state",temp_heu_state
                                heuristic_for_states.append(temp_heu_state)
                                # print "heuristic_for_states", heuristic_for_states
                                possible_state_with_heuristic.put((current_piece_heuristic + next_piece_heuristic,col_main,current_piece_rotations.index(piece)))
                                d = 1

                possible_state_with_heuristic.put((current_piece_heuristic[0],col_main,current_piece_rotations.index(piece)))

        #Get best placement
        best_placement = possible_state_with_heuristic.get()

        #Generate set of moves to place the current piece
        final_config_string = copy.deepcopy(self.get_config_string(best_placement))

        return final_config_string

        # return random.choice("mnb") * random.randint(1, 10)




    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "tetris" object to control the movement. In particular:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, tetris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            board = tetris.get_board()
            column_heights = [min([r for r in range(len(board) - 1, 0, -1) if board[r][c] == "x"] + [100, ]) for c in
                              range(0, len(board[0]))]
            index = column_heights.index(max(column_heights))

            if (index < tetris.col):
                tetris.left()
            elif (index > tetris.col):
                tetris.right()
            else:
                tetris.down()


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]
# player_opt = "computer"
# interface_opt = "simple"

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print "unknown player!"

    if interface_opt == "simple":
        tetris = SimpleTetris()
    elif interface_opt == "animated":
        tetris = AnimatedTetris()
    else:
        print "unknown interface!"

    tetris.start_game(player)

except EndOfGame as s:
    print "\n\n\n", s



