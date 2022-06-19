import numpy as np
from puzzle_solver import Puzzle

class JigsawSudoku(Puzzle):
    def __init__(self, start_board: np.ndarray, boxes: np.ndarray):
        # check shapes
        if start_board.shape != (9,9):
            raise ValueError(f"start_board has wrong dimensions: {start_board.shape} (should be (9,9))")
        if boxes.shape != (9,9):
            raise ValueError(f"boxes has wrong dimensions: {boxes.shape} (should be (9,9))")

        # construct sets from ints
        board = np.array([[set(range(1,10)) for j in range(9)] for i in range(9)])
        for i, e in np.ndenumerate(start_board):
            if e < 0 or e > 9:
                raise ValueError(f"board: {e} in position {i} not in range(0,10)")
            if e != 0:
                board[i] = {e}
        
        # check that there are 9 boxes of of len 9
        temp = {}
        for i, e in np.ndenumerate(boxes):
            temp[e] = temp[e] + 1 if e in temp else 1
        if len(temp) != 9:
            print(temp)
            raise ValueError(f"boxes: wrong nr. of boxes: {len(temp)} (should be 9)")
        for e in temp:
            if temp[e] != 9:
                raise ValueError(f"boxes: box nr. {e} is wrong size: {temp[e]} (should be 9)")
        
        super().__init__(board, boxes)
    
    def reduce(self, board):
        boxes = self.reduction_args
        # Rows/Columns/Boxes
        certain = [pos for (pos, e) in np.ndenumerate(board) if len(e) == 1]
        
        for i, j in certain:
            value = board[i,j]
            board[i,:] -= value
            board[:,j] -= value
            for pos in zip(*np.where(boxes == boxes[i,j])):
                board[pos] = board[pos] - value # inplace subtract (-=) makes it so no solution is found
            board[i,j] = value

def main():
    # Input
    board = np.array([
        [0, 0, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 6, 8, 4, 0, 1, 2, 0],
        [0, 0, 0, 0, 6, 9, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 9],
        [0, 4, 7, 0, 0, 0, 6, 1, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 5, 0, 0, 0, 0],
        [0, 9, 3, 0, 7, 1, 8, 0, 0],
        [0, 0, 0, 0, 0, 4, 0, 0, 0],
    ])
    boxes = np.array([
    [1, 2, 2, 2, 2, 2, 3, 3, 3],
    [1, 2, 2, 2, 4, 4, 4, 3, 3],
    [1, 1, 4, 2, 4, 4, 3, 3, 3],
    [1, 5, 4, 4, 4, 6, 6, 6, 3],
    [1, 5, 5, 6, 6, 6, 7, 7, 7],
    [1, 5, 6, 6, 8, 6, 7, 7, 7],
    [1, 5, 8, 8, 8, 8, 7, 7, 7],
    [1, 5, 8, 8, 8, 8, 9, 9, 9],
    [5, 5, 5, 9, 9, 9, 9, 9, 9]
    ])
    
    # The Real Shit
    p = JigsawSudoku(board, boxes)
    p.solve_fancy()

if __name__ == "__main__":
    main()