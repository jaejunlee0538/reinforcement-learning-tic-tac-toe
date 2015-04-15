'''
Created on 2015. 4. 6.

@author: jaejun
'''
import sys
from random import randint
import abc


EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2
DRAW = 3

PLAYERS_NAMES = [' ', 'X', 'O']

def exitWithError(msg):
    _msg = "Error : %s"%msg
    sys.exit(_msg)

class gridBoard:
    board = []
       
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
        
        self.board[i][j] = s_des

    def drawBoardState(self):# tested
        print '-'*10
        for row in self.board:
            print chr(124),
            for cell in row:
                print PLAYERS_NAMES[cell]+chr(124),
            print '\n',
        print '-'*10
    
    # return entire grid board
    def getState(self):
        return self.board   
    
    # return a list of tuples which consists of index of available cells
    def getEmpty(self):
        remains = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j]==EMPTY:
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


    # def repeatTheResult(self, result):
    #     msg = ""
    #     if result is self.player_type:
    #         msg = "player " + PLAYERS_NAMES[self.player_type] + " Win!!!"
    #     elif result is DRAW:
    #         msg = "Game Draw"
    #     else:
    #         msg = "player " + PLAYERS_NAMES[self.player_type] + " Loose..."
    #
    #     print msg


class LearningAgent(GameAgent):
    def __init__(self, player_type):
        super(LearningAgent, self).__init__(player_type)
        print 'learning Agent'

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
    agent1 = RandomAgent(PLAYER_X)
    agent2 = RandomAgent(PLAYER_O)
    game = Game(agent1, agent2)
    game.startGame()

