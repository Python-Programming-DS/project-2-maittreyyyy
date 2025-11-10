"""
Name: Maitrey Vivek Phatak
Course: MS in APPLIED DATA SCIENCE
Date: October 09, 2025
Program: TicTacToe - Part A (Classes & Objects)

A two-player Tic-Tac-Toe game using classes and objects.
Players enter moves as 'row,column'. The game validates input,
checks for wins/draw, displays the board, and allows replay.
"""


# ---------------- Board Class ---------------- #

class Board:
    """Represents the 3x3 Tic-Tac-Toe board."""

    def __init__(self):
        # I am initialising 3x3 space
        self.c = [[" ", " ", " "],
                [" ", " ", " "],
                [" ", " ", " "]]

    def reset(self):
        """Clearing the board for a new game."""
        for r in range(3):
            for col in range(3):
                self.c[r][col] = " "

    def printBoard(self):
        """This allows us to print the board with row/column labels."""
        header = "-----------------\n|R\\C| 0 | 1 | 2 |\n-----------------"
        print(header)
        for r in range(3):
            print(f"| {r} | {self.c[r][0]} | {self.c[r][1]} | {self.c[r][2]} |")
            print("-----------------")


# ---------------- Game Class ---------------- #

class Game:


    def __init__(self):
        self.board = Board()
        self.turn = 'X'  

    def switchPlayer(self):

        self.turn = 'O' if self.turn == 'X' else 'X'

    def validateEntry(self, row, col):
        """
        This will allow us to validate
        """
        if not (0 <= row <= 2 and 0 <= col <= 2):
            return False
        if self.board.c[row][col] != " ":
            return False
        return True

    def checkFull(self):
        """Return True if the board is full; otherwise False."""
        for r in range(3):
            for c in range(3):
                if self.board.c[r][c] == " ":
                    return False
        return True

    def checkWin(self):
        """
        Return True if the current player (self.turn) has a winning line.
        Checks rows, columns, and diagonals.
        """
        t = self.turn
        b = self.board.c

        # Rows
        for r in range(3):
            if b[r][0] == b[r][1] == b[r][2] == t:
                return True

        # Columns
        for c in range(3):
            if b[0][c] == b[1][c] == b[2][c] == t:
                return True

        # Diagonals
        if b[0][0] == b[1][1] == b[2][2] == t:
            return True
        if b[0][2] == b[1][1] == b[2][0] == t:
            return True

        return False

    def checkEnd(self):

        if self.checkWin():
            self.board.printBoard()
            print(f"{self.turn} IS THE WINNER!!!")
            return True

        if self.checkFull():
            self.board.printBoard()
            print("DRAW! NOBODY WINS!")
            return True

        return False

    def playGame(self):

        self.board.reset()
        self.turn = 'X'
        print("New Game: X goes first.")

        while True:
            print()
            self.board.printBoard()
            print(f"{self.turn}'s turn.")
            move_str = input("Enter row and column (e.g. 0,2): ").strip()

            # basic format check
            if "," not in move_str:
                print("Invalid format. Please use 'row,column' with 0, 1, or 2.")
                continue

            parts = [p.strip() for p in move_str.split(",")]
            if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
                print("Invalid input. Row and column must be numbers 0, 1, or 2.")
                continue

            row, col = int(parts[0]), int(parts[1])

            # I am using this to validate the game
            if not self.validateEntry(row, col):
                print("Invalid move. Out of range or cell already taken. Try again.")
                continue

            self.board.c[row][col] = self.turn


            if self.checkEnd():
                break

            self.switchPlayer()


# ---------------- main() ---------------- #

def main():
    # repeat whole game session until user decides to stop
    again = "Y"
    while again in ("Y", "y"):
        game = Game()
        game.playGame()
        print()
        again = input("Play another game? (Y/N): ").strip()
        print()

    print("Thank you for playing!")


if __name__ == "__main__":
    main()
