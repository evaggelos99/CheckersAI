import numpy as np
import copy
import math
import time
import random
import matplotlib.pyplot as plt

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

def evaluationFun(board,player):
    val,play=gameIsSolved(board)
    lengthTwo = np.count_nonzero(board == 2)
    lengthOne = np.count_nonzero(board == 1)
    if player==1:
        if val and play==2:
            return -100 
        elif val and play==1:
            return +100
        else:
            return lengthOne-lengthTwo
    if player==2:
        if val and play==2:
            return +100
        elif val and play==1:
            return -100
        else:
            return lengthTwo-lengthOne


    

def isAttackValid(i,j,board,player,dir):
    if player==1:
        if dir=="LEFT":
            if isItInBounds(i-2,j-2) and board[i-2][j-2]==0:
                return True
        if dir=="RIGHT":
            if isItInBounds(i-2,j+2) and board[i-2][j+2]==0:
                return True
        pass
    elif player==2:
        if dir=="LEFT":
            if isItInBounds(i+2,j-2) and board[i+2][j-2]==0:
                return True
        if dir=="RIGHT":
            if isItInBounds(i+2,j+2) and board[i+2][j+2]==0:
                return True


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
        return True,1
    elif sum2==0:
        return True,2
    else:
        return False,None
    pass


