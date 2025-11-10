"""
-----------------------------------------------------------------------------
Name: Maitrey Vivek Phatak
Course: MS in APPLIED DATA SCIENCE
Date: October 9, 2025
Program: TicTacToe (ML model)
Overview:
    I am implementing a human vs Machine Learning model Tic-Tac-Toe game.It displays a 3x3 board which
    accepts input as "row,column", model predicts best move, and checks for wins across
    rows/columns/diagonals or a draw on a full board. After each round it offers
    to start a new game without restarting the program.
-----------------------------------------------------------------------------
"""

from typing import List
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

Board = List[List[str]]


# Base TicTacToe class
# -----------------------------------------------------------------------------
class TicTacToe:
    def __init__(self):

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
        We can reset the board with this function.
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
        This allows us to validate that a proposed move is on the board.
        """
        if not (0 <= row <= 2 and 0 <= col <= 2):
            return False
        return self.board[row][col] == " "

    def checkFull(self) -> bool:
        """
        We can check whether the board has any empty spaces remaining.
        Iterate over cells; returns True if none are empty.
        """
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == " ":
                    return False
        return True

    def checkWin(self, turn: str) -> bool:
        """
        All winning possibilities are checked for a match.
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
        We can evaluate whether the game has ended.
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
        We prompt the current player for a move, validate input, and place the mark.
        Ensures the entry is according to constraints.
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

    
        if self.board[r][c] != " ":
            print("That cell is already taken.")
            print()
            print("Please make another selection.")
            print()
            return self._promptAndApplyMove(player)

        print("Thank you for your selection.")
        print()
        self.board[r][c] = player

    def play(self):

        while True:
            print("New Game: X goes first.")
            print()
            self.resetBoard()
            self.printBoard()

            current = "X"
            while True:
                self._promptAndApplyMove(current)

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



# ML TicTacToe: Player 2 (O) is an SVC model
# -----------------------------------------------------------------------------
class TicTacToeML(TicTacToe):
    """
    Player 1: X (human)
    Player 2: O (SVC model trained on optimal O moves)
    """

    def __init__(self, model: SVC):
        super().__init__()
        self.model = model

    def _board_to_features(self) -> np.ndarray:

        mapping = {"X": 1, "O": -1, " ": 0}
        vals = [mapping[self.board[r][c]] for r in range(3) for c in range(3)]
        return np.array(vals, dtype=int).reshape(1, -1)

    def _ml_move(self) -> None:
        """
        Using the trained SVC model to decide O's move.
        If predicted move is invalid, model chooses first available cell.
        """
        features = self._board_to_features()
        move_index = int(self.model.predict(features)[0])

        r, c = divmod(move_index, 3)

        if not self.validateEntry(r, c):
            for idx in range(9):
                rr, cc = divmod(idx, 3)
                if self.validateEntry(rr, cc):
                    r, c = rr, cc
                    break

        print(f"Player 2 chooses: {r}, {c}")
        self.board[r][c] = "O"

    def play(self):
        """
        Human (X) vs ML model (O).
        """
        while True:
            print("\nNew Game: You are X.")
            print("Opponent is O.\n")

            self.resetBoard()
            self.printBoard()

            current = "X"

            while True:
                if current == "X":
                    self._promptAndApplyMove("X")
                else:
                    self._ml_move()

                if self.checkEnd(current):
                    break

                self.printBoard()
                current = "O" if current == "X" else "X"

            again = input("Play again vs ML? (Y/y for yes): ").strip()
            if again not in ("Y", "y"):
                print("\nThank you for playing against the ML model!")
                return



def train_svc_model_from_dataset() -> SVC:
    """
    I am loading tictac_single.txt and train an SVC model with hyperparameter tuning.

    """
    data = np.loadtxt("tictac_single.txt")
    X = data[:, :-1]
    y = data[:, -1].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    param_grid = {
        "C": [0.1, 1, 10, 100],
        "kernel": ["linear", "rbf"],
        "gamma": ["scale"],
    }

    base_svc = SVC(decision_function_shape="ovr")

    grid_search = GridSearchCV(
        estimator=base_svc,
        param_grid=param_grid,
        cv=5,
        scoring="accuracy",
        n_jobs=-1,
    )

    grid_search.fit(X_train, y_train)
    best_model: SVC = grid_search.best_estimator_

    return best_model



def main():
    model = train_svc_model_from_dataset()
    game = TicTacToeML(model)
    game.play()


if __name__ == "__main__":
    main()
