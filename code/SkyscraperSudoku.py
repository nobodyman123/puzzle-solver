import numpy as np
from puzzle_solver import Puzzle

class SkyscraperSudoku(Puzzle):
    def __init__(self, start_board: np.ndarray, skyscrapers: np.ndarray):
        # check shapes
        if start_board.shape != (9,9):
            raise ValueError(f"start_board has wrong dimensions: {start_board.shape} (should be (9,9))")
        if skyscrapers.shape != (4,9):
            raise ValueError(f"skyscrapers has wrong dimensions: {skyscrapers.shape} (should be (4,9))")

        # construct sets from ints
        board = np.array([[set(range(1,10)) for j in range(9)] for i in range(9)])
        for i, e in np.ndenumerate(start_board):
            if e < 0 or e > 9:
                raise ValueError(f"board: {e} in position {i} not in range(0,10)")
            if e != 0:
                board[i] = {e}
        
        for i, e in np.ndenumerate(skyscrapers):
            if e < 1 or e > 9:
                raise ValueError(f"skryscrapers: {e} in position {i} not in range(1,10)")
        
        super().__init__(board, skyscrapers)
    
    def reduce(self, board):
        skyscrapers = self.reduction_args
        # Rows/Columns/Boxes
        certain = [pos for (pos, e) in np.ndenumerate(board) if len(e) == 1]
        
        for i, j in certain:
            value = board[i,j]
            board[i,:] -= value
            board[:,j] -= value
            board[3*(i//3):3*(i//3 + 1),3*(j//3):3*(j//3 + 1)] -= value
            board[i,j] = value
        
        if set() in board: return
        
        # Skyscrapers
        for (i, j), e in np.ndenumerate(board):
            counts = [skyscrapers[0][j], skyscrapers[1][i], skyscrapers[2][j], skyscrapers[3][i]]
            rows_columns = [
                [(x, j) for x in range(0, 9, 1)], # top
                [(i, x) for x in range(8, -1,-1)], # right
                [(x, j) for x in range(8, -1,-1)], # bottom
                [(i, x) for x in range(0, 9, 1)]  # left
            ]

            for direction in range(4):
                this_count = counts[direction]
                this_row_column = rows_columns[direction]
                
                def calc_count():
                    last = 0
                    current_count = 0
                    for pos in this_row_column:
                        if max(board[pos]) > last:
                            last = max(board[pos])
                            current_count += 1
                    return current_count
                
                if this_count == 1:
                    board[this_row_column[0]] = {9}
                
                if max(len(board[pos]) for pos in this_row_column) == 1 and calc_count() != this_count:
                    board[0,0] = set()
                    return

                if this_count == 2 and {9} in [board[pos] for pos in this_row_column]:
                    pos9 = [board[pos] for pos in this_row_column].index({9})
                    for k in range(1, pos9):
                        board[this_row_column[k]] -= set(range(max(board[this_row_column[0]]), 10))
                
                if set() in board: return

def main():
    # Input
    board = np.array([
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 3, 0, 0, 0, 0, 0],
        [0, 3, 1, 6, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 6, 2, 4, 9, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1],
    ])
    skyscrapers = np.array([
        [3, 2, 4, 2, 3, 2, 3, 4, 1], # top, left to right
        [1, 4, 3, 3, 2, 2, 2, 5, 3], # right, top to bottom
        [4, 3, 1, 3, 2, 4, 2, 2, 5], # bottom, left to right
        [3, 2, 3, 3, 3, 1, 2, 3, 3]  # left, top to bottom
        ])

    p = SkyscraperSudoku(board, skyscrapers)
    p.solve_fancy()

if __name__ == "__main__":
    main()