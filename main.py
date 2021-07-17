import numpy as np
import copy
import math
import time
from collections import Counter
import random
import matplotlib.pyplot as plt
from termcolor import colored

def getInitialBoard():
    board = np.zeros(shape=(8,8), dtype=int)
    
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
    lengthThree = np.count_nonzero(board == 3)
    lengthFour = np.count_nonzero(board == 4)

    lengthThree=lengthThree*5
    lengthFour=lengthFour*5
    if player==1:
        if val and play==1:
            return +100 
        elif val and play==2:
            return -100
        else:
            return lengthOne-lengthTwo+(lengthThree-lengthFour)
    else:
        if val and play==2:
            return +100
        elif val and play==1:
            return -100
        else:
            return lengthTwo-lengthOne+(lengthFour-lengthThree)


def getMainDiag(board):
    diag = []
    diag.append(board[0,7])
    diag.append(board[1,6])
    diag.append(board[2,5])
    diag.append(board[3,4])
    diag.append(board[4,3])
    diag.append(board[5,2])
    diag.append(board[6,1])
    diag.append(board[7,0])
    return diag


def getSecondaryDiag(board):
    diagLower = []
    diagUpper = []

    diagLower.append(board[1][0])
    diagLower.append(board[2][1])
    diagLower.append(board[3][2])
    diagLower.append(board[4][3])
    diagLower.append(board[5][4])
    diagLower.append(board[6][5])
    diagLower.append(board[7][6])

    diagUpper.append(board[0][1])
    diagUpper.append(board[1][2])
    diagUpper.append(board[2][3])
    diagUpper.append(board[3][4])
    diagUpper.append(board[4][5])
    diagUpper.append(board[5][6])
    diagUpper.append(board[6][7])

    return (diagLower,diagUpper)
    

