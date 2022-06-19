import numpy as np
from puzzle_solver import Puzzle
    
class Sudoku(Puzzle):
    def __init__(self, start_board: np.ndarray):
        # check shape
        if start_board.shape != (9,9):
            raise ValueError(f"start_board has wrong dimensions: {start_board.shape} (should be (9,9))")

        # construct sets from ints
        board = np.array([[set(range(1,10)) for i in range(9)] for j in range(9)])
        for i, e in np.ndenumerate(start_board):
            if e < 0 or e > 9:
                raise ValueError(f"board: {e} in position {i} not in range(0,10)")
            if e != 0:
                board[i] = {e}
        
        super().__init__(board, ())

    def reduce(self, board):
        # Rows/Columns/Boxes
        certain = [pos for (pos, e) in np.ndenumerate(board) if len(e) == 1]
        
        for i, j in certain:
            value = board[i,j]
            board[i,:] -= value
            board[:,j] -= value
            board[3*(i//3):3*(i//3 + 1),3*(j//3):3*(j//3 + 1)] -= value
            board[i,j] = value

def main():
    # Input
    board = np.array([
        [0, 4, 0, 0, 0, 0, 6, 0, 2],
        [8, 0, 0, 2, 0, 9, 0, 4, 3],
        [0, 9, 2, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 6, 9, 0, 4, 5, 7],
        [0, 0, 6, 0, 4, 0, 1, 0, 0],
        [4, 5, 7, 0, 1, 2, 0, 3, 0],
        [0, 0, 0, 0, 0, 0, 3, 7, 0],
        [2, 6, 0, 9, 0, 7, 0, 0, 4],
        [3, 0, 9, 0, 0, 0, 0, 6, 0]
    ])
    
    # The Real Shit
    p = Sudoku(board)
    p.solve_fancy()

if __name__ == "__main__":
    main()