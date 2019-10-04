#Yiyang Zeng yz3622
#CS4613 Artificial Intelligence Project

# Import necessary libs
import copy, pygame as pg

# Mode
debug = False
stat = True
debug_ab = False
debug_event = False
debug_dm = False
debug_hpm = False

# Game Settings
# Color constants
BLACK       = ( 53,  53,  53)
LIGHT       = (202, 202, 202)  # For highlighting
WHITE       = (255,  255,  255)
BG_COLOR_2  = (126,  87,  78) # Background colour 1
BG_COLOR_1  = (237, 221, 204) # Background colour 2
PIECECOLOR  = [WHITE, BLACK, LIGHT, LIGHT]

# Game graphics constants
FPS       = 30
TITLE     = "CS-UY 4613 Artificial Intelligence"
TILESIZE  = 80 # Tile sizes of the board.
PIECEPAD  = 5

# Font constants
FONTNAME = "monospace"
FONTSIZE = 30
FONTBOLD = True

# Lists containing the default positions of white/black checker locations
STARTING_BLACK_POSITIONS = [(0,0), (0,2), (0,4), (1,1), (1,3), (1,5)]
STARTING_WHITE_POSITIONS = [(4,0), (4,2), (4,4), (5,1), (5,3), (5,5)]

# All the legal actions a white piece can do.
LEGAL_BLACK_ACTIONS = [ (1, -1), (1, 1) ]

# All the legal actions a black piece can do.
LEGAL_WHITE_ACTIONS = [ (-1, 1), (-1, -1) ]

# Other constants
PLAYER_ONE  = 0
PLAYER_TWO  = 1
PLAYER_NONE = 2
DRAW        = 3
BOARD_ROWS  = 6
BOARD_COLS  = 6

# Result strings for when player wins.
PLAYER_NAMES = ["Smart AI", "Stupid Human", "None", "Draw"]
GAME_RESULT_STRING = ["Smart AI Wins!", "Stupid Human Wins!", "Game In Progress", "Game is a Draw!"]

# Different max search depth for different difficulties
DEPTH_FOR_DIFFICULTY = [1, 5, 9]

