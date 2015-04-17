'''
Created on 2015. 4. 6.

@author: jaejun

references :
Mathematical Analysis of Tic-Tac-Toe : http://www.mathrec.org/old/2002jan/solutions.html

'''
import sys
from random import randint
import abc
import itertools


EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2
DRAW = 3

PLAYERS_NAMES = [' ', 'X', 'O']
COORDINATES = ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2))

def exitWithError(msg):
    _msg = "Error : %s"%msg
    sys.exit(_msg)

class gridBoard:
    board = []
    last_action = None
    def __init__(self):
        self.board = [[EMPTY for i in range(3)] for j in range(3)]
    
    # player calls this function
    def fillCell(self, s_des, i, j):# tested
        if not s_des in [PLAYER_O, PLAYER_X]:    # only write with 'X', 'O'
            exitWithError("Undefined User")
        if i not in range(3) or j not in range(3):
            exitWithError("Cell index(%d,%d) is out of range"%(i,j))
        if self.board[i][j]!=EMPTY:
            exitWithError("board[%d,%d] is already occupied"%(i,j))

        self.last_action = [i, j, s_des]
        self.board[i][j] = s_des

    def undo(self):
        if self.last_action:
            self.board[self.last_action[0]][self.last_action[1]] = EMPTY

    def drawBoardState(self):# tested
        print '-'*10
        for row in self.board:
            print chr(124),
            for cell in row:
                print PLAYERS_NAMES[cell]+chr(124),
            print '\n',
        print '-'*10

    # return entire grid board in tuple
    # return in tuple because list is not hashable type
    def getState(self):
        return tuple(self.board[0]), tuple(self.board[1]), tuple(self.board[2])


    # return a list of tuples which consists of index of available cells
    def getEmpty(self):
        remains = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    remains.append((i,j))
        return remains   

    def isEmpty(self, i, j):
        return self.board[i][j] == EMPTY

    # 
    def isGameOver(self):
        for i in range(3):
            # check rows
            if self.board[i][0]!=EMPTY and self.board[i][1]==self.board[i][0] and self.board[i][2]==self.board[i][0]:
                return self.board[i][0]
            # check columns
            if self.board[0][i]!=EMPTY and self.board[1][i]==self.board[0][i] and self.board[2][i]==self.board[0][i]:
                return self.board[0][i]
        
        # check diagonals
        if self.board[0][0]!=EMPTY and self.board[1][1]==self.board[0][0] and self.board[2][2]==self.board[0][0]:
            return self.board[0][0]
        if self.board[0][2]!=EMPTY and self.board[1][1]==self.board[0][2] and self.board[2][0]==self.board[0][2]:
            return self.board[0][0]
        
        # check if grid board is full
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    return EMPTY
        return DRAW

"""
GameAgent is ABSTRACT CLASS
I found two methods for creating abstract class.

1. http://stackoverflow.com/questions/372042/difference-between-abstract-class-and-interface-in-python
    raise NotImplementedError("[play] method of GameAgent must be implemented.")
2. use abc package
    http://stackoverflow.com/questions/4382945/abstract-methods-in-python
    http://pymotw.com/2/abc/
"""
class GameAgent(object):
    __metaclass__ = abc.ABCMeta

    player_type = EMPTY
    def __init__(self, player_type):
        self.player_type = player_type
        print '%c type GameAgent'%PLAYERS_NAMES[player_type]
    
    def checkBoardObject(self, board):
        # you have to give gridBoard object
        if not isinstance(board, gridBoard):
            exitWithError("You can give only gridBoard object to the Agent")
    
    def randomPlay(self, board):         
        empties = board.getEmpty()  # get currently available cells
        if len(empties) > 1:
            idx = empties[randint(0, len(empties)-1)] # randomly choose one cell
        else:
            idx = empties[0]
        board.fillCell(self.player_type, idx[0], idx[1]) # conduct

    """
    play

    You have to implement this method in a class which is inherited from GameAgent.
    Implementation changes depending on the kinds of agent.

    RandomAgent :
        Implement with purely random selection of grid position.
    HumanAgent :
        Require user a coordinate of grid position and do the play as it.
    LearningAgent :
        Mixture of policy iteration and random play.
        Random play for exploration.
        Policty Iteration for exploitation.
    """
    @abc.abstractmethod
    def play(self, board):
        return

    """
    report

    You have to implement this method in a class which is inherited from GameAgent.
    Implementation changes depending on the kinds of agent.

    RandomAgent, HumanAgent:
        Report the result.

    LearningAgent :
        Report the result.
        Additionally you have to implement learning algorithm.
    """
    def report(self, result):
        return

# x_comb : (1,4,6) y_comb : (2,3,5)
def validate_board_layout(x_comb = None, y_comb = None):
    board = [[EMPTY for _1 in range(3)] for _2 in range(3)]
    if x_comb:
        for x in x_comb:
            board[COORDINATES[x][0]][COORDINATES[x][1]] = PLAYER_X

    if y_comb:
        for y in y_comb:
            board[COORDINATES[y][0]][COORDINATES[y][1]] = PLAYER_O

