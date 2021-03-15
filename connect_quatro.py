BOARD_LENGTH = 8
BOARD_HEIGHT = 6

CHAR_BLANK = '0'
CHAR_WIN = '*'
CHAR_ONE = '1'
CHAR_TWO = '2'

GO_FIRST = CHAR_ONE

class Board:
    def __init__(self, user_bx: int, user_by: int):
        """Attributes:  bx: the width of the board (how many columns there are)
                        by: the height of the board (how many rows there are)
                        b: the game board, represented as a two-dimentional list
        """
        self.bx = user_bx
        self.by = user_by
        self.b = []
        for i in range(self.bx):
            self.b.append([])
            for j in range(self.by):
                self.b[i].append(CHAR_BLANK)
    def width(self):
        return self.bx
    def height(self):
        return self.by
    def print_board(self):
        # Sketch:
        #   1 2 3 4 5 6 7 8
        #   ---------------
        #   0 0 0 0 0 0 0 0
        #   0 0 0 0 0 0 0 0
        #   0 0 0 0 0 0 0 0
        #   0 0 0 0 0 0 0 0
        #   0 0 0 0 0 0 0 0
        #   0 0 0 0 0 0 0 0
        # Number index
        for i in range(self.bx):
            print("{} ".format(i+1), end="")
        print()
        # Line divider
        for i in range(self.bx*2 - 1):
            print("-", end="")
        print()
        # The Board
        for i in range(self.by):
            row = ""
            for j in range(self.bx):
                row += self.b[j][i]
                row += " "
            print(row)
        print()
        return
    def print_final_board(self, winning_coords: [(int, int)]):
        """Modifies the underlying game board to replace the winning streak with CHAR_WIN (for easy visibility at the end of the game)."""
        for cell in winning_coords:
            self.b[cell[0]][cell[1]] = CHAR_WIN
        self.print_board()
        return
    def _find_last_empty_row(self, column_index: int):
        """Private function for locating the lowest available row in a given column. Responsible for "gravity."
        Inputs: column_index: the column through which to check, pre-formatted to work with zero-based indexing."""
        for i in range(self.by):
            if self.b[column_index][i] != CHAR_BLANK:
                return i-1  # If a non-empty cell is encountered, return the index of the previous cell
        return self.by-1    # By default: the last cell in a column
    def add_piece(self, user_input_column: str, team: str):
        """Modifies a cell in the game board to contain a piece.
        Inputs: user_input_column: what the user typed in for the column they want to drop their piece in.
                team: the user's game piece.
        """
        col = int(user_input_column) - 1
        row = self._find_last_empty_row(col)
        self.b[col][row] = team
        return
    def _scan_for_four_in_a_row(self, coordslist: [(int, int)], most_recent_cell: (int, int)):
        """Private function for scanning lists of coordinates in batches of 4 for any winning streaks. Responsible for the "Four" part of "Connect Four."
        Inputs: coordslist: all coordinates in a given direction from the most recently dropped piece.
                most_recent_cell: the coordinates of the most recently dropped piece."""
        player = self.b[most_recent_cell[0]][most_recent_cell[1]]
        for i in range(4):
            chain = []
            try:
                chain.append(coordslist[i])
                chain.append(coordslist[i+1])
                chain.append(coordslist[i+2])
                chain.append(coordslist[i+3])
            except IndexError:
                pass
            if len(chain) < 4:
                return []
            if player != 0 and all([player == self.b[j][k] for (j,k) in chain]):
                return chain
        return []
    def check_win(self, users_last_column: str):
        """Checks in all directions from the most recently placed piece to see if that was a game-winning move.
        Returns a list of coordinates of the winning streak or an empty list if no one won that round.
        Inputs: users_last_column: the column that the user dropped their piece in."""
        last_column = int(users_last_column) - 1
        most_recent_piece = (last_column, self._find_last_empty_row(last_column)+1)   # A tuple of the exact coordinates of the most recently placed piece

        # Lists to check for winning streaks:
        horizontal_coords = []
        vertical_coords = []
        diagdown_coords = []
        diagup_coords = []
        for i in range(-3, 4):
            if -1 < most_recent_piece[0] + i < self.bx:
                horizontal_coords.append((most_recent_piece[0] + i, most_recent_piece[1]))
            if -1 < most_recent_piece[1] + i < self.by:
                vertical_coords.append((most_recent_piece[0], most_recent_piece[1] + i))
            if -1 < most_recent_piece[0] + i < self.bx and -1 < most_recent_piece[1] + i < self.by:
                diagdown_coords.append((most_recent_piece[0] + i, most_recent_piece[1] + i))
            if -1 < most_recent_piece[0] + i < self.bx and -1 < most_recent_piece[1] - i < self.by:
                diagup_coords.append((most_recent_piece[0] + i, most_recent_piece[1] - i))
        # print("Horizontal coords:   ", horizontal_coords)
        # print("Vertical coords:     ", vertical_coords)
        # print("Diagonal-down coords:", diagdown_coords)
        # print("Diagonal-up coords:  ", diagup_coords)
        # Giant return here because we want to leave as soon as any wins are found
        return self._scan_for_four_in_a_row(horizontal_coords, most_recent_piece) or self._scan_for_four_in_a_row(vertical_coords, most_recent_piece) or self._scan_for_four_in_a_row(diagdown_coords, most_recent_piece) or self._scan_for_four_in_a_row(diagup_coords, most_recent_piece)
    def is_column_full(self, c: int):
        return CHAR_BLANK not in self.b[c]
    def is_board_full(self):
        return all([self.is_column_full(i) for i in range(self.bx)])
    def clear_board(self):
        for i in range(len(self.b)):
            for j in range(len(self.b[i])):
                self.b[i][j] = CHAR_BLANK
        return