# A representation of the board.
class GameState:
    def __init__(self, rows, cols, firstplayer):
        self.__rows = rows  # number of rows in the board
        self.__cols = cols  # number of columns in the board
        self.__player = firstplayer  # the current player to move, 0 = Player One, 1 = Player Two

        # Initializes all the variables that help with putting and moving pieces.
        self.white_piece_list = copy.deepcopy(STARTING_WHITE_POSITIONS)  # All white pieces at bottom.
        self.black_piece_list = copy.deepcopy(STARTING_BLACK_POSITIONS)  # All black pieces at top.

    # These are getter functions used to get private variables such as self.__rows.
    def cols(self):
        return self.__cols  # number of columns in board

    def rows(self):
        return self.__rows  # number of rows in board

    def player_to_move(self):
        return self.__player  # the player to move next

    def opponent(self, player):
        return (player + 1) % 2  # return the opponent's value

    # Check if a move is legal.
    def is_legal(self, move):
        if debug:
            print("Check if ", move, " is legal")

        if move is None:
            if debug:
                print(move, "is None")
            return False

        # If the move is on tile with a white piece, then it's not legal.
        if move in self.white_piece_list:
            if debug:
                print(move, "is already a white piece")
            return False

        # If the move is on tile with a black piece, then it's not legal.
        if move in self.black_piece_list:
            if debug:
                print(move, "is already a black piece")
            return False

        # Check if the row position is within bounds.
        if move[0] < 0 or move[0] >= BOARD_ROWS:
            if debug:
                print(move, "is out of row bound")
            return False

        # Check if the column position is within bounds.
        if move[1] < 0 or move[1] >= BOARD_COLS:
            if debug:
                print(move, "is out of column bound")
            return False

        # Previously checks were false so tile must be legal.
        return True

    # This will execute a move when passed a new row/column location.
    def do_move(self, new_pos, to_remove, checker):

        if debug_dm:
            print("new_pos is ", new_pos, ", piece is", checker, "to_remove is", to_remove)

        # If the move is illegal, then return.
        if not self.is_legal(new_pos):
            self.__player = self.opponent(self.__player)
            if debug_dm:
                print("DOING ILLEGAL MOVE")
            return

        # If the player is white then execute his move.
        if self.__player == 0:
            if debug_dm:
                print("AI (Player 0) playing")
            # If a jump was executed, removed the element jumped.
            for piece in to_remove:
                # If the piece's action to get there is the same as we used to get here then remove it.
                if piece[1] == new_pos and piece[2] == checker:
                    if debug_dm:
                        print("Jump over and remove ", piece[0])
                    self.black_piece_list.remove(piece[0])  # Remove from board.

            # Grab index of selected tile.
            piece_index = self.white_piece_list.index(checker)

            # Update the position of the checker
            self.white_piece_list[piece_index] = new_pos

        # If the player is black then execute his move.
        if self.__player == 1:
            if debug_dm:
                print("Human (Player 1) playing")
            # If a jump was executed, removed the element jumped..
            for piece in to_remove:
                # If the piece's action to get there is the same as we used to get here then remove it.
                if piece[1] == new_pos and piece[2] == checker:
                    if debug_dm:
                        print("Jump over and remove ", piece[0])
                    self.white_piece_list.remove(piece[0])  # Remove from board.
                    break

            # Grab index of selected tile
            piece_index = self.black_piece_list.index(checker)
            if debug_dm:
                print("Replacing", self.black_piece_list[piece_index], "with", new_pos)
            # Update the position of the checker
            self.black_piece_list[piece_index] = new_pos

        if debug_dm:
            print("After moving, black_list:", self.black_piece_list, "white_list:", self.white_piece_list)
        # Swap players so the next player gets the turn.
        self.__player = self.opponent(self.__player)

    # Undo the last done move in the gamestate.
    def undo_move(self, j_done_move, j_deleted_move):

        if debug:
            print("------------ undo_move ------------")
        if self.__player == 0:
            # Remove the new postion piece and add the old position back in.
            if debug:
                print("player is ", 0)
                print("self.just_done_move is ", j_done_move)

            # Undo the move
            piece_index = self.black_piece_list.index(j_done_move[0])
            self.black_piece_list[piece_index] = j_done_move[1]

            # If we deleted a piece then put it back in.
            if j_deleted_move is not None:
                self.white_piece_list.append(j_deleted_move)

        # If the player is black, undo the white move and pass it to white.
        elif self.__player == 1:
            # Remove the new postion piece and add the old position back in.
            if debug:
                print("player is ", 1)
                print("self.just_done_move is ", j_done_move)
            piece_index = self.white_piece_list.index(j_done_move[0])
            self.white_piece_list[piece_index] = j_done_move[1]

            # If we deleted a piece then put it back in.
            if j_deleted_move is not None:
                self.black_piece_list.append(j_deleted_move)

        # Give the opponent back his turn.
        self.__player = self.opponent(self.__player)

    # When a player selects a piece, this function will highlight all the potential moves around it.
    def highlight_potential_moves(self, tile):
        if debug_hpm:
            print("----------------------------------- HIGHLIGHT ----------------------------------- ")
            print("player is ", self.__player)
        potential_move_list = []
        to_remove_list = []
        has_jump = False

        # Grab potential_moves depending on the player.
        # White piece player
        if self.__player == 0:
            # If the tile pressed isn't white, then return.
            if debug_hpm:
                print("tile is ", tile)
            if tile not in self.white_piece_list:
                if debug_hpm:
                    print("Didn't click on white tile")
                return

            # Loop through all legal white actions to add them as potential moves.
            for action in LEGAL_WHITE_ACTIONS:
                # The new postion of the piece.
                new_row = tile[0] + action[0]
                new_col = tile[1] + action[1]
                temp_piece = (new_row, new_col)

                # If the temp location is on a black piece, check if jump exists.
                if temp_piece in self.black_piece_list:
                    # The possible jump column will change depending on the action taken.
                    # possible jump row will remain the same.
                    possible_jump_row = temp_piece[0] + action[0]
                    possible_jump_col = temp_piece[1] + action[1]

                    # Where we'll be jumping to if the spot is legal.
                    possible_jump = (possible_jump_row, possible_jump_col)
                    if debug_hpm:
                        print(possible_jump, "is a possible jump move for", tile)
                    if self.is_legal(possible_jump):
                        # If this move is a legal jump move, then clear the list and add the jump move

                        if not has_jump:
                            potential_move_list.clear()
                            has_jump = True

                        if debug_hpm:
                            print("Add jump move", possible_jump, "to the list")
                        potential_move_list.append(possible_jump)

                        # We remove the jumped piece by using this list.
                        to_remove_list.append((temp_piece, possible_jump, tile))
                    continue
                else:
                    # The regular move is added to list only when there is no jump move
                    if self.is_legal(temp_piece) and not has_jump:
                        if debug_hpm:
                            print("Add regular move", temp_piece, "to the list")
                        potential_move_list.append(temp_piece)

        # Black piece player # not used because it's a human player
        if (self.__player == 1):
            # If the tile pressed isn't black, then return.
            if debug_hpm:
                print("tile is ", tile)
            if tile not in self.black_piece_list:
                if debug_hpm:
                    print("Didn't click on black tile")
                return

            # Loop through all legal black actions to add them as potential moves.
            for action in LEGAL_BLACK_ACTIONS:
                # The new postion of the piece.
                new_row = tile[0] + action[0]
                new_col = tile[1] + action[1]
                temp_piece = (new_row, new_col)

                # If the temp location is on a black piece, check if jump exists.
                if temp_piece in self.white_piece_list:
                    # The possible jump column will change depending on the action taken.
                    # possible jump row will remain the same.
                    possible_jump_row = temp_piece[0] + action[0]
                    possible_jump_col = temp_piece[1] + action[1]

                    # Where we'll be jumping to if the spot is legal.
                    possible_jump = (possible_jump_row, possible_jump_col)
                    if self.is_legal(possible_jump):
                        if not has_jump:
                            potential_move_list.clear()
                            has_jump = True

                        # It's now a potential move
                        if debug_hpm:
                            print("Add jump move", possible_jump, "to the list")
                        potential_move_list.append(possible_jump)

                        # We remove the jumped piece by using this list.
                        to_remove_list.append((temp_piece, possible_jump, tile))
                    continue
                else:
                    # The temp_piece is now added to list.
                    if self.is_legal(temp_piece) and not has_jump:
                        if debug_hpm:
                            print("Add regular move", temp_piece, "to the list")
                        potential_move_list.append(temp_piece)

        return potential_move_list, to_remove_list

    # Search and decide whether the piece has any legal move left
    def if_has_legal_move(self, piece, player):
        if debug:
            print(piece, " has legal move?")

        # Grab potential_moves depending on the player.
        # White piece player
        if player == 0:

            # Loop through all legal white actions to add them as potential moves.
            for action in LEGAL_WHITE_ACTIONS:
                # The new postion of the piece.
                new_row = piece[0] + action[0]
                new_col = piece[1] + action[1]
                temp_piece = (new_row, new_col)

                # If the temp location is on a black piece, check if jump exists.
                if temp_piece in self.black_piece_list:
                    # The possible jump column will change depending on the action taken.
                    # possible jump row will remain the same.
                    possible_jump_row = temp_piece[0] + action[0]
                    possible_jump_col = temp_piece[1] + action[1]

                    # Where we'll be jumping to if the spot is legal.
                    possible_jump = (possible_jump_row, possible_jump_col)
                    if self.is_legal(possible_jump):
                        # It's now a potential move.
                        return True
                    continue
                else:
                    # The temp_piece is now added to list.
                    if self.is_legal(temp_piece):
                        return True

        # Black piece player
        if (player == 1):

            # Loop through all legal black actions to add them as potential moves.
            for action in LEGAL_BLACK_ACTIONS:
                # The new postion of the piece.
                new_row = piece[0] + action[0]
                new_col = piece[1] + action[1]
                temp_piece = (new_row, new_col)


                # If the temp location is on a black piece, check if jump exists.
                if temp_piece in self.white_piece_list:

                    # The possible jump column will change depending on the action taken.
                    # possible jump row will remain the same.
                    possible_jump_row = temp_piece[0] + action[0]
                    possible_jump_col = temp_piece[1] + action[1]

                    # Where we'll be jumping to if the spot is legal.
                    possible_jump = (possible_jump_row, possible_jump_col)
                    if self.is_legal(possible_jump):
                        # It's now a potential move
                        return True
                    continue
                else:
                    if self.is_legal(temp_piece):
                        return True
        if debug:
            print(piece, " has no legal move")
        return False

    # Test if a checker has a jump move.
    def if_has_jump_move(self, piece, player):
        if debug_event:
            print(piece, " has jump move?")

        # Black piece player
        if player == 1:

            # Loop through all legal black actions to add them as potential moves.
            for action in LEGAL_BLACK_ACTIONS:
                # The new postion of the piece.
                new_row = piece[0] + action[0]
                new_col = piece[1] + action[1]
                temp_piece = (new_row, new_col)

                # If the temp location is on a black piece, check if jump exists.
                if temp_piece in self.white_piece_list:

                    # The possible jump column will change depending on the action taken.
                    # possible jump row will remain the same.
                    possible_jump_row = temp_piece[0] + action[0]
                    possible_jump_col = temp_piece[1] + action[1]

                    # Where we'll be jumping to if the spot is legal.
                    possible_jump = (possible_jump_row, possible_jump_col)
                    if self.is_legal(possible_jump):
                        # It's now a potential move
                        return True
        else:
            # Loop through all legal black actions to add them as potential moves.
            for action in LEGAL_WHITE_ACTIONS:
                # The new postion of the piece.
                new_row = piece[0] + action[0]
                new_col = piece[1] + action[1]
                temp_piece = (new_row, new_col)

                # If the temp location is on a black piece, check if jump exists.
                if temp_piece in self.black_piece_list:

                    # The possible jump column will change depending on the action taken.
                    # possible jump row will remain the same.
                    possible_jump_row = temp_piece[0] + action[0]
                    possible_jump_col = temp_piece[1] + action[1]

                    # Where we'll be jumping to if the spot is legal.
                    possible_jump = (possible_jump_row, possible_jump_col)
                    if self.is_legal(possible_jump):
                        # It's now a potential move
                        return True
        if debug_event:
            print(piece, " has no jump move")
        return False

    # Decides the winner of the game
    def winner(self):
        if len(self.black_piece_list) <= 0:
            if debug:
                print("P1 wins by eliminating the opponent's checkers")
            return PLAYER_ONE

        elif len(self.white_piece_list) <= 0:
            if debug:
                print("P2 wins by eliminating the opponent's checkers")
            return PLAYER_TWO

        for white_piece in self.white_piece_list:
            if self.if_has_legal_move(white_piece, 0):
                return PLAYER_NONE

        for black_piece in self.black_piece_list:
            if self.if_has_legal_move(black_piece, 1):
                return PLAYER_NONE

        if len(self.black_piece_list) < len(self.white_piece_list):
            if debug:
                print("P1 wins by having more checkers")
            return PLAYER_ONE

        elif len(self.black_piece_list) > len(self.white_piece_list):
            if debug:
                print("P2 wins by having more checkers")
            return PLAYER_TWO

        elif len(self.black_piece_list) == len(self.white_piece_list):
            if debug:
                print("Draw")
            return DRAW

        else:
            if debug:
                print("No one wins!")
            return PLAYER_NONE

    # The evaluation of terminal states and cutoffs.
    def eval(self, player):
        if debug:
            print("in eval")
        score = 0

        if (self.winner() == player):
            score = 1000
            if debug:
                print("winning move")
            return score

        elif (self.winner() == ((player + 1) % 2)):
            score = -1000
            if debug:
                print("losing move")
            return score

        else:
            if player == PLAYER_ONE:
                # evaluation for player 1
                score += (len(self.white_piece_list) - len(self.black_piece_list))  # check difference in num pieces
                return score

            else:
                # evaluation for player 2
                score += (len(self.black_piece_list) - len(self.white_piece_list))  # check difference in num pieces
                return score