def improvedEval(board,player):
    val,play=gameIsSolved(board)

    if player==1:
        if val and play==1:
            return +100 
        elif val and play==2:
            return -100
    elif player==2:
        if val and play==2:
            return +100
        elif val and play==1:
            return -100

    
    # 
    
    lengthTwo = np.count_nonzero(board == 2) # number of pawns of player 2
    lengthOne = np.count_nonzero(board == 1) # number of pawns of player 1
    lengthThree = np.count_nonzero(board == 3) # number of kings of player 1
    lengthFour = np.count_nonzero(board == 4) # number of kings of player 2
    unProtPawns = 0 # pawns that they are attacked from the enemy player
    protPawns = 0 # pawns that are not being attacked

    unProtKings = 0 # kings that are attacked
    protKings = 0 # kings that are not being attacked
    numMovablePawns = 0 # pawns that can move
    numMovableKings = 0 # kings that can move
    unOccopiedPromotion = 0 # board pieces that are empty on promotion line
    backPieces = 0 # pieces that are on back defence / last 2 rows
    attackingPawns = 0 # pawns that are in the front line first 3 rows
    attackingPawnsEnemy = 0 # >> of our enemies
    centralPawns = 0 # pawns that are in the middle two rows
    centralPawnsEnemy = 0 # enemy pawns that are in the middle two rows

    centralKings = 0 # kings that are in the middle two rows
    centralKingsEnemy = 0 # kings pawns that are in the middle two rows

    pawnsDiag = 0 # pawns that are located on the main Diagonal
    pawnsDiagEnemy = 0 # enemy pawns that are located on the main Diagonal

    kingsDiag = 0 # kings that are located on the main Diagonal
    kingsDiagEnemy = 0 # enemy kings that are located on the main Diagonal

    pawnsSecDiag = 0 # pawns that are located on the secondary two Diagonals
    pawnsSecDiagEnemy = 0 # enemy pawns that are located on the secondary two Diagonals

    kingsSecDiag = 0 # kings that are located on the secondary two Diagonals
    kingsSecDiagEnemy = 0 # enemy kings that are located on the secondary two Diagonals

    lonerPawns = 0 # pawns that are not adjacent to friendly pieces
    lonerPawnsEnemy = 0 # enemy pawns that are not adjacent to friendly pieces
    pawnsThatAttack = 0
    pawnsThatAttackEnemy = 0
    # patterns 
    boolTriangle = False
    boolOreo = False
    boolBridge = False
    boolDog = False


    #01 pattern piece
    #10
    defendedPieces = 0
    defendedPiecesEnemy = 0
    # unprotected pawns
    if player==1:
        for i in range(8):
            for j in range(8):
                if board[i][j]==2:

                    # left pattern
                    if (isItInBounds(i+1,j-1) and (board[i+1,j-1]==2 or board[i+1,j-1]==4)):
                        defendedPiecesEnemy+=1

                    # right pattern
                    if (isItInBounds(i+1,j+1) and (board[i+1,j+1]==2 or board[i+1,j+1]==4)):
                        defendedPiecesEnemy+=1

                if board[i][j]==1:
                    if isAttackAvailable(i,j,board,1):
                        pawnsThatAttack+=1

                    if (isItInBounds(i-1,j+1) and board[i-1][j+1]==0) and isItInBounds(i-1,j-1) and board[i-1][j-1]==0:
                        numMovablePawns+=1
                    
                    # left pattern
                    if (isItInBounds(i-1,j-1) and (board[i-1,j-1]==1 or board[i-1,j-1]==3)):
                        defendedPieces+=1

                    # right pattern
                    if (isItInBounds(i-1,j+1) and (board[i-1,j+1]==1 or board[i-1,j+1]==3)):
                        defendedPieces+=1

                    

                    
                if board[i][j]==3:
                    movement = getMovementQueen(i,j,board)
                    if movement!= []:
                        numMovableKings+=1
                    
                if board[i][j]==2:
                    if isAttackAvailable(i,j,board,2):
                        unProtPawns+=1
                elif board[i][j]==4:
                    if isAttackAvailableQueen(i,j,board,2):
                        unProtKings+=1

        # unoccopied fields on promotion
        unOccopiedPromotion = np.count_nonzero(board[0] == 0)

        # back pieces on the defence
        backPieces += np.count_nonzero(board[7] == 1)
        backPieces += np.count_nonzero(board[6] == 1)
        backPieces += np.count_nonzero(board[7] == 3)
        backPieces += np.count_nonzero(board[6] == 3)

        # attacking pawns ours
        attackingPawns += np.count_nonzero(board[0] == 1)
        attackingPawns += np.count_nonzero(board[1] == 1)
        attackingPawns += np.count_nonzero(board[2] == 1)

        # atacking pawns enemy
        attackingPawnsEnemy  += np.count_nonzero(board[7] == 2)
        attackingPawnsEnemy  += np.count_nonzero(board[6] == 2)
        attackingPawnsEnemy  += np.count_nonzero(board[5] == 2)


        # central our pawns
        centralPawns+= np.count_nonzero(board[3]==1)
        centralPawns+= np.count_nonzero(board[4]==1)
        # central enemy pawns
        centralPawnsEnemy+= np.count_nonzero(board[3]==2)
        centralPawnsEnemy+= np.count_nonzero(board[4]==2)

        # central our kings
        centralKings+= np.count_nonzero(board[3]==3)
        centralKings+= np.count_nonzero(board[4]==3)

        # central enemy kings
        centralKingsEnemy+= np.count_nonzero(board[3]==4)
        centralKingsEnemy+= np.count_nonzero(board[4]==4)

        # main diagonal

        diag = getMainDiag(board)
        pawnsDiag += np.count_nonzero(diag==1)
        kingsDiag += np.count_nonzero(diag==3)

        pawnsDiagEnemy += np.count_nonzero(diag==2)
        kingsDiagEnemy += np.count_nonzero(diag==4)

        # two diagonals 
        diagL,diagU = getSecondaryDiag(board) # diagL => diagonal Lower / diagonal Upper

        pawnsSecDiag += np.count_nonzero(diagL == 1)
        pawnsSecDiagEnemy += np.count_nonzero(diagL == 2)

        pawnsSecDiag += np.count_nonzero(diagU == 1)
        pawnsSecDiagEnemy += np.count_nonzero(diagU == 2)

        kingsSecDiag += np.count_nonzero(diagL == 3)
        kingsSecDiag += np.count_nonzero(diagU == 3)

        kingsSecDiagEnemy += np.count_nonzero(diagL == 4)
        kingsSecDiagEnemy += np.count_nonzero(diagU == 4)

        # loner pawns
        lonerPawns = lengthOne - defendedPieces

        lonerPawnsEnemy = lengthTwo - defendedPiecesEnemy

        # Triangle pattern 
        # [[0,1,0],[1,0,1]]
        arr = np.array([[0,0,0,0,0,1,0,0],[0,0,0,0,1,0,1,0]],int)
        newPattern=0
        for x in range(8):
            if x==7:
                break
            newBoard = np.array([board[x],board[x+1]])
            if np.array_equal(newBoard, arr):
                newPattern+=1

        if newPattern>0:
            boolTriangle=True

        
        arr = np.array([[0,0,0,1,0,0,0,0],[0,0,1,0,1,0,0,0]])
        newPattern=0
        for x in range(8):
            if x==7:
                break
            newBoard = np.array([board[x],board[x+1]])
            if np.array_equal(newBoard, arr):
                newPattern+=1

        if newPattern>0:
            boolOreo=True


        arr = np.array([0,0,1,0,0,0,1,0])
        newPattern=0
        for x in range(8):
            newBoard = np.array(board[x])
            if np.array_equal(newBoard, arr):
                newPattern+=1

        if newPattern>0:
            boolBridge=True


        arr = np.array([[0,0,0,0,0,0,0,2],[0,0,0,0,0,0,1,0]])
        newPattern=0
        for x in range(8):
            if x==7:
                break
            newBoard = np.array([board[x],board[x+1]])
            if np.array_equal(newBoard, arr):
                newPattern+=1

        if newPattern>0:
            boolDog=True

        # normal tings
        protKings = lengthThree - unProtKings
        protPawns = lengthTwo - unProtPawns
    elif player==2:
        for i in range(8):
            for j in range(8):
                if board[i][j]==1:
                    # left pattern
                    if (isItInBounds(i-1,j-1) and (board[i-1,j-1]==1 or board[i-1,j-1]==3)):
                        defendedPiecesEnemy+=1

                    # right pattern
                    if (isItInBounds(i-1,j+1) and (board[i-1,j+1]==1 or board[i-1,j+1]==3)):
                        defendedPiecesEnemy+=1

                if board[i][j]==2:
                    if isAttackAvailable(i,j,board,2):
                        pawnsThatAttack+=1

                    if isItInBounds(i+1,j-1) and board[i+1][j-1]==0 and isItInBounds(i+1,j+1) and board[i+1][j+1]==0:
                        numMovablePawns+=1

                    # left pattern
                    if (isItInBounds(i+1,j-1) and (board[i+1,j-1]==2 or board[i+1,j-1]==4)):
                        defendedPieces+=1

                    # right pattern
                    if (isItInBounds(i+1,j+1) and (board[i+1,j+1]==2 or board[i+1,j+1]==4)):
                        defendedPieces+=1

                if board[i][j]==4:
                    movement = getMovementQueen(i,j,board)
                    if movement!= []:
                        numMovableKings+=1
                

                if board[i][j]==1:
                    if isAttackAvailable(i,j,board,1):
                        unProtPawns+=1
                elif board[i][j]==3:
                    if isAttackAvailableQueen(i,j,board,1):
                        unProtKings+=1

        # unoccopied fields on promotion
        unOccopiedPromotion = np.count_nonzero(board[7] == 0)

        # back pieces on the defence
        backPieces += np.count_nonzero(board[0] == 2)
        backPieces += np.count_nonzero(board[1] == 2)
        backPieces += np.count_nonzero(board[0] == 4)
        backPieces += np.count_nonzero(board[1] == 4)

        # attacking pawns ours
        attackingPawns += np.count_nonzero(board[7] == 2)
        attackingPawns += np.count_nonzero(board[6] == 2)
        attackingPawns += np.count_nonzero(board[5] == 2)

        # atacking pawns enemy
        attackingPawnsEnemy  += np.count_nonzero(board[0] == 1)
        attackingPawnsEnemy  += np.count_nonzero(board[1] == 1)
        attackingPawnsEnemy  += np.count_nonzero(board[2] == 1)

        # central our pawns
        centralPawns+= np.count_nonzero(board[3]==2)
        centralPawns+= np.count_nonzero(board[4]==2)
        # central enemy pawns
        centralPawnsEnemy+= np.count_nonzero(board[3]==1)
        centralPawnsEnemy+= np.count_nonzero(board[4]==1)

        # central our kings
        centralKings+= np.count_nonzero(board[3]==4)
        centralKings+= np.count_nonzero(board[4]==4)

        # central enemy kings
        centralKingsEnemy+= np.count_nonzero(board[3]==3)
        centralKingsEnemy+= np.count_nonzero(board[4]==3)

        # main diagonal

        diag = getMainDiag(board)
        pawnsDiag += np.count_nonzero(diag==2)
        kingsDiag += np.count_nonzero(diag==4)

        pawnsDiagEnemy += np.count_nonzero(diag==1)
        kingsDiagEnemy += np.count_nonzero(diag==3)


        # two diagonals 
        diagL,diagU = getSecondaryDiag(board) # diagL => diagonal Lower / diagonal Upper

        pawnsSecDiag += np.count_nonzero(diagL == 2)
        pawnsSecDiagEnemy += np.count_nonzero(diagL == 1)

        pawnsSecDiag += np.count_nonzero(diagU == 2)
        pawnsSecDiagEnemy += np.count_nonzero(diagU == 1)

        kingsSecDiag += np.count_nonzero(diagL == 4)
        kingsSecDiag += np.count_nonzero(diagU == 4)

        kingsSecDiagEnemy += np.count_nonzero(diagL == 3)
        kingsSecDiagEnemy += np.count_nonzero(diagU == 3)

        # loner pawns
        lonerPawns = lengthTwo - defendedPieces

        lonerPawnsEnemy = lengthOne - defendedPiecesEnemy

        # normal tings
        protKings = lengthFour - unProtKings
        protPawns = lengthTwo - unProtPawns

        # Triangle pattern 
        # Triangle pattern 
        # [[0,1,0],[1,0,1]]s
        arr = np.array([[0,2,0,2,0,0,0,0],[0,0,2,0,0,0,0,0]],int)
        newPattern=0
        for x in range(8):
            if x==7:
                break
            newBoard = np.array([board[x],board[x+1]])
            if np.array_equal(newBoard, arr):
                newPattern+=1

        if newPattern>0:
            boolTriangle=True

        
        arr = np.array([[0,0,0,2,0,2,0,0],[0,0,0,0,2,0,0,0]])
        newPattern=0
        for x in range(8):
            if x==7:
                break
            newBoard = np.array([board[x],board[x+1]])
            if np.array_equal(newBoard, arr):
                newPattern+=1

        if newPattern>0:
            boolOreo=True


        arr = np.array([0,2,0,0,0,2,0,0])
        newPattern=0
        for x in range(8):
            newBoard = np.array(board[x])
            if np.array_equal(newBoard, arr):
                newPattern+=1

        if newPattern>0:
            boolBridge=True


        arr = np.array([[0,2,0,0,0,0,0,0],[1,0,0,0,0,0,0,0]])
        newPattern=0
        for x in range(8):
            if x==7:
                break
            newBoard = np.array([board[x],board[x+1]])
            if np.array_equal(newBoard, arr):
                newPattern+=1

        if newPattern>0:
            boolDog=True


        

    var=0

    if boolTriangle:
        var+=10

    if boolBridge:
        var+=10

    if boolOreo:
        var+=10

    if boolDog:
        var+=10

    if player==1:
        var = ((lengthOne-lengthTwo)*5) + (lengthThree - lengthFour)*5 - unProtPawns*3 - unProtKings*5 +protPawns + protKings*5 + numMovablePawns + numMovableKings*3 + unOccopiedPromotion + backPieces + attackingPawns - attackingPawnsEnemy + centralPawns - centralPawnsEnemy + centralKings - centralKingsEnemy - kingsDiagEnemy*3 + kingsDiag + kingsSecDiag*3 - kingsSecDiagEnemy*3 - lonerPawns + lonerPawnsEnemy + defendedPieces - defendedPiecesEnemy + pawnsThatAttack*30
    elif player==2:
        var = ((lengthTwo-lengthOne)* 5) + (lengthFour - lengthThree)*5 - unProtPawns*3 - unProtKings*5 + protPawns + protKings*5 + numMovablePawns + numMovableKings*3 + unOccopiedPromotion + backPieces + attackingPawns - attackingPawnsEnemy + centralPawns - centralPawnsEnemy + centralKings - centralKingsEnemy - kingsDiagEnemy*3 + kingsDiag + kingsSecDiag*3 - kingsSecDiagEnemy*3 - lonerPawns + lonerPawnsEnemy + defendedPieces - defendedPiecesEnemy + pawnsThatAttack*30
    
    return var
    


