from typing import SupportsComplex
import numpy as np
import copy


def getInitialBoard():
    board = np.zeros(shape=(8,8))

    board[0][1] = 2
    board[0][3] = 2
    board[0][5] = 2
    board[0][7] = 2

    board[1][0] = 2
    board[1][2] = 2
    board[1][4] = 2
    board[1][6] = 2

    board[2][1] = 2
    board[2][3] = 2
    board[2][5] = 2
    board[2][7] = 2


    board[5][0] = 1
    board[5][2] = 1
    board[5][4] = 1
    board[5][6] = 1

    board[6][1] = 1
    board[6][3] = 1
    board[6][5] = 1
    board[6][7] = 1

    board[7][0] = 1
    board[7][2] = 1
    board[7][4] = 1
    board[7][6] = 1

    return board

'''
kings are presented as 4 for 2
and 3 for 1
black is 1
'''

def gameIsSolved(board):
    sum2=0
    sum1=0
    for x in board:
        for y in x:
            if y==1 or y==3:
                sum1+=1
            elif y==2 or y==4:
                sum2+=1
    
    if sum1==0:
        return True
    elif sum2==0:
        return True
    else:
        return False
    pass


'''
This function only checks for blanks
still havent reached more into it
'''
def getPossibleMoves(player,board):
    board = copy.deepcopy(board)

    if player==2:
        # we know that this is player 2, and we check the upper board with different kinds of bounds
        for x in range(8):
            for y in range(8):
                # without queens or kings whatever
                if board[x][y] == player:
                    # now we check Diagonal bounds

                    # this is the left bound
                    print("we are currently in", x, y, ", this is player: ", player)
                    if isItBeingBlocked(x,y,board,"LEFT",player):
                        print("left bound okay")

                    if isItBeingBlocked(x,y,board,"RIGHT",player):
                        print("right bound okay")
                    print
    elif player==1:
        for x in range(8):
            for y in range(8):
                # without queens or kings whatever
                if board[x][y] == player:
                    # now we check Diagonal bounds

                    # this is the left bound
                    print("we are currently in", x, y, ", this is player: ", player)
                    if isItBeingBlocked(x,y,board,"LEFT",player):
                        print("left bound okay")

                    # right bound 
                    if isItBeingBlocked(x,y,board,"RIGHT",player):
                        print("right bound okay")
                    print

    pass


def isAttackAvailable(i,j,board,player):
        
    pass

def isItInBounds(i,j):
    if i>=0 and i<=7:
        if j>=0 and j<=7:
            return True
    return False
    pass


'''
i and j is used for the current checker piece and directions sets where to look for
'''
def isItBeingBlocked(i,j,board, direction, player):
    if player==2:
        if direction=="LEFT":
            if isItInBounds(i+1,j-1):
                if (0 == board[i+1][j-1]):
                    return True
        elif direction=="RIGHT":
                if isItInBounds(i+1,j+1):
                    if (0 == board[i+1][j+1]):
                        return True

    if player==1:
            if direction=="LEFT":
                if isItInBounds(i-1,j-1):
                    if (0 == board[i-1][j-1]):
                        return True
            elif direction=="RIGHT":
                    if isItInBounds(i-1,j+1):
                        if (0 == board[i-1][j+1]):
                            return True
    return False
    pass

def startGame(board):
    player = 1
    while(True):
        print(board)



        break
        

        if (gameIsSolved(board)):
            print



if __name__ == "__main__":
    board = getInitialBoard()
    print(board)

    #startGame(board)

    '''board = np.zeros(shape=(8,8))

    board[0][1] = 2
    board[1][0] = 2
    board[1][2] = 2
    print(board)'''
    getPossibleMoves(1,board)