'''
This function only checks for blanks
still havent reached more into it
'''
def getPossibleMoves(player,board):
    copyBoard = copy.deepcopy(board)
    moves = []
    
    if player==2:
        # we know that this is player 2, and we check the upper board with different kinds of bounds
        for x in range(8):
            for y in range(8):
                # without queens or kings whatever
                if board[x][y] == 2:
                    # if we have an attack availalble
                    if isAttackAvailable(x,y,board,2) !=[]:
                        listOfDirection = whereIsTheAttack(x,y,board,2)
                        if listOfDirection!=[]:
                            for direction in listOfDirection:
                                if direction=="LEFT":
                                    # we know that we can jump there so we check if there is another attack there
                                    # manipulate the board
                                    newBoard = copy.deepcopy(copyBoard)
                                    newBoard[x][y]=0
                                    newBoard[x+1][y-1]=0
                                    newBoard[x+2][y-2]=2
                                    newX,newY = x+2,y-2
                                    if isAttackAvailable(x+2,y-2,newBoard,2) != []:
                                        newListOfDirection = whereIsTheAttack(x+2,y-2,newBoard,2)
                                        if newListOfDirection!=[]:
                                            for direction in newListOfDirection:
                                                if direction=="LEFT":
                                                    newBoard[newX][newY]=0
                                                    newBoard[newX+1][newY-1]=0
                                                    newBoard[newX+2][newY-2]=2
                                                    moves.append(copy.deepcopy(newBoard))
                                                else:
                                                    newBoard[newX][newY]=0
                                                    newBoard[newX+1][newY+1]=0
                                                    newBoard[newX+2][newY+2]=2
                                                    moves.append(copy.deepcopy(newBoard))
                                    else:
                                        moves.append(copy.deepcopy(newBoard))
                                else:
                                    # right
                                    
                                    newBoard = copy.deepcopy(copyBoard)
                                    newBoard[x][y]=0
                                    newBoard[x+1][y+1]=0
                                    newBoard[x+2][y+2]=2
                                    newX,newY = x+2,y+2
                                    if isAttackAvailable(x+2,y+2,newBoard,2) != []:
                                        newListOfDirection = whereIsTheAttack(x+2,y+2,newBoard,2)
                                        if newListOfDirection!=[]:
                                            for direction in newListOfDirection:
                                                if direction=="LEFT":
                                                    newBoard[newX][newY]=0
                                                    newBoard[newX+1][newY-1]=0
                                                    newBoard[newX+2][newY-2]=2
                                                    moves.append(copy.deepcopy(newBoard))
                                                else:
                                                    newBoard[newX][newY]=0
                                                    newBoard[newX+1][newY+1]=0
                                                    newBoard[newX+2][newY+2]=2
                                                    moves.append(copy.deepcopy(newBoard))
                                    else:
                                        moves.append(copy.deepcopy(newBoard))
                    # no attack simple move
                    else:
                        # left
                        
                        if isItInBounds(x+1,y-1) and board[x+1][y-1]==0:
                            edit = copy.deepcopy(board)
                            edit[x][y]=0
                            edit[x+1][y-1]=2
                            moves.append(edit)
                        # right
                        if isItInBounds(x+1,y+1) and board[x+1][y+1]==0:
                            edit = copy.deepcopy(board)
                            edit[x][y]=0
                            edit[x+1][y+1]=2
                            moves.append(edit)
    elif player==1:   
        for x in range(8):
            for y in range(8):
                # without queens or kings whatever   
                if board[x][y] == 1:
                    if isAttackAvailable(x,y,board,1) !=[]:
                        listOfDirection = whereIsTheAttack(x,y,board,1)
                        if listOfDirection!=[]:
                            for direction in listOfDirection:
                                if direction=="LEFT":
                                    # we know that we can jump there so we check if there is another attack there
                                    # manipulate the board
                                    newBoard = copy.deepcopy(copyBoard)
                                    newBoard[x][y]=0
                                    newBoard[x-1][y-1]=0
                                    newBoard[x-2][y-2]=1
                                    newX, newY= x-2, y-2
                                    if isAttackAvailable(newX,newY,newBoard,1) != []:
                                        newListOfDirection = whereIsTheAttack(newX,newY,newBoard,1)
                                        if newListOfDirection!=[]:
                                            for direction in newListOfDirection:
                                                if direction=="LEFT":
                                                    newBoard[newX][newY]=0
                                                    newBoard[newX-1][newY-1]=0
                                                    newBoard[newX-2][newY-2]=1
                                                    moves.append(copy.deepcopy(newBoard))
                                                else:
                                                    newBoard[newX][newY]=0
                                                    newBoard[newX-1][newY+1]=0
                                                    newBoard[newX-2][newY+2]=1
                                                    moves.append(copy.deepcopy(newBoard))
                                    else:
                                        moves.append(newBoard)
                                else:
                                    newBoard = copy.deepcopy(copyBoard)
                                    newBoard[x][y]=0
                                    newBoard[x-1][y+1]=0
                                    newBoard[x-2][y+2]=1
                                    newX,newY= x-2,y+2
                                    if isAttackAvailable(x-2,y+2,newBoard,1) != []:
                                        newListOfDirection = whereIsTheAttack(x-2,y-2,newBoard,1)
                                        if newListOfDirection!=[]:
                                            for direction in newListOfDirection:
                                                if direction=="LEFT":
                                                    newBoard[newX][newY]=0
                                                    newBoard[newX-1][newY-1]=0
                                                    newBoard[newX-2][newY-2]=1
                                                    moves.append(copy.deepcopy(newBoard))
                                                else:
                                                    newBoard[newY][newY]=0
                                                    newBoard[newX-1][newY+1]=0
                                                    newBoard[newX-2][newY+2]=1
                                                    moves.append(copy.deepcopy(newBoard))
                                    else:
                                        moves.append(newBoard)
                    # no attack simple move
                    else:
                        # left
                        if isItInBounds(x-1,y-1) and board[x-1][y-1]==0:
                            edit = copy.deepcopy(board)
                            edit[x][y]=0
                            edit[x-1][y-1]=1
                            moves.append(edit)
                        # right
                        if isItInBounds(x-1,y+1) and board[x-1][y+1]==0:
                            edit = copy.deepcopy(board)
                            edit[x][y]=0
                            edit[x-1][y+1]=1
                            moves.append(edit)
    return moves



