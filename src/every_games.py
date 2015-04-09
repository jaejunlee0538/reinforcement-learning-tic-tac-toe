'''
Created on 2015. 4. 6.

@author: jaejun
'''
import sys
from random import randint

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
        
class GameAgent(object):
    player_type = EMPTY
    def __init__(self, player_type):
        self.player_type = player_type
        print '%c type GameAgent'%PLAYERS_NAMES[player_type]
    
    def checkBoardObject(self, board):
        # you have to give gridBoard object
        if not isinstance(board, gridBoard):
            exitWithError("You can give gridBoard object to the Agent")
    
    def randomPlay(self, board):         
        empties = board.getEmpty()  # get currently available cells 
        idx = empties[randint(0,len(empties)-1)] # randomly choose one cell 
        board.fillCell(self.player_type, idx[0], idx[1]) # conduct
    
    def play(self, board):
        print 'You have to implement this'

class LearningAgent(GameAgent):
    def __init__(self, player_type):
        super(LearningAgent, self).__init__(player_type)
        print 'learning Agent'
    
class RandomAgent(GameAgent):
    def __init__(self, player_type):
        super(RandomAgent, self).__init__(player_type)
        print 'init RandomAgent'
        
    def play(self, board):
        self.checkBoardObject(board)
        self.randomPlay(board)
    
    
class HumanAgent(GameAgent):
    def __init__(self, player_type):
        super(HumanAgent, self).__init__(player_type)
        print 'init HumanAgent'
    
    def play(self, board):
        self.checkBoardObject(board)
        board.drawBoardState()
        input = raw_input('Where do you want to take? ex) 1,0 ').split(',')
        board.fillCell(self.player_type, int(input[0]), int(input[1]))
        
        
class Game:
    def __init__(self):
        print 'init Game'


if __name__ == "__main__":
    board = gridBoard()
    explorer = RandomAgent(PLAYER_O)
    human = HumanAgent(PLAYER_X)
    
    explorer.play(board)
    board.drawBoardState()
    human.play(board)
    board.drawBoardState()
    explorer.play(board)
    board.drawBoardState()
    human.play(board)
    board.drawBoardState()
    
    print 'Learning with Random Agent'
    
   
    print 'Play game with human'
    