def getMovementQueen(x,y,board):
    moves = []
    upLeft=[]
    upRight = []
    downLeft = []
    downRight = []
    newX = x+1
    newY = y+1
    while isItInBounds(newX,newY) and board[newX][newY]==0:
        movementBoard = copy.deepcopy(board)
        movementBoard[x][y]=0
        movementBoard[newX][newY]=3
        downRight.append(movementBoard)
        newX = newX+1
        newY = newY+1
    newX,newY=x,y
    newX = x+1
    newY = y-1
    while isItInBounds(newX,newY) and board[newX][newY]==0:
        movementBoard = copy.deepcopy(board)
        movementBoard[x][y]=0
        movementBoard[newX][newY]=3
        downLeft.append(movementBoard)
        newX = newX+1
        newY = newY-1
    newX,newY=x,y
    newX = x-1
    newY = y+1
    while isItInBounds(newX,newY) and board[newX][newY]==0:
        movementBoard = copy.deepcopy(board)
        movementBoard[x][y]=0
        movementBoard[newX][newY]=3
        upRight.append(movementBoard)
        newX = newX-1
        newY = newY+1
    newX,newY=x,y
    newX = x-1
    newY = y-1
    while isItInBounds(newX,newY) and board[newX][newY]==0:
        movementBoard = copy.deepcopy(board)
        movementBoard[x][y]=0
        movementBoard[newX][newY]=3
        upLeft.append(movementBoard)
        newX = newX-1
        newY = newY-1
    
    for a in upLeft:
        moves.append(a)
    for a in upRight:
        moves.append(a)
    for a in downLeft:
        moves.append(a)
    for a in downRight:
        moves.append(a)

    return moves



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
can be called firstVar,_ = gameIsSolved(board)
'''
def gameIsSolved(board):
    lengthTwo = np.count_nonzero(board == 2)
    lengthOne = np.count_nonzero(board == 1)
    lengthThree = np.count_nonzero(board == 3)
    lengthFour = np.count_nonzero(board == 4)

    if (lengthOne+lengthThree)==0:
        return True,2
    elif (lengthTwo+lengthFour)==0:
        return True,1
    else:
        return False,None


def isAttackAvailable(i,j,board,player):
    if player==1:
        # direction left
        if isItInBounds(i-1, j-1) and (board[i-1][j-1]==2 or board[i-1][j-1]==4)  and isItInBounds(i-2,j-2) and board[i-2][j-2]==0:
            return True
            
            
        # direction right
        if isItInBounds(i-1, j+1) and (board[i-1][j+1]==2 or board[i-1][j+1]==4)  and isItInBounds(i-2,j+2) and board[i-2][j+2]==0:
            return True
            
        
    elif player==2:
        # direction left
        if isItInBounds(i+1,j-1) and (board[i+1][j-1]==1 or board[i+1][j-1]==3)  and isItInBounds(i+2,j-2) and board[i+2][j-2]==0:
            return True
        

        # direction right
        if isItInBounds(i+1, j+1) and (board[i+1][j+1]==1 or board[i+1][j+1]==3) and isItInBounds(i+2,j+2) and board[i+2][j+2]==0:
            return True
    else:
        return False


def isItInBounds(i,j):
    if i>=0 and i<=7 and j>=0 and j<=7:
        return True
    else:
        return False

'''def isThereAnAttackOnBoard(board, player):
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
    
    return False
