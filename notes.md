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

## With kings representations
[[0 0 3 0 0 0 0 0]
 [0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0]
 [0 0 4 0 0 0 0 0]]


 ## Code that might be needed for more debugging
    
    board = np.zeros((8,8))
    board[5][3]=1
    board[3][3]=1
    board[1][3]=1
    board[0][4]=2
    printBoard(board)
    for move in getPossibleMoves(2,board):
        printBoard(move)

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


    board = np.zeros((8,8))

    board[7][3]=1
    board[6][2]=2
    board[4][2]=2
    board[2][2]=2

    printBoard(board)
    for move in getPossibleMoves(1,board):
        printBoard(move)


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

## Changes 1.1.1

* Minimax
    * alphabeta prunning algorithm had some bugs didnt go to depth

* General
    * Player 1 doesnt play optimal for some reason don't know why. It could be because i switch the players and some bugs happen. Don't know where in code tho

## Changes 1.1.2

* possible moves
    * it allows 3 jumps which is the maximum you can jump

* bugs
    * goes out of bounds. Need to check my helper functions or maybe remake them cause some are not efficient -> this is gonna be done later who am I kidding 😅

## Changes 1.1.3

* possible moves
    * bugs fixed
    * no more out of bounds 