class board_validation(object):
    validate_func = None
    def __init__(self):
        self.validate_func = (self.case0, self.case1, self.case2, self.case3, self.case4,
                              self.case5, self.case6, self.case7, self.case8, self.case9)

    def get_empty_board(self, as_tuple=False):
        if as_tuple:
            return ((EMPTY for _1 in range(3)) for _2 in range(3))
        return [[EMPTY for _1 in range(3)] for _2 in range(3)]

    def convert_tuple_to_board(self, x_comb, o_comb):
        board = self.get_empty_board()
        if x_comb:
            for x in x_comb:
                board[COORDINATES[x][0]][COORDINATES[x][1]] = PLAYER_X
        if o_comb:
            for o in o_comb:
                board[COORDINATES[o][0]][COORDINATES[o][1]] = PLAYER_O

        return tuple(board[0]), tuple(board[1]), tuple(board[2])

    def test_winner(self, board, target):
        for i in range(3):
            # check rows
            if board[i][0]==target and board[i][1]==board[i][0] and board[i][2]==board[i][0]:
                return True
            # check columns
            if board[0][i]==target and board[1][i]==board[0][i] and board[2][i]==board[0][i]:
                return True

        # check diagonals
        if board[0][0]==target and board[1][1]==board[0][0] and board[2][2]==board[0][0]:
            return True
        if board[0][2]==target and board[1][1]==board[0][2] and board[2][0]==board[0][2]:
            return True
        return False

    def test(self, board, n_moves):
        return self.validate_func[n_moves](board)

    def case0(self, board):
        return True

    def case1(self, board):
        return True

    def case2(self, board):
        return True

    def case3(self, board):
        return True

    def case4(self, board):
        return True

    def case5(self, board):
        return True

    def case6(self, board):
        # when there are 7 moves, player_x(starter) cannot win
        return not self.test_winner(board, PLAYER_X)

    def case7(self, board):
        # when there are 7 moves, player_o cannot win
        return not self.test_winner(board, PLAYER_O)

    def case8(self, board):
        # when there are 8 moves, player_x(starter) cannot win
        return not self.test_winner(board, PLAYER_X)

    def case9(self, board):
        # when there are 9 moves, player_o cannot win
        return not self.test_winner(board, PLAYER_O)



class LearningAgent(GameAgent):
    values = {}

    def __init__(self, player_type):
        super(LearningAgent, self).__init__(player_type)
        validator = board_validation()

        self.values[validator.get_empty_board(as_tuple=True)] = 0.0

        for k in range(1, 10):  #TODO: routine for setting up values of winning, loose, draw depending on self.player_type
            if k % 2:
                n_px = (k-1) / 2 + 1
            else:
                n_px = k / 2
            n_po = k - n_px
            cnt = 0
            cnt_invalid = 0
            for comb in itertools.combinations(range(9), k):
                for x_comb in itertools.combinations(comb, n_px):
                    o_comb = tuple(o for o in comb if o not in x_comb)
                    board = validator.convert_tuple_to_board(x_comb, o_comb)
                    if validator.test(board, k):
                        self.values[board] = 0.5
                        cnt = cnt + 1
                    else:
                        cnt_invalid = cnt_invalid + 1

            print "%d: %d\t\t%d"%(k, cnt, cnt_invalid)
        print 'Size of state space is %d' % len(self.values) # number of possible board layout

    def play(self, board):
        self.checkBoardObject(board)

    def report(self, result):
        return

    
class RandomAgent(GameAgent):
    def __init__(self, player_type):
        super(RandomAgent, self).__init__(player_type)
        print 'init RandomAgent'
        
    def play(self, board):
        self.checkBoardObject(board)
        self.randomPlay(board)

    def report(self, result):
        return
    
class HumanAgent(GameAgent):
    def __init__(self, player_type):
        super(HumanAgent, self).__init__(player_type)
        print 'init HumanAgent'
    
    def play(self, board):
        self.checkBoardObject(board)
        board.drawBoardState()
        while True:
            input = raw_input('Where do you want to take? ex) 1,0 ').split(',')
            if not board.isEmpty(int(input[0]), int(input[1])):
                continue
            board.fillCell(self.player_type, int(input[0]), int(input[1]))
            break

        def report(self, result):
            return
        
class Game:
    player_x = None
    player_o = None
    grid_board = None
    def __init__(self, _player_x, _player_o):
        print 'init Game'
        self.player_x = _player_x
        self.player_o = _player_o
        self.grid_board = gridBoard()

    def startGame(self):
        # play single game
        # if game state becomes one of [DRAW, PLAYER_O, PLAYER_X], iteration will stops.
        for i in range(9):
            self.player_x.play(self.grid_board)
            self.grid_board.drawBoardState()
            if self.grid_board.isGameOver() is not EMPTY:
                break
            self.player_o.play(self.grid_board)
            self.grid_board.drawBoardState()
            if self.grid_board.isGameOver() is not EMPTY:
                break

        # report the result to the players
        result = self.grid_board.isGameOver()

        if result in [PLAYER_X, PLAYER_O]:
            print "Winner : Player " + PLAYERS_NAMES[result]
        else:
            print "Game DRAW"

        self.player_x.report(result)
        self.player_o.report(result)

if __name__ == "__main__":
    board = gridBoard()
    agent1 = LearningAgent(PLAYER_X)
    agent2 = RandomAgent(PLAYER_O)
    # game = Game(agent1, agent2)
    # game.startGame()

