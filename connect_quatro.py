BOARD_LENGTH = 8
BOARD_HEIGHT = 6

CHAR_BLANK = '0'
CHAR_WIN = '*'
CHAR_ONE = '1'
CHAR_TWO = '2'

GO_FIRST = CHAR_ONE
TURN_COUNT = 1

class Board:
    def __init__(self, user_bx, user_by):
        self.bx = user_bx
        self.by = user_by
        self.b = []
        for i in range(self.bx):
            self.b.append([])
            for j in range(self.by):
                self.b[i].append(CHAR_BLANK)
    def print_board(self):
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
    def find_last_empty_cell(self, column_index):
        index = len(self.b[column_index])-1   # By default: the last cell in a column
        for i in range(len(self.b[column_index])):
            if self.b[column_index][i] != CHAR_BLANK:
                # If a non-empty cell is encountered, return the index of the previous cell
                return i-1
        return index
    def add_piece(self, user_input_column, team):
        col = int(user_input_column) - 1
        row = self.find_last_empty_cell(col)
        self.b[col][row] = team
    def check_win(self, users_last_column):
        """Checks in all directions from the most recently placed piece to see if that was a game-winning move.
        Returns a list of coordinates of the winning streak or an empty list if no one won that round."""
        last_column = int(users_last_column) - 1    # users_last_column is a sanitized and legal string that can be cast into an integer
        most_recent_piece = (last_column, self.find_last_empty_cell(last_column)+1)   # The exact coordinates of the most recently placed piece
        potential_winner = self.b[most_recent_piece[0]][most_recent_piece[1]]

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
        print("Horizontal coords:   ", horizontal_coords)
        print("Vertical coords:     ", vertical_coords)
        print("Diagonal-down coords:", diagdown_coords)
        print("Diagonal-up coords:  ", diagup_coords)

        # TODO: parse list of coordinates for winning streaks

        return CHAR_BLANK
    def clear_board(self):
        for i in range(len(self.b)):
            for j in range(len(self.b[i])):
                self.b[i][j] = CHAR_BLANK

def sanitize_input(user_input_column, board):
    """Returns whether or not input was sanitized successfully."""
    try:
        # if user_input_column == "_pb":
        #     print(board.b)
        col = int(user_input_column.strip())
    except ValueError:
        # ERROR: Mixed non-integral input ("one", "2s", "1.5")
        print("Please enter a valid number from {} to {}.".format(1, board.bx))
        return False
    if col < 1 or col > board.bx:
        # ERROR: Out of bounds
        print("Please enter a valid number from {} to {}.".format(1, board.bx))
        return False
    col -= 1
    row = board.find_last_empty_cell(col)
    if row < 0 or row > len(board.b[col]):
        # ERROR: Full column
        print("Illegal move, that column is full!")
        return False
    return True

if __name__ == "__main__":
    print("Connect Four!\n")
    board = Board(BOARD_LENGTH, BOARD_HEIGHT)
    current_player = GO_FIRST
    winner = CHAR_BLANK
    while winner == CHAR_BLANK:
        print("TURN:", TURN_COUNT)
        board.print_board()
        col = input("Player {}: which column would you like to place your piece in?\n>>> ".format(current_player))
        if sanitize_input(col, board):
            # Only executes if the chosen column is legal
            board.add_piece(col, current_player)
            winner = board.check_win(col)
            current_player = CHAR_ONE if current_player == CHAR_TWO else CHAR_TWO   # Switch players
            TURN_COUNT += 1
    print("\nFinish! Winner: Player", winner)
    board.print_board()