# Alphabeta search.
class AlphaBeta:
    def __init__(self, max_depth=6):
        self.max_depth = max_depth  # set the max depth of search
        self.player = None
        self.best_move = None  # record the best move found so far
        self.best_move_to_remove_list = None  # record the possible removal of checkers found so far
        self.piece = None  # record the checker taking a move
        self.max_tree_depth = 0  # record stat
        self.num_of_nodes = 0  # record stat
        self.num_of_pruning_max = 0  # record stat
        self.num_of_pruning_min = 0  # record stat
        self.reset()  # Initialize the tree

        if debug:
            print('Initailize player alpha beta search')

    # Reset all appropriate values so alphabeta can be freshly called again.
    def reset(self):
        self.best_move = None
        self.best_move_to_remove_list = None
        self.piece = None
        self.max_tree_depth = 0
        self.num_of_nodes = 0
        self.num_of_pruning_max = 0
        self.num_of_pruning_min = 0

    def get_move(self, state):
        # reset the variables
        self.reset()
        # store the player that we're deciding a move for and set it as a class variable
        self.player = state.player_to_move()
        # do your alpha beta (or ID-AB) search here
        ab_value = self.alpha_beta(state, 0, -1000000, 1000000, True)
        if stat:
            print("--------------------------------------")
            print("Maximum depth: ", self.max_tree_depth, "\nTotal number of nodes generated: ", self.num_of_nodes,
                  "\nNumber of pruning in MAX: ", self.num_of_pruning_max, "\nNumber of pruning in MIN: ",
                  self.num_of_pruning_min)
        # return the best move computer by alpha_beta

        return self.best_move, self.best_move_to_remove_list, self.piece
        # Return the best move and the captured piece(if exist)
        # elif (state.player_to_move() == 1):

    def is_terminal(self, state, depth):
        # Cutoff when max depth is reached
        if depth >= self.max_depth:
            if depth > self.max_tree_depth:
                self.max_tree_depth = depth
            return True

        # Terminal state
        if state.winner() != PLAYER_NONE:
            if depth > self.max_tree_depth:
                self.max_tree_depth = depth
            return True
        return False

    def alpha_beta(self, state, depth, alpha, beta, max_player):
        # If terminal then return the evaluation.
        if self.is_terminal(state, depth):
            if debug:
                print('its terminal')
            return state.eval(self.player)

        if debug:
            print("player is ", state.player_to_move())

        if max_player:
            value = -10000
        else:
            value = 10000

        # Look for best move if white piece.
        piece_list = copy.deepcopy(state.white_piece_list if state.player_to_move() == 0 else state.black_piece_list)
        for piece in piece_list:
            # Get the possible moves
            piece_potential_move_list, piece_to_remove_list = state.highlight_potential_moves(piece)
            if debug_ab and depth == 0:
                print(piece, "has potential moves", piece_potential_move_list)
            for move in piece_potential_move_list:
                # Do the move in the game state
                self.num_of_nodes += 1
                state.do_move(move, piece_to_remove_list, piece)
                temp_jd_move = (move, piece)

                # Find out if a checker is just deleted. If so, store it
                temp_just_deleted = None
                for to_remove_piece in piece_to_remove_list:
                    # If the piece's action to get there is the same as we used to get here then remove it.
                    if to_remove_piece[1] == temp_jd_move[0] and to_remove_piece[2] == piece:
                        temp_just_deleted = to_remove_piece[0]

                val = self.alpha_beta(state, depth + 1, alpha, beta, not max_player)

                if debug_ab:
                    print("to_remove_list is", piece_to_remove_list)

                # Undo the move to restore the game state to its original state for the next iteration
                state.undo_move(temp_jd_move, temp_just_deleted)

                # Max
                if max_player:
                    if depth == 0:
                        if debug_ab:
                            print("----",piece, "can move to", move, "which can remove", piece_to_remove_list,
                                  "when white has", state.white_piece_list, "and black has", state.black_piece_list,
                                  "and potential moves", piece_potential_move_list)

                        # When there is no best move yet, do a fair comparison
                        if self.best_move is None:
                            self.best_move = temp_jd_move[0]
                            self.best_move_to_remove_list = piece_to_remove_list
                            self.piece = piece
                            if debug_ab:
                                print("-------Current best move found: move", self.piece, "to", self.best_move,
                                      "with value of", val)

                        # When both of the moves are both jump moves or are both regular moves, do a fair comparison
                        if len(self.best_move_to_remove_list) > 0 and len(piece_to_remove_list) > 0 or \
                            len(self.best_move_to_remove_list) <= 0 and len(piece_to_remove_list) <= 0:
                            if val > value:
                                self.best_move = temp_jd_move[0]
                                self.best_move_to_remove_list = piece_to_remove_list
                                self.piece = piece
                                if debug_ab:
                                    print("-------Current best move found: move", self.piece, "to", self.best_move,
                                          "with value of", val)

                        # When the new move is a jump move while the old one is not, favor the new one
                        elif len(self.best_move_to_remove_list) <= 0 and len(piece_to_remove_list) > 0:
                            self.best_move = temp_jd_move[0]
                            self.best_move_to_remove_list = piece_to_remove_list
                            self.piece = piece
                            if debug_ab:
                                print("-------Current best move found: move", self.piece, "to", self.best_move,
                                      "with value of", val)

                    value = max(value, val)
                    alpha = max(alpha, value)
                # MIN
                else:
                    value = min(value, val)
                    beta = min(value, beta)

                if debug_ab:
                    print("Potential move is", move, "at ", "MAX" if max_player else "MIN",
                          "with value =", val, ", alpha =", alpha, ", beta =", beta)

                # Pruning
                if alpha >= beta:
                    if debug_ab:
                        print("Pruning at ", "MAX" if max_player else "MIN", "with alpha = ", alpha,
                              ", beta = ", beta)
                    if max_player:
                        self.num_of_pruning_max += 1
                    else:
                        self.num_of_pruning_min += 1
                    break
        if depth == 0 and self.best_move is None and debug_ab:
            print("Available pieces are", piece_list)
            for i in piece_list:
                piece_potential_move_list, piece_to_remove_list = state.highlight_potential_moves(i)
                print("For", i, "available moves are", piece_potential_move_list, "to remove list is", piece_to_remove_list)
        return value

