"""
-----------------------------------------------------------------------------
Name: Maitrey Vivek Phatak
Course: MS in APPLIED DATA SCIENCE
Date: October 09, 2025
Program: TicTacToe 
Overview:
    I am implementing a Tic-Tac-Toe game: Player 1 is human (X),
    Player 2 is computer (O) using the Minimax algorithm.
    It displays a 3x3 board which accepts input as "row,column" for X,
    validates inputs, and checks for wins across rows/columns/diagonals
    or a draw on a full board. After each round it offers to start a new 
    game without restarting the program.
-----------------------------------------------------------------------------
"""
from typing import List, Tuple

Board = List[List[str]]

class TicTacToe:
    def __init__(self):            # Initializing a 3x3 grid of spaces, looping row by row
        self.board: Board = []
        for _ in range(3):
            row = []
            for _ in range(3):
                row.append(" ")
            self.board.append(row)

        # Starting the first turn as X
        self.turn: str = "X"
        self.sep = "." * 17

    def printBoard(self) -> None:
        """
        Printing the current board grid.
        """
        print()
        print(self.sep)
        print("|R\\C| 0 | 1 | 2 |")
        print(self.sep)
        for r in range(3):
            print(f"| {r} | {self.board[r][0]} | {self.board[r][1]} | {self.board[r][2]} |")
            print(self.sep)
        print()

    def resetBoard(self) -> None:
        """
        Reset the board to start a new game.
        """
        self.board = []
        for _ in range(3):
            row = []
            for _ in range(3):
                row.append(" ")
            self.board.append(row)
        self.turn = "X"

    def validateEntry(self, row: int, col: int) -> bool:
        """
        Validate that a proposed move is on the board and empty.
        """
        if not (0 <= row <= 2 and 0 <= col <= 2):
            return False
        return self.board[row][col] == " "

    def checkFull(self) -> bool:
        """
        Check whether the board has any empty spaces remaining.
        Returns True if the board is full.
        """
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == " ":
                    return False
        return True

    def checkWin(self, turn: str) -> bool:
        """
        Check all winning possibilities for a specific player.
        """
        lines = [
            # rows
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            # cols
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            # diagonals
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]

        for line in lines:
            all_match = True
            for r, c in line:
                if self.board[r][c] != turn:
                    all_match = False
                    break
            if all_match:
                return True
        return False

    def checkEnd(self, turn: str) -> bool:
        """
        Evaluate whether the game has ended after 'turn' just played.
        """
        if self.checkWin(turn):
            print(f"{turn} IS THE WINNER!!!")
            print()
            self.printBoard()
            return True
        if self.checkFull():
            print("DRAW! NOBODY WINS!")
            print()
            self.printBoard()
            return True
        return False

    def _promptAndApplyMove(self, player: str) -> None:
        """
        Prompt the (human) player for a move, validate input, and place the mark.
        """

        print(f"{player}'s turn.")
        print()
        print(f"Where do you want your {player} placed?")
        print()
        print("Please enter row number and column number separated by a comma.")
        print()

        move_str = input().strip()
        parts = [x.strip() for x in move_str.split(",")]

        if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
            print("Invalid entry: try again.")
            print()
            print("Row & column numbers must be either 0, 1, or 2.")
            print()
            return self._promptAndApplyMove(player)

        r, c = int(parts[0]), int(parts[1])

        print(f"You have entered row #{r}")
        print()
        print(f"and column #{c}")
        print()

        # Bound Check
        if not (0 <= r <= 2 and 0 <= c <= 2):
            print("Invalid entry: try again.")
            print()
            print("Row & column numbers must be either 0, 1, or 2.")
            print()
            return self._promptAndApplyMove(player)

        # Already selected alternative
        if self.board[r][c] != " ":
            print("That cell is already taken.")
            print()
            print("Please make another selection.")
            print()
            return self._promptAndApplyMove(player)

        print("Thank you for your selection.")
        print()
        self.board[r][c] = player

    # ===================== NEW FUNCTIONS (Minimax) =====================

    def minimax(self, board: Board, is_maximizing: bool) -> int:

        # All possible winning lines 
        lines = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]

        # Using the following for loop to check terminal state
        for line in lines:
            values = [board[r][c] for r, c in line]
            if values == ["O", "O", "O"]:
                return 1     
            if values == ["X", "X", "X"]:
                return -1     

        # Check draw 
        is_full = True
        for r in range(3):
            for c in range(3):
                if board[r][c] == " ":
                    is_full = False
                    break
            if not is_full:
                break
        if is_full:
            return 0

        # Recursive minimax search
        if is_maximizing:
            # Computer's turn: maximize score
            best_score = -999
            for r in range(3):
                for c in range(3):
                    if board[r][c] == " ":
                        board[r][c] = "O"
                        score = self.minimax(board, False)
                        board[r][c] = " "
                        if score > best_score:
                            best_score = score
            return best_score
        else:
            # Human's turn: minimize score
            best_score = 999
            for r in range(3):
                for c in range(3):
                    if board[r][c] == " ":
                        board[r][c] = "X"
                        score = self.minimax(board, True)
                        board[r][c] = " "
                        if score < best_score:
                            best_score = score
            return best_score

    def get_best_move(self) -> Tuple[int, int]:
        """
        Here, I am using the function minimax to choose the best move for the computer (O).
        """
        best_score = -999
        best_move = (0, 0)

        for r in range(3):
            for c in range(3):
                if self.board[r][c] == " ":

                    self.board[r][c] = "O"
                    score = self.minimax(self.board, False)

                    self.board[r][c] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)

        return best_move



    def play(self):
        """
        Run the game loop.
        Player 1: Human (X)
        Player 2: Computer (O) using Minimax.
        """
        while True:
            print("New Game: You are X (Player 1). Computer is O (Player 2).")
            print("X goes first.")
            print()
            self.resetBoard()
            self.printBoard()

            current = "X"

            while True:
                if current == "X":
                    # Human move
                    self._promptAndApplyMove("X")
                else:
                    # Computer move using Minimax
                    print("Player 2's (O) turn.")
                    row, col = self.get_best_move()
                    self.board[row][col] = "O"
                    print(f"Player 2 chose: {row}, {col}")
                    print()

                # Check if game ended after this move
                if self.checkEnd(current):
                    break

                self.printBoard()
                current = "O" if current == "X" else "X"

            print("Another game? Enter Y or y for yes.")
            again = input().strip()
            if again not in ("Y", "y"):
                print()
                print("Thank you for playing!")
                return


def main():
    TicTacToe().play()

if __name__ == "__main__":
    main()
