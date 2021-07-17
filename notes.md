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


Evaluation function notes:

1. Number of pawns; ✅
2. Number of kings;✅
3. Number of safe pawns (i.e. adjacent to the edge of the board); ✅
4. Number of safe kings;✅
5. Number of moveable pawns (i.e. able to perform a move other than capturing). ✅
6. Number of moveable kings. Parameters 5 and 6 are calculated taking no notice of capturing priority; ✅
7. Aggregated distance of the pawns to promotion line; TODO
8. Number of unoccupied fields on promotion line. ✅
Heuristics could also consider sums of or differences in respective parameters for both players rather than raw numbers for each player separately. Once heuristics using the straightforward parameters listed above had been generated and tested, it was decided that it would be desirable to add more sophisticated parameters characterizing layout of the pieces on the board. The following parameters were, therefore, introduced: 
9. Number of defender pieces2 (i.e. the ones situated in two lowermost rows); ✅
10. Number of attacking pawns (i.e. positioned in three topmost rows); ✅
11. Number of centrally positioned pawns (i.e. situated on the eight central squares of the board); ✅
12. Number of centrally positioned kings; ✅
13. Number of pawns positioned on the main diagonal; ✅
14. Number of kings positioned on the main diagonal; ✅
15. Number of pawns situated on double diagonal; ✅
16. Number of kings situated on double diagonal; ✅
17. Number of loner pawns. Loner piece is defined as the one not adjacent to any other 
piece; ✅
18. Number of loner kings; TODO
19. Number of holes, i.e. empty squares adjacent to at least three pieces of the same colour. TODO 
Apart from the above parameters six patterns were defined. They are described below using common notation presented in Fig. 2. Since only one instance of each pattern can exist for any of the players at the same time, features 20−25 can take only boolean values. 

1. 20. Presence of a Triangle pattern(see Fig. 3(a)). 
2. 21. Presence of an Oreo pattern (see Fig. 3(b)). 
3. 22. Presence of a Bridge pattern (see Fig. 3(c)). 
4. 23. Presence of a Dog pattern (see Fig. 3(d)). 
5. 24. Presence of a pawn in corner (i.e. White (Black) pawn on square 29 (4), resp.); 
6. 25. Presence of a king in corner (i.e. White (Black) king on square 4 (29), resp.); 

https://pages.mini.pw.edu.pl/~mandziukj/PRACE/es_init.pdf


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


## Changes 1.2.0

* Possible moves
    * bugs fixed

* Minimax
    * bugs fixed 
    * still player 2 doesnt play optimally
    * repeated moves 
    * TODO stop repeated moves and add random choices

* Evaluation
    * added a good evaluation function but it's very unoptimised

## Changes 1.2.1

* Overall
    * added 3 fold rule to check for repeating moves
    * Both players seem to play optimally