# The basic Checkers class.
class MiniCheckers:
    # The init function where we initalize important information about pygame and checkers.
    def __init__(self):
        if debug:
            print("--------- Initialize the game ---------")
        text = input("Do you want to play first?(y/n)")
        if text == "y":
            playfirst = 1
        else:
            playfirst = 0

        difficulty = input("Which difficulty do you want?(1-3)")
        AIplayer = AlphaBeta(DEPTH_FOR_DIFFICULTY[(int(difficulty) - 1) % 3 if difficulty.isdigit() else 1])

        pg.init()  # This initializes pygame, must be done.
        pg.display.set_caption(TITLE)  # Sets title of the window as defined in settings.
        self.clock = pg.time.Clock()  # Used to set the FPS.
        self.game_state = GameState(BOARD_ROWS, BOARD_COLS, playfirst)  # Used to display the GUI
        self.width = self.game_state.cols() * TILESIZE  # Width of screen.
        self.height = self.game_state.rows() * TILESIZE + 40  # Height of screen.
        self.screen = pg.display.set_mode((self.width, self.height))  # Window Size.
        self.font = pg.font.SysFont(FONTNAME, FONTSIZE, bold=FONTBOLD)  # Used later.
        self.winner = PLAYER_NONE  # Won't need to worry about this for now.
        self.text_position = (10, self.height - 35)  # Used later.
        self.players = [AIplayer, None]
        self.flip_color = True  # Used to switch background colors when drawing the board.
        self.black_piece_potential_move_list = []  # For human player move
        self.black_pieces_to_remove_list = []  # For human player move
        self.player_selected = None  # For human player move

    # The main game update loop of the application
    def update(self):
        # This sets a limit on how fast our computers process the drawing code.\
        self.dt = self.clock.tick(FPS) / 1000
        self.do_turn()
        self.events()  # This will check for any input.
        self.draw()  # Draw everything on the screen.

    # This will draw everything on the screen.
    def draw(self):
        # Add another parameter for king color.
        self.draw_board()  # Draw the basic checkerboard for the background.

        # Determine if there's a winner.
        player = self.game_state.player_to_move()
        if self.winner == PLAYER_NONE:
            self.draw_text(PLAYER_NAMES[player] + (" Thinking" if self.players[player] is None else " Thinking"),
                           self.text_position, PIECECOLOR[player])
        else:
            self.draw_text(GAME_RESULT_STRING[self.winner], self.text_position, PIECECOLOR[self.winner])

        self.draw_piece_list(self.screen, self.game_state.white_piece_list, WHITE, 2)  # Draw all the white pieces.
        self.draw_piece_list(self.screen, self.game_state.black_piece_list, BLACK, 2)  # Draw all the black pieces.

        # If a player has pressed down on a piece then highlight potential moves.
        self.draw_piece_list(self.screen, self.black_piece_potential_move_list, LIGHT,
                             2)  # Draw all potential black moves on board.
        pg.display.flip()  # Paint the graphics to the screen.

    # This will draw the checkered background of the checkers screen.
    def draw_board(self):
        # This must always be reinitialized or else colors will constantly be flashing.
        self.flip_color = True
        self.screen.fill(BG_COLOR_1)  # Fill the Background to BG Colour 2.

        # Draw all the tiles on the screen.
        # Fill the part of the screen(like paintbucket in MS Paint/Photoshop) to fill in the checkerboard.
        for c in range(self.game_state.cols()):
            for r in range(self.game_state.rows()):
                # Draw a colored tile on the screen depending on flip_color value.
                if self.flip_color:
                    self.screen.fill(BG_COLOR_1, (c * TILESIZE, r * TILESIZE, TILESIZE * 1, TILESIZE * 1))
                    self.flip_color = False  # Draw the next tile a different color.
                else:
                    self.screen.fill(BG_COLOR_2, (c * TILESIZE, r * TILESIZE, TILESIZE * 1, TILESIZE * 1))
                    self.flip_color = True  # Draw the next tile a different color.

            # Flip the color again so the next column starts with a different color.
            self.flip_color = not self.flip_color

            # This will draw a list of pieces on a board using a list of tuples.

    def draw_piece_list(self, surface, piece_list, color, border):
        # For every piece in given list, draw a piece at that row and column.
        for piece in piece_list:
            row, col = self.game_state.rows() - 1 - piece[0], piece[1]

            pg.draw.circle(surface, color, (col * TILESIZE + TILESIZE // 2, row * TILESIZE + TILESIZE // 2),
                           TILESIZE // 2 - PIECEPAD)

    # draw some text with the given arguments
    def draw_text(self, text, pos, color):
        label = self.font.render(text, 1, color)
        self.screen.blit(label, pos)

    # This will execute a move when passed a new row/column location.
    def take_move(self, move, to_remove, checker):
        player = self.game_state.player_to_move()
        if debug:
            print("-------- take move --------")
            print("player ", player, " moves to ", move)

        if debug:
            print("do move", move)
        # Check for winner and do move.
        self.winner = self.game_state.winner()
        self.game_state.do_move(move, to_remove, checker)

    # This function will do a basic move
    def do_turn(self):
        self.winner = self.game_state.winner()
        if self.winner == PLAYER_NONE:  # there is no winner yet, so get the next move from the AI
            player = self.game_state.player_to_move()  # get the next player to move from the state

            if self.players[player] is not None:  # if the current player is an AI, get its move
                best_move, to_remove, checker = self.players[player].get_move(self.game_state)
                self.take_move(best_move, to_remove, checker)  # Get an alpha beta move.

    # Returns the tile (r,c) on the grid underneath a given mouse position in pixels
    def get_tile(self, mpos):
        return (mpos[1] // TILESIZE, mpos[0] // TILESIZE)

    # This function will handle all user input handling.
    def events(self):

        # Loop through every event occuring.
        for event in pg.event.get():
            # If user hit the X button on window, then quit.
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            # Only detect a mouse input when the human player is taking the turn
            if self.game_state.player_to_move() == 1:

                # Check if the player has any legal move, if not then skip the turn
                has_move = False
                for piece in self.game_state.black_piece_list:
                    if self.game_state.if_has_legal_move(piece, 1):
                        has_move = True
                        break
                if not has_move:
                    self.take_move(None, None, None)

                # Check if a mousebutton is pressed down.
                if event.type == pg.MOUSEBUTTONDOWN:
                    if pg.mouse.get_pressed()[0]:
                        move = self.get_tile(event.pos)
                        repositioned_row = move[0] - (BOARD_ROWS - 1)
                        move = (abs(repositioned_row), move[1])

                        # If player clicked on a potential move then move checker to the position.
                        if (move in self.black_piece_potential_move_list) and self.winner == PLAYER_NONE:
                            if debug_event:
                                print("Click move: ", move)
                            self.take_move(move, self.black_pieces_to_remove_list, self.player_selected)
                            self.player_selected = None
                            self.black_piece_potential_move_list = []
                            self.black_pieces_to_remove_list = []
                            continue

                        # If player didn't click on potential move then show them instead.
                        if debug_event:
                            print("Click select: ", move)
                        if move in self.game_state.black_piece_list:

                            # Check if there is any jump move available. If so, don't allow any regular move
                            has_jump = self.game_state.if_has_jump_move(move, 1)
                            can_show = True
                            if not has_jump:
                                for piece in self.game_state.black_piece_list:
                                    if self.game_state.if_has_jump_move(piece, 1):
                                        can_show = False
                                        if debug_event:
                                            print(piece, "can jump,", move, "is not allowed to move")
                                        break
                            if can_show:
                                if debug_event and has_jump:
                                    print(move, "can jump so can move!")
                                if debug_event and not has_jump:
                                    print(move, "can move and other cannot jump!")
                                self.player_selected = move
                                self.black_piece_potential_move_list, self.black_pieces_to_remove_list = \
                                    self.game_state.highlight_potential_moves(move)
                            else:
                                self.player_selected = None
                                self.black_piece_potential_move_list = []
                                self.black_pieces_to_remove_list = []


# The basic game object
game = MiniCheckers()

# The game loop
while True:
    game.update()
