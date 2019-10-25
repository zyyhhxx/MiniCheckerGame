# MiniCheckerGame
 A mini checker game with a GUI and an AI using alpha-beta tree with pruning

# How to compile and run
This project uses a Python GUI library PyGame, so this library is required to run the project. The
file pygame-1.9.3.tar.gz can be easily installed with the instruction [here](https://www.pygame.org/wiki/GettingStarted).
Then run the python file mini-checkers.py directly. 

# How the game works
In the beginning of the game, you need to first decide if you want to play first (y/n) and the difficulty of the game (1-3). Any unreasonable answer will be interpreted as no and difficulty 2 for two questions respectively.

After the game starts, click on a checker, then you can see the highlighted possible moves. Click on the highlighted possible move to take the move. The bottom bar is a console in which all messages are displayed. 

![Figure 1](https://i.imgur.com/djrIMYe.png)

Human and AI will take turns, until one side loses all checkers or both sides cannot move any
checker. Then a victory or draw will be decided. 

![Figure 2](https://i.imgur.com/fHe2Zu4.png)

# A high level description of the design

There are three classes in the design: **GameState**, **AlphaBeta**, **MiniCheckers**

**GameState** is a representation of the current board which provides functions:
* To access information:
  * The list of all black checkers
  * The list of all white checkers
  * The player who is currently taking a move
  * The possible moves for a specific checker
  * The evaluation of the current board (for both cutoffs and terminal states)
  
* To check conditions:
  * If a move is legal
  * If a checker has a legal move
  * If a checker has a legal capture move
  * If a player wins the game

* To make change to the board:
  * Do a move
  * Undo a move
  
**AlphaBeta** is a representation of the alpha-beta search tree which provides functions:

* To get the best move using alpha-beta search
  * A fair comparison between two moves is made only when the moves are both
regular moves or both are capture moves
  * If a regular move is compared to a capture move, the search will favor the
capture move to make sure that the AI definitely takes a capture move when
possible

* To clear the tree (because the instance is reused)

* To check if a terminal state is reached or a cutoff is needed

**MiniCheckers** is a representation of the mini-checkers game which provides functions:
* To get necessary information to set up the game (including who plays first and the
difficulty of the game)
* To draw the board, the checkers and the highlighted moves
* To display texts at the bottom
* To make a move
* To get input from the human player and convert it to a move
* To control the flow of the game

After the game is started, an infinite loop will be created to repeatedly to:
1. Update the game: to ask either the AI (the alpha-beta search) or the human for input to
make a move
2. To draw the board and checkers, and maybe highlighted checkers

# Definition of terminal states

The game state is a terminal state when one of the following is satisfied:
* The checkers of one side is eliminated
* The checkers of both sides do not have any legal move
The utility value is calculated in the following ways:
* If the player wins in the state, the value is 1000
* If the player loses in the state, the value is -1000
* Otherwise, the value is (the number of checkers of the player – the number of checkers
of the opponent)

# Evaluation function and cutoff

The maximum depth of the cutoff is set to 9. Be aware that this depth is very demanding for
average laptops in my implementation.

The evaluation function is (the number of checkers of the player – the number of checkers of
the opponent), simply because a state in which the player has more checkers is more favorable. 

# Different levels of difficulty

At level 3, the maximum depth of the cutoff is set to 9 for maximum smartness of the AI. At
level 2, the maximum depth of the cutoff is set to 5 for average smartness of the AI. At level 1,
the maximum depth of the cutoff is set to 1 for minimum smartness of the AI.