'''

def whereIsTheAttack(i,j,board, player):
    attacks = []

    if player==2:
        if isItInBounds(i+1,j-1) and (board[i+1][j-1] == 1 or board[i+1][j-1] == 3) and isAttackValid(i,j,board,2,"LEFT"):
            attacks.append("LEFT")
        if  isItInBounds(i+1,j+1) and (board[i+1][j+1]==1 or board[i+1][j+1]==3) and isAttackValid(i,j,board,2,"RIGHT"):
            attacks.append("RIGHT")
        return attacks
    elif player==1:
            if isItInBounds(i-1,j-1) and (2 == board[i-1][j-1] or 4 == board[i-1][j-1]) and isAttackValid(i,j,board,1,"LEFT"):
                attacks.append("LEFT")
            if isItInBounds(i-1,j+1) and (2 == board[i-1][j+1] or 4 == board[i-1][j+1]) and isAttackValid(i,j,board,1,"RIGHT"):
                attacks.append("RIGHT")
    return attacks


'''
after movement
'''
def canWeQueen(i,player):
    if player==1:
        if i==0:
            return True
        else:
            return False
    elif player==2:
        if i==7:
            return True
        else:
            return False
    else:
        return False


def getDiagonals(x,y,board):
    upLeft=[]
    upRight = []
    downLeft = []
    downRight = []

    newX = x+1
    newY = y+1
    while isItInBounds(newX,newY):
        downRight.append(board[newX][newY])
        newX = newX+1
        newY = newY+1

    newX = x+1
    newY = y-1
    while isItInBounds(newX,newY):

        downLeft.append(board[newX][newY])
        newX = newX+1
        newY = newY-1
    
    newX = x-1
    newY = y+1
    while isItInBounds(newX,newY):
        upRight.append(board[newX][newY])
        newX = newX-1
        newY = newY+1
    
    newX = x-1
    newY = y-1
    while isItInBounds(newX,newY):
        upLeft.append(board[newX][newY])
        newX = newX-1
        newY = newY-1

    varDouble = False
    counter=0
    upLeftSec = []
    for i in upLeft:
        if varDouble and i!=0:
            upLeftSec.pop(len(upLeftSec)-1)
            upLeft = upLeftSec
            break

        upLeftSec.append(i)
        if i !=0:
            varDouble=True
        else:
            varDouble=False
        counter=counter+1

    varDouble = False
    counter=0
    upRightSec = []
    for i in upRight:
        if varDouble and i!=0:
            upRightSec.pop(len(upRightSec)-1)
            upRight= upRightSec
            break
        
        upRightSec.append(i)
        if i !=0:
            varDouble=True
        else:
            varDouble=False
        counter=counter+1

    varDouble = False
    counter=0
    downLeftSec = []
    for i in downLeft:
        if varDouble and i!=0:
            downLeftSec.pop(len(downLeftSec)-1)
            downLeft= downLeftSec
            break
        downLeftSec.append(i)
        if i !=0:
            varDouble=True
        else:
            varDouble=False
        counter=counter+1

    varDouble = False
    counter=0
    downRightSec= []
    for i in downRight:
        if varDouble and i !=0:
            downRightSec.pop(len(downRightSec)-1)
            downRight= downRightSec
            break
        downRightSec.append(i)
        if i !=0:
            varDouble=True
        else:
            varDouble=False
        counter=counter+1 

    return {
        'up_left' : upLeft,
        'up_right' : upRight,
        'dw_left' : downLeft,
        'dw_right' : downRight
    }

def isAttackAvailableQueen(i,j,board,player):
    if not isItInBounds(i,j):
        return [],False
    
    if (board[i][j]==4 and player==2):
        pass
    elif (board[i][j]==3 and player==1):
        pass
    else:
        return [],False

    newDict = getDiagonals(i,j,board)
    del newDict['up_left'][len(newDict['up_left'])-1:]
    del newDict['up_right'][len(newDict['up_right'])-1:]
    del newDict['dw_left'][len(newDict['dw_left'])-1:]
    del newDict['dw_right'][len(newDict['dw_right'])-1:]


    listoua = []

    if player==1:
        if (newDict['up_left'].count(2) > 0 or newDict['up_left'].count(4) > 0):
            listoua.append(("up_left",newDict["up_left"]))
        if (newDict['up_right'].count(2) > 0 or newDict['up_right'].count(4) > 0):
            listoua.append(("up_right", newDict["up_right"]))
        if (newDict['dw_left'].count(2) > 0 or newDict['dw_left'].count(4) > 0):
            listoua.append(("dw_left", newDict["dw_left"]))
        if (newDict['dw_right'].count(2) > 0 or newDict['dw_right'].count(4) > 0):
            listoua.append(("dw_right", newDict["dw_right"]))
    elif player==2:
        if (newDict['up_left'].count(3) > 0 or newDict['up_left'].count(1) > 0):
            listoua.append(("up_left", newDict["up_left"]))
        if (newDict['up_right'].count(3) > 0 or newDict['up_right'].count(1) > 0):
            listoua.append(("up_right", newDict["up_right"]))
        if (newDict['dw_left'].count(3) > 0 or newDict['dw_left'].count(1) > 0):
            listoua.append(("dw_left", newDict["dw_left"]))
        if (newDict['dw_right'].count(3) > 0 or newDict['dw_right'].count(1) > 0):
            listoua.append(("dw_right", newDict["dw_right"]))
    else: 
        return [],False

    if listoua!=[]:
        return listoua,True
    else:
        return [],False




def move(player,board):
    bestScore = -math.inf
    moves = getPossibleMoves(player, board)
    moveloc = moves[0]
    if player==1:
        for position in moves:
            score = alphabeta(position, 3, -math.inf, math.inf, True, 1,1)
            if score > bestScore:
                bestScore = score
                moveLoc = position
        return moveLoc
    else:
        for position in moves:
            score = alphabeta(position, 3, -math.inf, math.inf, True, 2,2)
            if score > bestScore:
                bestScore = score
                moveLoc = position
        return moveLoc


'''
initial call:
minimax(currentPosition, 3, -∞, +∞, true)
'''
# Ivy is the name of the engine
def alphabeta(board,depth,alpha,beta,maxPlayer, player, initialPlayer):
    smallBool,_ = gameIsSolved(board)
    if smallBool or depth==0:
        if initialPlayer==2:
            return improvedEval(board,initialPlayer)
        else:
            return improvedEval(board,initialPlayer)

    if player==1:
        player=2
    elif player==2:
        player=1

    if maxPlayer:
        bestValue = -math.inf
        for move in getPossibleMoves(player,board):
            value = alphabeta(move,depth-1,alpha,beta, False, player,initialPlayer)
            bestValue = max(bestValue,value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return bestValue
        
    else:
        smallValue = math.inf
        for move in getPossibleMoves(player,board):
            value = alphabeta(move,depth-1,alpha,beta, True, player,initialPlayer)
            smallValue = min(smallValue,value)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return smallValue

def printBoard(board,player):

    colorMap = {
        0: np.array([255,255,255]),
        3: np.array([117,72,72]),
        1: np.array([255,0,0]),
        2: np.array([251,255,0]),
        4: np.array([124,125,76])
    }

    threeDArr = np.ndarray(shape=(board.shape[0], board.shape[1], 3), dtype=int)
    for i in range(0, board.shape[0]):
        for j in range(0, board.shape[1]):
            threeDArr[i][j] = colorMap[board[i][j]]

    
    fig, ax = plt.subplots(1,1)
    ax.imshow(threeDArr)
    for i in range(0, board.shape[0]):
        for j in range(0, board.shape[1]):
            c = board[j,i]
            ax.text(i, j, str(c), va='center', ha='center')
    
    plt.title("player=%i" %player)
    plt.show()

def startGame():
    board = getInitialBoard()
    gamePositions=[]
    player = 1
    while(True):
        print(colored(player,'blue'))
        print(colored(board,'green'))
        #printBoard(board,player)
        start = time.time()
        board = move(player,board)
        # repeation checking
        gamePositions.append(board)
        if len(gamePositions)>=11:
            newBool = checkPositions(gamePositions[-11:])
            if newBool:
                listOfMoves = getPossibleMoves(player=player,board=board)
                minMove = listOfMoves[1]
                for i in listOfMoves:
                    if improvedEval(i,player)>improvedEval(minMove,player):
                        minMove = i
                #board = random.choice(getPossibleMoves(player=player,board=board))
                board=minMove
        
        print("Time took for each move:",round(time.time()-start,6))
        boolis, playerWon = gameIsSolved(board)
        if boolis:
            print(playerWon, "Won!")
            print(colored(player,'blue'))
            print(colored(board,'green'))
            #printBoard(board,player)
            break
        if player==1:
            player=2
        elif player==2:
            player=1


def checkPositions(positions):
    indy = 0 #index
    for i in positions:
        newPositions = positions
        del newPositions[indy]
        countRep = 0
        for j in newPositions:
            if (i==j).all():
                countRep+=1
        if countRep>=2: # because we remove the index we are in now
            return True
        indy+=1
    return False
    pass

def getPossibleMoves(player,board):
    moves = []
    if player==1:
        for x in range(8):
            for y in range(8):
                if board[x][y]==1:
                    # left
                    if isItInBounds(x-1,y-1) and board[x-1][y-1]==0:
                            edit = copy.deepcopy(board)
                            edit[x][y]=0
                            edit[x-1][y-1]=1
                            if canWeQueen(x-1,1):
                                edit[x-1][y-1]=3
                                moves.append(edit)
                            else:
                                moves.append(edit)

                    # right
                    if isItInBounds(x-1,y+1) and board[x-1][y+1]==0:
                            edit = copy.deepcopy(board)
                            edit[x][y]=0
                            edit[x-1][y+1]=1
                            if canWeQueen(x-1,1):
                                edit[x-1][y+1]=3
                                moves.append(edit)
                            else:
                                moves.append(edit)
                    if isAttackAvailable(x,y,board,1):
                        # there is an attack
                        directionList = whereIsTheAttack(x,y,board,1)
                        for dir in directionList:
                            if dir=="LEFT":
                                # first jump left
                                copyBoard = copy.deepcopy(board)
                                copyBoard[x][y]=0
                                copyBoard[x-1][y-1]=0
                                if canWeQueen(x-2,1):
                                    copyBoard[x-2][y-2]=3
                                else:
                                    copyBoard[x-2][y-2]=1
                                newX,newY = x-2,y-2
                                if isAttackAvailable(newX,newY,copyBoard,1):
                                    firstLeftdirectionList = whereIsTheAttack(newX,newY,copyBoard,1)
                                    for firstLeftDir in firstLeftdirectionList:
                                        if firstLeftDir == "LEFT":
                                            # second attack left
                                            firstLeftBoard = copy.deepcopy(copyBoard)
                                            firstLeftBoard[newX][newY]=0
                                            firstLeftBoard[newX-1][newY-1]=0
                                            if canWeQueen(newX-2,1):
                                                firstLeftBoard[newX-2][newY-2]=3
                                            else:
                                                firstLeftBoard[newX-2][newY-2]=1
                                            firstLeftX,firstLeftY = newX-2, newY-2
                                            if isAttackAvailable(firstLeftX,firstLeftY,firstLeftBoard,1):
                                                secondLeftDirectionList = whereIsTheAttack(firstLeftX,firstLeftY,firstLeftBoard,1)
                                                for secondLeftDir in secondLeftDirectionList:
                                                    if secondLeftDir == "LEFT":
                                                        # third left
                                                        secondLeftBoard = copy.deepcopy(firstLeftBoard)
                                                        secondLeftBoard[firstLeftX][firstLeftY]=0
                                                        secondLeftBoard[firstLeftX-1][firstLeftY-1]=0
                                                        if canWeQueen(firstLeftX-2,1):
                                                            secondLeftBoard[firstLeftX-2][firstLeftY-2]=3
                                                        else:
                                                            secondLeftBoard[firstLeftX-2][firstLeftY-2]=1
                                                        moves.append(secondLeftBoard)
                                                    else:
                                                        # third right
                                                        secondLeftBoard = copy.deepcopy(firstLeftBoard)
                                                        secondLeftBoard[firstLeftX][firstLeftY]=0
                                                        secondLeftBoard[firstLeftX-1][firstLeftY+1]=0
                                                        if canWeQueen(firstLeftX-2,1):
                                                            secondLeftBoard[firstLeftX-2][firstLeftY+2]=3
                                                        else:
                                                            secondLeftBoard[firstLeftX-2][firstLeftY+2]=1
                                                        
                                                        moves.append(secondLeftBoard)
                                            else:
                                                moves.append(firstLeftBoard)
                                        else:
                                            #second attack right
                                            firstRightBoard = copy.deepcopy(copyBoard)
                                            firstRightBoard[newX][newY]=0
                                            firstRightBoard[newX-1][newY+1]=0
                                            
                                            if canWeQueen(newX-2,1):
                                                firstRightBoard[newX-2][newY+2]=3
                                            else:
                                                firstRightBoard[newX-2][newY+2]=1
                                            firstLeftX,firstLeftY = newX-2, newY+2
                                            if isAttackAvailable(firstLeftX,firstLeftY,firstRightBoard,1):
                                                secondLeftDirectionList = whereIsTheAttack(firstLeftX,firstLeftY,firstRightBoard,1)
                                                for secondLeftDir in secondLeftDirectionList:
                                                    if secondLeftDir == "LEFT":
                                                        # third left
                                                        secondLeftBoard = copy.deepcopy(firstRightBoard)
                                                        secondLeftBoard[firstLeftX][firstLeftY]=0
                                                        secondLeftBoard[firstLeftX-1][firstLeftY-1]=0
                                                        secondLeftBoard[firstLeftX-2][firstLeftY-2]=1
                                                        if canWeQueen(firstLeftX-2,1):
                                                            secondLeftBoard[firstLeftX-2][firstLeftY-2]=3
                                                        else:
                                                            secondLeftBoard[firstLeftX-2][firstLeftY-2]=1
                                                        moves.append(secondLeftBoard)
                                                    else:
                                                        # third right
                                                        secondLeftBoard = copy.deepcopy(firstRightBoard)
                                                        secondLeftBoard[firstLeftX][firstLeftY]=0
                                                        secondLeftBoard[firstLeftX-1][firstLeftY+1]=0
                                                        if canWeQueen(x,1):
                                                            secondLeftBoard[firstLeftX-2][firstLeftY+2]=3
                                                        else:
                                                            secondLeftBoard[firstLeftX-2][firstLeftY+2]=1
                                                        moves.append(secondLeftBoard)
                                            else:
                                                moves.append(firstRightBoard)
                                else:
                                    moves.append(copyBoard)
                            else:
                                # first jump right
                                copyBoard = copy.deepcopy(board)
                                copyBoard[x][y]=0
                                copyBoard[x-1][y+1]=0
                                copyBoard[x-2][y+2]=1
                                if canWeQueen(x-2,1):
                                    copyBoard[x-2][y+2]=3
                                else:
                                    copyBoard[x-2][y+2]=1
                                newX,newY = x-2,y+2
                                if isAttackAvailable(newX,newY,copyBoard,1):
                                    firstLeftdirectionList = whereIsTheAttack(newX,newY,copyBoard,1)
                                    for firstLeftDir in firstLeftdirectionList:
                                        if firstLeftDir == "LEFT":
                                            # second attack left
                                            firstLeftBoard = copy.deepcopy(copyBoard)
                                            firstLeftBoard[newX][newY]=0
                                            firstLeftBoard[newX-1][newY-1]=0
                                            if canWeQueen(newX-2,1):
                                                firstLeftBoard[newX-2][newY-2]=3
                                            else:
                                                firstLeftBoard[newX-2][newY-2]=1
                                            
                                            firstLeftX,firstLeftY = newX-2, newY-2
                                            if isAttackAvailable(firstLeftX,firstLeftY,firstLeftBoard,1):
                                                firstLeftdirectionList = whereIsTheAttack(firstLeftX,firstLeftY,firstLeftBoard,1)
                                                for firstLeftDir in firstLeftdirectionList:
                                                    if firstLeftDir == "LEFT":
                                                        #third left
                                                        secondLeftBoard = copy.deepcopy(firstLeftBoard)
                                                        secondLeftBoard[firstLeftX][firstLeftY]=0
                                                        secondLeftBoard[firstLeftX-1][firstLeftY-1]=0
                                                        if canWeQueen(firstLeftX-2,1):
                                                            secondLeftBoard[firstLeftX-2][firstLeftY-2]=3
                                                        else:
                                                            secondLeftBoard[firstLeftX-2][firstLeftY-2]=1
                                                        moves.append(secondLeftBoard)
                                                    else:
                                                        # third right
                                                        secondLeftBoard = copy.deepcopy(firstLeftBoard)
                                                        secondLeftBoard[firstLeftX][firstLeftY]=0
                                                        secondLeftBoard[firstLeftX-1][firstLeftY+1]=0
                                                        secondLeftBoard[firstLeftX-2][firstLeftY+2]=1
                                                        if canWeQueen(firstLeftX-2,1):
                                                            secondLeftBoard[firstLeftX-2][firstLeftY+2]=3
                                                        else:
                                                            secondLeftBoard[firstLeftX-2][firstLeftY+2]=1
                                                        moves.append(secondLeftBoard)
                                            else:
                                                moves.append(firstLeftBoard)
                                        else:
                                            #second attack right
                                            firstRightBoard = copy.deepcopy(copyBoard)
                                            firstRightBoard[newX][newY]=0
                                            firstRightBoard[newX-1][newY+1]=0
                                            if canWeQueen(newX-2,1):
                                                firstRightBoard[newX-2][newY+2]=3
                                            else:
                                                firstRightBoard[newX-2][newY+2]=1
                                            firstLeftX,firstLeftY = newX-2, newY+2
                                            if isAttackAvailable(firstLeftX,firstLeftY,firstRightBoard,1):
                                                firstLeftdirectionList = whereIsTheAttack(firstLeftX,firstLeftY,firstRightBoard,1)
                                                for firstLeftDir in firstLeftdirectionList:
                                                    if firstLeftDir == "LEFT":
                                                        #third left
                                                        secondLeftBoard = copy.deepcopy(firstRightBoard)
                                                        secondLeftBoard[firstLeftX][firstLeftY]=0
                                                        secondLeftBoard[firstLeftX-1][firstLeftY-1]=0
                                                        if canWeQueen(firstLeftX-2,1):
                                                            secondLeftBoard[firstLeftX-2][firstLeftY-2]=3
                                                        else:
                                                            secondLeftBoard[firstLeftX-2][firstLeftY-2]=1
                                                        moves.append(secondLeftBoard)
                                                    else:
                                                        # third right
                                                        secondLeftBoard = copy.deepcopy(firstRightBoard)
                                                        secondLeftBoard[firstLeftX][firstLeftY]=0
                                                        secondLeftBoard[firstLeftX-1][firstLeftY+1]=0
                                                        if canWeQueen(firstLeftX-2,1):
                                                            secondLeftBoard[firstLeftX-2][firstLeftY+2]=1
                                                        else:
                                                            secondLeftBoard[firstLeftX-2][firstLeftY+2]=1
                                                        moves.append(secondLeftBoard)
                                            else:
                                                moves.append(firstRightBoard)
                                else:
                                    moves.append(copyBoard)
                elif board[x][y]==3:
                    direction,boolis = isAttackAvailableQueen(x,y,board,1)
                    upLeft=[]
                    upRight = []
                    downLeft = []
                    downRight = []
                    newX = x+1
                    newY = y+1
                    while isItInBounds(newX,newY) and board[newX][newY]==0:
                        movementBoard = copy.deepcopy(board)
                        movementBoard[x][y]=0
                        movementBoard[newX][newY]=3
                        downRight.append(movementBoard)
                        newX = newX+1
                        newY = newY+1
                    newX,newY=x,y
                    newX = x+1
                    newY = y-1
                    while isItInBounds(newX,newY) and board[newX][newY]==0:
                        movementBoard = copy.deepcopy(board)
                        movementBoard[x][y]=0
                        movementBoard[newX][newY]=3
                        downLeft.append(movementBoard)
                        newX = newX+1
                        newY = newY-1
                    newX,newY=x,y
                    newX = x-1
                    newY = y+1
                    while isItInBounds(newX,newY) and board[newX][newY]==0:
                        movementBoard = copy.deepcopy(board)
                        movementBoard[x][y]=0
                        movementBoard[newX][newY]=3
                        upRight.append(movementBoard)
                        newX = newX-1
                        newY = newY+1
                    newX,newY=x,y
                    newX = x-1
                    newY = y-1
                    while isItInBounds(newX,newY) and board[newX][newY]==0:
                        movementBoard = copy.deepcopy(board)
                        movementBoard[x][y]=0
                        movementBoard[newX][newY]=3
                        upLeft.append(movementBoard)
                        newX = newX-1
                        newY = newY-1
                    
                    for a in upLeft:
                        moves.append(a)
                    for a in upRight:
                        moves.append(a)
                    for a in downLeft:
                        moves.append(a)
                    for a in downRight:
                        moves.append(a)
                    # so we know we can attack
                    # we have the list of the attack 
                    if boolis==True:
                        for ggg in direction:
                            if ggg[0] == "up_right":
                                summ=0
                                for randomS in ggg[1]:
                                    if randomS==2 or randomS==4:
                                        summ=summ+1
                                        break
                                    else:
                                        summ=summ+1

                                
                                miniBoard = copy.deepcopy(board)
                                newX = x-summ
                                newY = y+summ
                                miniBoard[x][y]=0
                                miniBoard[newX][newY]=0
                                miniBoard[newX-1][newY+1]=3
                                brandNewX, brandNewY = newX-1,newY+1
                                newDir, newBoolis = isAttackAvailableQueen(brandNewX,brandNewY,miniBoard,1)
                                if newBoolis:
                                    newNewBoard = recursiveAttackQueen(brandNewX,brandNewY,miniBoard,1,newDir)
                                    moves.append(newNewBoard)
                                else:
                                    moves.append(miniBoard)
                                
                            elif ggg[0] == "up_left":
                                summ=0
                                for randomS in ggg[1]:
                                    if randomS==2 or randomS==4:
                                        summ=summ+1
                                        break
                                    else:
                                        summ=summ+1
                                    
                                miniBoard = copy.deepcopy(board)
                                newX = x-summ
                                newY = y-summ
                                miniBoard[x][y]=0
                                miniBoard[newX][newY]=0
                                miniBoard[newX-1][newY-1]=3
                                brandNewX, brandNewY = newX-1,newY-1
                                newDir, newBoolis = isAttackAvailableQueen(brandNewX,brandNewY,miniBoard,1)
                                if newBoolis:
                                    newNewBoard = recursiveAttackQueen(brandNewX,brandNewY,miniBoard,1,newDir)
                                    moves.append(newNewBoard)
                                else:
                                    moves.append(miniBoard)

                            elif ggg[0] == "dw_right":
                                summ=0
                                for randomS in ggg[1]:
                                    if randomS==2 or randomS==4:
                                        summ=summ+1
                                        break
                                    else:
                                        summ=summ+1
                                
                                miniBoard = copy.deepcopy(board)
                                newX = x+summ
                                newY = y+summ
                                miniBoard[x][y]=0
                                miniBoard[newX][newY]=0
                                miniBoard[newX+1][newY+1]=3
                                brandNewX, brandNewY = newX+1,newY+1
                                newDir, newBoolis = isAttackAvailableQueen(brandNewX,brandNewY,miniBoard,1)
                                if newBoolis:
                                    newNewBoard = recursiveAttackQueen(brandNewX,brandNewY,miniBoard,1,newDir)
                                    moves.append(newNewBoard)
                                else:
                                    moves.append(miniBoard)

                            elif ggg[0] == "dw_left":
                                summ=0
                                for randomS in ggg[1]:
                                    if randomS==2 or randomS==4:
                                        summ=summ+1
                                        break
                                    else:
                                        summ=summ+1

                                miniBoard = copy.deepcopy(board)
                                newX = x+summ
                                newY = y-summ
                                miniBoard[x][y]=0
                                miniBoard[newX][newY]=0
                                miniBoard[newX+1][newY-1]=3
                                brandNewX, brandNewY = newX+1,newY-1
                                newDir, newBoolis = isAttackAvailableQueen(brandNewX,brandNewY,miniBoard,1)
                                if newBoolis:
                                    newNewBoard = recursiveAttackQueen(brandNewX,brandNewY,miniBoard,1,newDir)
                                    moves.append(newNewBoard)
                                else:
                                    moves.append(miniBoard)
    elif player==2:
        for x in range(8):
            for y in range(8):
                if board[x][y]==2:
                    # left
                    if isItInBounds(x+1,y-1) and board[x+1][y-1]==0:
                        edit = copy.deepcopy(board)
                        edit[x][y]=0
                        edit[x+1][y-1]=2
                        if canWeQueen(x+1,2):
                            edit[x+1][y-1]=4
                            moves.append(edit)
                        else:
                            moves.append(edit)
                    # right
                    if isItInBounds(x+1,y+1) and board[x+1][y+1]==0:
                        edit= copy.deepcopy(board)
                        edit[x][y]=0
                        edit[x+1][y+1]=2
                        if canWeQueen(x+1,2):
                            edit[x+1][y+1]=4
                            moves.append(edit)
                        else:
                            moves.append(edit)
                    if isAttackAvailable(x,y,board,2):
                        # there is an attack
                        directionList = whereIsTheAttack(x,y,board,2)
                        for dir in directionList:
                            if dir=="LEFT":
                                # first jump left
                                copyBoard = copy.deepcopy(board)
                                copyBoard[x][y]=0
                                copyBoard[x+1][y-1]=0
                                if canWeQueen(x+2,1):
                                    copyBoard[x+2][y-2]=4
                                else:
                                    copyBoard[x+2][y-2]=2
                                newX,newY = x+2, y-2
                                if isAttackAvailable(newX,newY,copyBoard,2):
                                    firstLeftdirectionList = whereIsTheAttack(newX,newY,copyBoard,2)
                                    for secondDirection in firstLeftdirectionList:
                                        if secondDirection == "LEFT":
                                            # second
                                            newBoardSec = copy.deepcopy(copyBoard)
                                            newBoardSec[newX][newY]=0
                                            newBoardSec[newX+1][newY-1]=0
                                            if canWeQueen(newX+2,1):
                                                newBoardSec[newX+2][newY-2]=4
                                            else:
                                                newBoardSec[newX+2][newY-2]=2
                                            firstRightX,firstRightY = newX+2, newY-2
                                            if isAttackAvailable(firstRightX,firstRightY,newBoardSec,2):
                                                secondLeftDirectionList = whereIsTheAttack(firstRightX,firstRightY,newBoardSec,2)
                                                for SLD in secondLeftDirectionList:
                                                    if SLD=="LEFT":
                                                        # third
                                                        newBoardThird = copy.deepcopy(newBoardSec)
                                                        newBoardThird[firstRightX][firstRightY]=0
                                                        newBoardThird[firstRightX+1][firstRightY-1]=0
                                                        if canWeQueen(firstRightX+2,1):
                                                            newBoardThird[firstRightX+2][firstRightY-2]=4
                                                        else:
                                                            newBoardThird[firstRightX+2][firstRightY-2]=2
                                                        moves.append(newBoardThird)
                                                    else:
                                                        # third
                                                        newBoardThird = copy.deepcopy(newBoardSec)
                                                        newBoardThird[firstRightX][firstRightY]=0
                                                        newBoardThird[firstRightX+1][firstRightY+1]=0
                                                        if canWeQueen(firstRightX+2,1):
                                                            newBoardThird[firstRightX+2][firstRightY+2]=4
                                                        else:
                                                            newBoardThird[firstRightX+2][firstRightY+2]=2
                                                        moves.append(newBoardThird)
                                            else:
                                                moves.append(newBoardSec)
                                        else:
                                            #second
                                            newBoardSec = copy.deepcopy(copyBoard)
                                            newBoardSec[newX][newY]=0
                                            newBoardSec[newX+1][newY+1]=0
                                            if canWeQueen(newX+2,1):
                                                newBoardSec[newX+2][newY+2]=4
                                            else:
                                                newBoardSec[newX+2][newY+2]=2
                                            firstRightX,firstRightY = newX+2, newY+2
                                            if isAttackAvailable(firstRightX,firstRightY,newBoardSec,2):
                                                secondLeftDirectionList = whereIsTheAttack(firstRightX,firstRightY,newBoardSec,2)
                                                for SLD in secondLeftDirectionList:
                                                    if SLD=="LEFT":
                                                        # third
                                                        newBoardThird = copy.deepcopy(newBoardSec)
                                                        newBoardThird[firstRightX][firstRightY]=0
                                                        newBoardThird[firstRightX+1][firstRightY-1]=0
                                                        if canWeQueen(firstRightX+2,1):
                                                            newBoardThird[firstRightX+2][firstRightY-2]=4
                                                        else:
                                                            newBoardThird[firstRightX+2][firstRightY-2]=2
                                                        moves.append(newBoardThird)
                                                    else:
                                                        # third
                                                        newBoardThird = copy.deepcopy(newBoardSec)
                                                        newBoardThird[firstRightX][firstRightY]=0
                                                        newBoardThird[firstRightX+1][firstRightY+1]=0
                                                        if canWeQueen(firstRightX+2,1):
                                                            newBoardThird[firstRightX+2][firstRightY+2]=2
                                                        else:
                                                            newBoardThird[firstRightX+2][firstRightY+2]=2
                                                        moves.append(newBoardThird)
                                            else:
                                                moves.append(newBoardSec)

                                else:
                                    moves.append(copyBoard)
                            else:
                                # first jump right
                                copyBoard = copy.deepcopy(board)
                                copyBoard[x][y]=0
                                copyBoard[x+1][y+1]=0
                                copyBoard[x+2][y+2]=2
                                if canWeQueen(x+2,1):
                                    copyBoard[x+2][y+2]=4
                                else:
                                    copyBoard[x+2][y+2]=2
                                newX,newY = x+2,y+2
                                if isAttackAvailable(newX,newY,copyBoard,2):
                                    firstRightBoard = whereIsTheAttack(newX,newY,copyBoard,2)
                                    for FRB in firstRightBoard:
                                        if FRB=="LEFT":
                                            # second
                                            secondBoard = copy.deepcopy(copyBoard)
                                            secondBoard[newX][newY]=0
                                            secondBoard[newX+1][newY-1]=0
                                            if canWeQueen(newX+2,1):
                                                secondBoard[newX+2][newY-2]=4
                                            else:
                                                secondBoard[newX+2][newY-2]=2
                                            secondRightX,secondRightY = newX+2,newY-2
                                            if isAttackAvailable(secondRightX,secondRightY,secondBoard,2):
                                                newSecondList = whereIsTheAttack(secondRightX,secondRightY,secondBoard,2)
                                                for NSL in newSecondList:
                                                    if NSL=="LEFT":
                                                        # third
                                                        thirdBoard = copy.deepcopy(secondBoard)
                                                        thirdBoard[secondRightX][secondRightY]=0
                                                        thirdBoard[secondRightX+1][secondRightY-1]=0
                                                        if canWeQueen(secondRightX+2,1):
                                                            thirdBoard[secondRightX+2][secondRightY-2]=4
                                                        else:
                                                            thirdBoard[secondRightX+2][secondRightY-2]=2
                                                        moves.append(thirdBoard)
                                                    else:
                                                        # third
                                                        thirdBoard = copy.deepcopy(secondBoard)
                                                        thirdBoard[secondRightX][secondRightY]=0
                                                        thirdBoard[secondRightX+1][secondRightY+1]=0
                                                        if canWeQueen(secondRightX+2,1):
                                                            thirdBoard[secondRightX+2][secondRightY+2]=4
                                                        else:
                                                            thirdBoard[secondRightX+2][secondRightY+2]=2
                                                        moves.append(thirdBoard)
                                            else:
                                                moves.append(secondBoard)
                                        else:
                                            # second
                                            secondBoard = copy.deepcopy(copyBoard)
                                            secondBoard[newX][newY]=0
                                            secondBoard[newX+1][newY+1]=0
                                            if canWeQueen(newX+2,1):
                                                secondBoard[newX+2][newY+2]=4
                                            else:
                                                secondBoard[newX+2][newY+2]=2
                                            secondRightX,secondRightY = newX+2,newY+2
                                            if isAttackAvailable(secondRightX,secondRightY,secondBoard,2):
                                                newSecondList = whereIsTheAttack(secondRightX,secondRightY,secondBoard,2)
                                                for NSL in newSecondList:
                                                    if NSL=="LEFT":
                                                        # third
                                                        thirdBoard = copy.deepcopy(secondBoard)
                                                        thirdBoard[secondRightX][secondRightY]=0
                                                        thirdBoard[secondRightX+1][secondRightY-1]=0
                                                        if canWeQueen(secondRightX+2,1):
                                                            thirdBoard[secondRightX+2][secondRightY-2]=4
                                                        else:
                                                            thirdBoard[secondRightX+2][secondRightY-2]=2
                                                        moves.append(thirdBoard)
                                                    else:
                                                        # third
                                                        thirdBoard = copy.deepcopy(secondBoard)
                                                        thirdBoard[secondRightX][secondRightY]=0
                                                        thirdBoard[secondRightX+1][secondRightY+1]=0
                                                        if canWeQueen(secondRightX+2,1):
                                                            thirdBoard[secondRightX+2][secondRightY+2]=4
                                                        else:
                                                            thirdBoard[secondRightX+2][secondRightY+2]=2
                                                        moves.append(thirdBoard)
                                            else:
                                                moves.append(secondBoard)
                                else:
                                    moves.append(copyBoard)
                elif board[x][y]==4:
                    direction,boolis = isAttackAvailableQueen(x,y,board,2)
                    upLeft=[]
                    upRight = []
                    downLeft = []
                    downRight = []
                    newX = x+1
                    newY = y+1
                    while isItInBounds(newX,newY) and board[newX][newY]==0:
                        movementBoard = copy.deepcopy(board)
                        movementBoard[x][y]=0
                        movementBoard[newX][newY]=4
                        downRight.append(movementBoard)
                        newX = newX+1
                        newY = newY+1


                    newX = x+1
                    newY = y-1
                    while isItInBounds(newX,newY) and board[newX][newY]==0:
                        movementBoard = copy.deepcopy(board)
                        movementBoard[x][y]=0
                        movementBoard[newX][newY]=4
                        downLeft.append(movementBoard)
                        newX = newX+1
                        newY = newY-1
                    

                    newX = x-1
                    newY = y+1
                    while isItInBounds(newX,newY) and board[newX][newY]==0:
                        movementBoard = copy.deepcopy(board)
                        movementBoard[x][y]=0
                        movementBoard[newX][newY]=4
                        upRight.append(movementBoard)
                        newX = newX-1
                        newY = newY+1
                    
                    newX = x-1
                    newY = y-1
                    while isItInBounds(newX,newY) and board[newX][newY]==0:
                        movementBoard = copy.deepcopy(board)
                        movementBoard[x][y]=0
                        movementBoard[newX][newY]=4
                        upLeft.append(movementBoard)
                        newX = newX-1
                        newY = newY-1
                    
                    for a in upLeft:
                        moves.append(a)
                    for a in upRight:
                        moves.append(a)
                    for a in downLeft:
                        moves.append(a)
                    for a in downRight:
                        moves.append(a)
                    # so we know we can attack
                    # we have the list of the attack 
                    if boolis==True:
                        for ggg in direction:
                            if ggg[0] == "up_right":
                                summ=0
                                for randomS in ggg[1]:
                                    if randomS==1 or randomS==3:
                                        summ=summ+1
                                        break
                                    else:
                                        summ=summ+1

                                
                                miniBoard = copy.deepcopy(board)
                                newX = x-summ
                                newY = y+summ
                                miniBoard[x][y]=0
                                miniBoard[newX][newY]=0
                                miniBoard[newX-1][newY+1]=4
                                brandNewX, brandNewY = newX-1,newY+1
                                newDir,newBoolis = isAttackAvailableQueen(brandNewX,brandNewY,miniBoard,2)
                                if newBoolis:
                                    newNewBoard = recursiveAttackQueen(brandNewX,brandNewY,miniBoard,2,newDir)
                                    moves.append(newNewBoard)
                                else:
                                    moves.append(miniBoard)

                            elif ggg[0] == "up_left":
                                summ=0
                                for randomS in ggg[1]:
                                    if randomS==1 or randomS==3:
                                        summ=summ+1
                                        break
                                    else:
                                        summ=summ+1
                                

                                miniBoard = copy.deepcopy(board)
                                newX = x-summ
                                newY = y-summ
                                miniBoard[x][y]=0
                                miniBoard[newX][newY]=0
                                miniBoard[newX-1][newY-1]=4
                                brandNewX, brandNewY = newX-1,newY-1
                                newDir,newBoolis = isAttackAvailableQueen(brandNewX,brandNewY,miniBoard,2)
                                if newBoolis:
                                    newNewBoard = recursiveAttackQueen(brandNewX,brandNewY,miniBoard,2,newDir)
                                    moves.append(newNewBoard)
                                else:
                                    moves.append(miniBoard)
                            elif ggg[0] == "dw_right":
                                summ=0
                                for randomS in ggg[1]:
                                    if randomS==1 or randomS==3:
                                        summ=summ+1
                                        break
                                    else:
                                        summ=summ+1
                                
                                miniBoard = copy.deepcopy(board)
                                newX = x+summ
                                newY = y+summ
                                miniBoard[x][y]=0
                                miniBoard[newX][newY]=0
                                miniBoard[newX+1][newY+1]=4
                                brandNewX, brandNewY = newX+1,newY+1
                                newDir,newBoolis = isAttackAvailableQueen(brandNewX,brandNewY,miniBoard,2)
                                if newBoolis:
                                    newNewBoard = recursiveAttackQueen(brandNewX,brandNewY,miniBoard,2,newDir)
                                    moves.append(newNewBoard)
                                else:
                                    moves.append(miniBoard)
                            elif ggg[0] == "dw_left":
                                summ=0
                                for randomS in ggg[1]:
                                    if randomS==1 or randomS==3:
                                        summ=summ+1
                                        break
                                    else:
                                        summ=summ+1

                                miniBoard = copy.deepcopy(board)
                                newX = x+summ
                                newY = y-summ
                                miniBoard[x][y]=0
                                miniBoard[newX][newY]=0
                                miniBoard[newX+1][newY-1]=4
                                brandNewX, brandNewY = newX+1,newY-1

                                newDir,newBoolis = isAttackAvailableQueen(brandNewX,brandNewY,miniBoard,2)
                                if newBoolis:
                                    newNewBoard = recursiveAttackQueen(brandNewX,brandNewY,miniBoard,2,newDir)
                                    moves.append(newNewBoard)
                                else:
                                    moves.append(miniBoard)
    return moves

def recursiveAttackQueen(x,y,board,player,direction):
    direction,boolis = isAttackAvailableQueen(x,y,board,player)
    moves = []

    if not boolis:
        return board

    if player==2:
        for ggg in direction:
            if ggg[0] == "up_right":
                summ=0
                for randomS in ggg[1]:
                    if randomS==2 or randomS==4:
                        summ=summ+1
                        break
                    else:
                        summ=summ+1

                
                miniBoard = copy.deepcopy(board)
                newX = x-summ
                newY = y+summ
                miniBoard[x][y]=0
                miniBoard[newX][newY]=0
                miniBoard[newX-1][newY+1]=4
                moves.append(miniBoard)

            elif ggg[0] == "up_left":
                summ=0
                for randomS in ggg[1]:
                    if randomS==1 or randomS==3:
                        summ=summ+1
                        break
                    else:
                        summ=summ+1
                    
                miniBoard = copy.deepcopy(board)
                newX = x-summ
                newY = y-summ
                miniBoard[x][y]=0
                miniBoard[newX][newY]=0
                miniBoard[newX-1][newY-1]=4
                moves.append(miniBoard)
            elif ggg[0] == "dw_right":
                summ=0
                for randomS in ggg[1]:
                    if randomS==1 or randomS==3:
                        summ=summ+1
                        break
                    else:
                        summ=summ+1
                
                miniBoard = copy.deepcopy(board)
                newX = x+summ
                newY = y+summ
                miniBoard[x][y]=0
                miniBoard[newX][newY]=0
                miniBoard[newX+1][newY+1]=4
                moves.append(miniBoard)
            elif ggg[0] == "dw_left":
                summ=0
                for randomS in ggg[1]:
                    if randomS==1 or randomS==3:
                        summ=summ+1
                        break
                    else:
                        summ=summ+1

                miniBoard = copy.deepcopy(board)
                newX = x+summ
                newY = y-summ
                miniBoard[x][y]=0
                miniBoard[newX][newY]=0
                miniBoard[newX+1][newY-1]=4
                moves.append(miniBoard)

        for mov in moves:
            for i in range(8):
                for j in range(8):
                    if player==1:
                        if mov[i][j]==3:
                            brandNewB = recQueen(i,j,mov,1)
                            return brandNewB
                    elif player==2:
                        if mov[i][j]==4:
                            brandNewB = recQueen(i,j,mov,2)
                            return brandNewB
        if moves!= []:
            return board
    elif player==1:
        if boolis==True:
            for ggg in direction:
                if ggg[0] == "up_right":
                    summ=0
                    for randomS in ggg[1]:
                        if randomS==2 or randomS==4:
                            summ=summ+1
                            break
                        else:
                            summ=summ+1

                    
                    miniBoard = copy.deepcopy(board)
                    newX = x-summ
                    newY = y+summ
                    miniBoard[x][y]=0
                    miniBoard[newX][newY]=0
                    miniBoard[newX-1][newY+1]=3
                    moves.append(miniBoard)
                elif ggg[0] == "up_left":
                    summ=0
                    for randomS in ggg[1]:
                        if randomS==2 or randomS==4:
                            summ=summ+1
                            break
                        else:
                            summ=summ+1
                        
                    miniBoard = copy.deepcopy(board)
                    newX = x-summ
                    newY = y-summ
                    miniBoard[x][y]=0
                    miniBoard[newX][newY]=0
                    miniBoard[newX-1][newY-1]=3
                    moves.append(miniBoard)
                elif ggg[0] == "dw_right":
                    summ=0
                    for randomS in ggg[1]:
                        if randomS==2 or randomS==4:
                            summ=summ+1
                            break
                        else:
                            summ=summ+1
                    
                    miniBoard = copy.deepcopy(board)
                    newX = x+summ
                    newY = y+summ
                    miniBoard[x][y]=0
                    miniBoard[newX][newY]=0
                    miniBoard[newX+1][newY+1]=3
                    moves.append(miniBoard)
                elif ggg[0] == "dw_left":
                    summ=0
                    for randomS in ggg[1]:
                        if randomS==2 or randomS==4:
                            summ=summ+1
                            break
                        else:
                            summ=summ+1

                    miniBoard = copy.deepcopy(board)
                    newX = x+summ
                    newY = y-summ
                    miniBoard[x][y]=0
                    miniBoard[newX][newY]=0
                    miniBoard[newX+1][newY-1]=3
                    moves.append(miniBoard)

        
        for mov in moves:
            for i in range(8):
                for j in range(8):
                    if player==1:
                        if mov[i][j]==3:
                            brandNewB = recQueen(i,j,mov,1)
                            return brandNewB
                    elif player==2:
                        if mov[i][j]==4:
                            brandNewB = recQueen(i,j,mov,2)
                            return brandNewB

def recQueen(x,y,board,player):
    direction,boolis = isAttackAvailableQueen(x,y,board,player)
    moves = []

    if not boolis:
        return board

    if player==2:
        for ggg in direction:
            if ggg[0] == "up_right":
                summ=0
                for randomS in ggg[1]:
                    if randomS==2 or randomS==4:
                        summ=summ+1
                        break
                    else:
                        summ=summ+1

                
                miniBoard = copy.deepcopy(board)
                newX = x-summ
                newY = y+summ
                miniBoard[x][y]=0
                miniBoard[newX][newY]=0
                miniBoard[newX-1][newY+1]=4
                moves.append(miniBoard)

            elif ggg[0] == "up_left":
                summ=0
                for randomS in ggg[1]:
                    if randomS==1 or randomS==3:
                        summ=summ+1
                        break
                    else:
                        summ=summ+1
                    
                miniBoard = copy.deepcopy(board)
                newX = x-summ
                newY = y-summ
                miniBoard[x][y]=0
                miniBoard[newX][newY]=0
                miniBoard[newX-1][newY-1]=4
                moves.append(miniBoard)
            elif ggg[0] == "dw_right":
                summ=0
                for randomS in ggg[1]:
                    if randomS==1 or randomS==3:
                        summ=summ+1
                        break
                    else:
                        summ=summ+1
                
                miniBoard = copy.deepcopy(board)
                newX = x+summ
                newY = y+summ
                miniBoard[x][y]=0
                miniBoard[newX][newY]=0
                miniBoard[newX+1][newY+1]=4
                moves.append(miniBoard)
            elif ggg[0] == "dw_left":
                summ=0
                for randomS in ggg[1]:
                    if randomS==1 or randomS==3:
                        summ=summ+1
                        break
                    else:
                        summ=summ+1

                miniBoard = copy.deepcopy(board)
                newX = x+summ
                newY = y-summ
                miniBoard[x][y]=0
                miniBoard[newX][newY]=0
                miniBoard[newX+1][newY-1]=4
                moves.append(miniBoard)

        for mov in moves:
            for i in range(8):
                for j in range(8):
                    if player==1:
                        if mov[i][j]==3:
                            brandNewB = recQueen(i,j,mov,1)
                            return brandNewB
                    elif player==2:
                        if mov[i][j]==4:
                            brandNewB = recQueen(i,j,mov,2)
                            return brandNewB
    elif player==1:
        if boolis==True:
            for ggg in direction:
                if ggg[0] == "up_right":
                    summ=0
                    for randomS in ggg[1]:
                        if randomS==2 or randomS==4:
                            summ=summ+1
                            break
                        else:
                            summ=summ+1

                    
                    miniBoard = copy.deepcopy(board)
                    newX = x-summ
                    newY = y+summ
                    miniBoard[x][y]=0
                    miniBoard[newX][newY]=0
                    miniBoard[newX-1][newY+1]=3
                    moves.append(miniBoard)
                elif ggg[0] == "up_left":
                    summ=0
                    for randomS in ggg[1]:
                        if randomS==2 or randomS==4:
                            summ=summ+1
                            break
                        else:
                            summ=summ+1
                        
                    miniBoard = copy.deepcopy(board)
                    newX = x-summ
                    newY = y-summ
                    miniBoard[x][y]=0
                    miniBoard[newX][newY]=0
                    miniBoard[newX-1][newY-1]=3
                    moves.append(miniBoard)
                elif ggg[0] == "dw_right":
                    summ=0
                    for randomS in ggg[1]:
                        if randomS==2 or randomS==4:
                            summ=summ+1
                            break
                        else:
                            summ=summ+1
                    
                    miniBoard = copy.deepcopy(board)
                    newX = x+summ
                    newY = y+summ
                    miniBoard[x][y]=0
                    miniBoard[newX][newY]=0
                    miniBoard[newX+1][newY+1]=3
                    moves.append(miniBoard)
                elif ggg[0] == "dw_left":
                    summ=0
                    for randomS in ggg[1]:
                        if randomS==2 or randomS==4:
                            summ=summ+1
                            break
                        else:
                            summ=summ+1

                    miniBoard = copy.deepcopy(board)
                    newX = x+summ
                    newY = y-summ
                    miniBoard[x][y]=0
                    miniBoard[newX][newY]=0
                    miniBoard[newX+1][newY-1]=3
                    moves.append(miniBoard)
        
        for mov in moves:
            for i in range(8):
                for j in range(8):
                    if player==1:
                        if mov[i][j]==3:
                            brandNewB = recQueen(i,j,mov,1)
                            return brandNewB
                    elif player==2:
                        if mov[i][j]==4:
                            brandNewB = recQueen(i,j,mov,2)
                            return brandNewB
        if moves!=[]:
            return board



if __name__ == "__main__":
    startGame()
    '''board = np.zeros((8,8),int)
    board[7,0]=1
    board[4,1]=1
    board[7,2]=4
    board[5,6]=1
    board[7,6]=1
    board[6,5]=3
    board[6,7]=1
    printBoard(board,2)
    mv = move(2,board)
    printBoard(mv,2)'''
    '''board = np.zeros((8,8),int)
    board[0][3]=2
    board[5][3]=4
    board[2][3]=1
    board[7][3]=1
    printBoard(board,2)
    strr = time.time()
    for i in range(50000):
        random.random
        getPossibleMoves(random.randint(1,2),board)
    print(time.time()-strr)'''