def isAttackAvailable(i,j,board,player):
    listOfAttackAvailable = []
    if player==1:
        # direction left
        if isItInBounds(i-1, j-1) and board[i-1][j-1]==2  and isItInBounds(i-2,j-2) and board[i-2][j-2]==0:
            listOfAttackAvailable.append((i-1,j-1))
            
            
        # direction right
        if isItInBounds(i-1, j+1) and board[i-1][j+1]==2 and isItInBounds(i-2,j+2) and board[i-2][j+2]==0:
            listOfAttackAvailable.append((i-1,j+1))
            
        
    elif player==2:
        # direction left
        if isItInBounds(i+1,j-1) and board[i+1][j-1]==1  and isItInBounds(i+2,j-2) and board[i+2][j-2]==0:
            listOfAttackAvailable.append((i+1,j-1))
        

        # direction right
        if isItInBounds(i+1, j+1) and board[i+1][j+1]==1 and isItInBounds(i+2,j+2) and board[i+2][j+2]==0:
            listOfAttackAvailable.append((i+1,j+1))
    else:
        return None
    
    return listOfAttackAvailable


'''
This function only checks for the array bounds nothing else
'''
def isItInBounds(i,j):
    if i>=0 and i<=7:
        if j>=0 and j<=7:
            return True
    return False
    pass


def isThereAnAttackOnBoard(board, player):
    for i in range(8):
        for j in range(8):
            if board[i][j]  == 1: # player one
                listOfAttacks=isAttackAvailable(i,j,board,1)
                if listOfAttacks != []:
                    if player == 1:
                        return True
                
            elif board[i][j] == 2: # player two
                listOfAttacks=isAttackAvailable(i,j,board,2)
                if listOfAttacks != []:
                    if player == 2:
                        return True
    
    return []


'''
i and j is used for the current checker piece and directions sets where to look for
'''
def isItClearBounds(i,j,board, direction, player):
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

def whereIsTheAttack(i,j,board, player):
    attacks = []

    if player==2:
        if isItInBounds(i+1,j-1) and board[i+1][j-1] == 1 and isAttackValid(i,j,board,2,"LEFT"):
            attacks.append("LEFT")
        if  isItInBounds(i+1,j+1) and board[i+1][j+1]==1 and isAttackValid(i,j,board,2,"RIGHT"):
            attacks.append("RIGHT")
        return attacks
    elif player==1:
            if isItInBounds(i-1,j-1) and 2 == board[i-1][j-1] and isAttackValid(i,j,board,1,"LEFT"):
                attacks.append("LEFT")
            if isItInBounds(i-1,j+1) and 2 == board[i-1][j+1] and isAttackValid(i,j,board,1,"RIGHT"):
                attacks.append("RIGHT")
    return attacks


def move(player,board):
    bestScore = -math.inf
    moves = getPossibleMoves(player, board)
    moveloc = moves[0]
    for move in moves:
        if player==1:
            score = alphabeta(move, 1, -math.inf, math.inf, True, 1)
        elif player==2:
            score = alphabeta(move, 1, -math.inf, math.inf, True, 2)
        if score > bestScore:
            bestScore = score
            moveLoc = move
    return moveLoc

def startGame():

    board = getInitialBoard()
    # create player objects
    player = 1
    while(True):
        
        '''plt.imshow(board)
        plt.title("player=%i" %player)
        plt.show()'''
        print(board)
        properMove = move(player,board)
        board = properMove
        boolis, playerWon = gameIsSolved(board)
        if boolis:
            print(playerWon, "Won!")
            break
        if player==1:
            player=2
        else:
            player=1



'''
initial call:
minimax(currentPosition, 3, -∞, +∞, true)
'''
def alphabeta(board,depth,alpha,beta,max, player):
    smallBool,_ = gameIsSolved(board)
    if smallBool or depth==0:
        return evaluationFun(board,player)
    
    if max:
        bestValue = -math.inf
        for move in getPossibleMoves(player,board):
            if player==1:
                player=2
            else:
                player==1
            value = alphabeta(move,depth-1,alpha,beta, False, player)
            bestValue = max(bestValue,value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return bestValue
        
    else:
        smallValue = math.inf
        for move in getPossibleMoves(player,board):
            if player==1:
                player=2
            else:
                player==1
            value = alphabeta(move,depth-1,alpha,beta, True, player)
            smallValue = min(smallValue,value)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return smallValue



if __name__ == "__main__":
    startGame()