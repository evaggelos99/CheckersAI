## This is the board representation Numpy array

[

[0. 2. 0. 2. 0. 2. 0. 2.]

 [2. 0. 2. 0. 2. 0. 2. 0.]

 [0. 2. 0. 2. 0. 2. 0. 2.]

 [0. 0. 0. 0. 0. 0. 0. 0.]

 [0. 0. 0. 0. 0. 0. 0. 0.]

 [1. 0. 1. 0. 1. 0. 1. 0.]

 [0. 1. 0. 1. 0. 1. 0. 1.]

 [1. 0. 1. 0. 1. 0. 1. 0.]  ]


 ## useless shit

class Player:

    id=0

    def __init__(self,id):
        self.id=id

    def printNum(self):
        print(self.id)

    '''
    initial call:
    minimax(currentPosition, 3, -∞, +∞, true)
    '''
    def alphabeta(self,board,depth,alpha,beta,max):
        if gameIsSolved(board) or depth==0:
            return evaluationFun(board)
        
        player=0
        if max:
            player=1
        else:
            player=2
        
        if max:
            bestValue = -math.inf
            
            for move in getPossibleMoves(player,board=board):
                value = alphabeta(move,depth-1,alpha,beta, False)
                bestValue = max(bestValue, value)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return bestValue
            
        else:
            smallValue = math.inf
            for move in getPossibleMoves(player,board):
                value = alphabeta(move,depth-1,alpha,beta, True)
                smallValue = min(smallValue, value)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return smallValue



    def move(self,board):
        pass




[[0. 1. 0. 0. 0. 2. 0. 2.]
 [0. 0. 2. 0. 2. 0. 2. 0.]
 [0. 2. 0. 2. 0. 2. 0. 1.]
 [2. 0. 2. 0. 1. 0. 0. 0.]
 [0. 1. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 1. 0. 1. 0. 1. 0. 1.]
 [1. 0. 1. 0. 1. 0. 1. 0.]]


    board = getInitialBoard()
    board = np.zeros((8,8))
    board[0,1]=1
    board[0,5]=2
    board[0,7]=2

    board[1,2]=2
    board[1,4]=2
    board[1,6]=2

    board[2,1]=2
    board[2,3]=2
    board[2,5]=2
    board[2,7]=1

    board[3,0]=2
    board[3,2]=2
    board[3,4]=1
    
    board[4,1]=1

    board[6,1]=1
    board[6,3]=1
    board[6,5]=1
    board[6,7]=1

    board[7,0]=1
    board[7,2]=1
    board[7,4]=1
    board[7,6]=1



    board = np.zeros((8,8))

    board[1][3]=2
    board[2][2]=1
    board[4][2]=1
    print(board)
    print()
    moves = getPossibleMoves(1,board)
    for move in moves:
        print(move)
        print()



## Changes 1.1

* possible moves 
    * only allows 2 jumps this is wrong but its a start so i can get a minimum viable playable game
    * more jumps will be added
    * king promotion will happen aswell

* evaluation function 
    * is bare bones
    * paterns of checkers will be added later

* optimization 
    * this will be added when I have a better evaluation function and understand the game better and redo possible moves fun