def sanitize_input(user_input_column: str, board: Board):
    """Returns whether or not the user typed in a valid column number.
    Inputs: user_input_column: what the user typed in for the column they want to drop their piece in
            board: the current state of the board BEFORE the user's piece is added"""
    try:
        # Debug
        # if user_input_column == "_pb":
        #     print(board.b)
        col = int(user_input_column.strip())
    except ValueError:
        # ERROR: Mixed non-integral input ("one", "2s", "1.5")
        print("Please enter a valid number from {} to {}.".format(1, board.width()))
        return False
    if col < 1 or col > board.bx:
        # ERROR: Out of bounds
        print("Please enter a valid number from {} to {}.".format(1, board.width()))
        return False
    if board.is_column_full(col-1):
        # ERROR: Full column
        print("Illegal move, that column is full!")
        return False
    return True     # Could be functionally improved with a single-line return and many conditionals, but I want unique behavior for each detected error

def ending_win(winner: str, final_board: Board, winning_coords: [(int, int)], turns: int):
    print("*** Finish! Winner: Player", winner)
    print("Total turns:", turns)
    final_board.print_final_board(winning_coords)
    return

def ending_tie(final_board: Board):
    print("\n*** Finish! TIE!")
    final_board.print_board()
    return

def main():
    print("Connect Four!\n")
    board = Board(BOARD_LENGTH, BOARD_HEIGHT)
    current_player = GO_FIRST
    winning_streak = []
    turn_count = 1
    while winning_streak == []:
        if board.is_board_full():
            # Full board fail state check is here because the last move to *make the board full* could be a winning move, which is checked at the onset of every loop
            ending_tie(board)
            return
        print("---- TURN:", turn_count, "----")
        board.print_board()
        col = input("Player {}: which column would you like to place your piece in?\n>>> ".format(current_player))
        print()
        if sanitize_input(col, board):
            # Only executes if the chosen column is legal
            board.add_piece(col, current_player)
            winning_streak = board.check_win(col)
            if winning_streak == []:
                current_player = CHAR_ONE if current_player == CHAR_TWO else CHAR_TWO   # Switch players if no winner's been decided that round
                turn_count += 1
    ending_win(current_player, board, winning_streak, turn_count)
    return

if __name__ == "__main__":
    main()