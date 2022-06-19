import numpy as np
from puzzle_solver import Puzzle

class SumSudoku(Puzzle):
    def __init__(self, start_board: np.ndarray, sum_boxes: np.ndarray, end_sums: dict):
        # check shapes
        if start_board.shape != (9,9):
            raise ValueError(f"start_board has wrong dimensions: {start_board.shape} (should be (9,9))")
        if sum_boxes.shape != (9,9):
            raise ValueError(f"sum_boxes has wrong dimensions: {sum_boxes.shape} (should be (9,9))")

        # construct sets from ints
        board = np.array([[set(range(1,10)) for j in range(9)] for i in range(9)])
        for i, e in np.ndenumerate(start_board):
            if e < 0 or e > 9:
                raise ValueError(f"board: {e} in position {i} not in range(0,10)")
            if e != 0:
                board[i] = {e}

        # construct reverse_sum_boxes
        reverse_sum_boxes = {}
        for i, e in np.ndenumerate(sum_boxes):
            reverse_sum_boxes[e] = reverse_sum_boxes[e] + [i] if e in reverse_sum_boxes else [i]
        
        if end_sums.keys() != reverse_sum_boxes.keys():
            raise KeyError("end_sums keys and reverse_sum_boxes keys do not match")
        
        super().__init__(board, (reverse_sum_boxes, end_sums))
    
    def reduce(self, board):
        reverse_sum_boxes, end_sums = self.reduction_args
        # Rows/Columns/Boxes
        certain = [pos for (pos, e) in np.ndenumerate(board) if len(e) == 1]
        
        for i, j in certain:
            value = board[i,j]
            board[i,:] -= value
            board[:,j] -= value
            board[3*(i//3):3*(i//3 + 1),3*(j//3):3*(j//3 + 1)] -= value
            board[i,j] = value

        # Sums
        for i in reverse_sum_boxes:
            pos_list = reverse_sum_boxes[i]
            temp_pl = pos_list.copy()
            temp_sum = end_sums[i]

            for pos in pos_list:
                if len(board[pos]) == 1:
                    temp_pl.remove(pos)
                    temp_sum -= min(board[pos])
            
            if temp_sum < 0:
                board[0,0] = set()
                return
            
            if len(temp_pl) == 1:
                pos, = temp_pl
                board[pos] = board[pos] & {temp_sum}
            elif len(temp_pl) == 0 and temp_sum != 0:
                board[0,0] = set()
                return

def main():
    # Input
    board = np.zeros((9,9))
    sum_boxes = np.array([
    [ 1,  2,  3,  3,  4,  4,  5,  6,  6],
    [ 1,  2,  7,  7,  8,  9,  5,  6,  6],
    [11,  2, 10, 10,  8,  9,  9,  6, 13],
    [11, 11, 11, 11, 12, 12, 12, 13, 13],
    [14, 14, 15, 15, 15, 15, 15, 16, 16],
    [17, 17, 18, 18, 18, 19, 19, 19, 19],
    [17, 20, 21, 21, 23, 25, 25, 28, 19],
    [20, 20, 22, 21, 23, 26, 26, 28, 29],
    [20, 20, 22, 24, 24, 27, 27, 28, 29]
    ])
    end_sums = {
        1 : 9,
        2 : 16,
        3 : 10,
        4 : 11,
        5 : 11,
        6 : 25,
        7 : 5,
        8 : 17,
        9 : 9,
        10 : 15,
        11 : 20,
        12 : 20,
        13 : 12,
        14 : 14,
        15 : 24,
        16 : 7,
        17 : 11,
        18 : 9,
        19 : 30,
        20 : 33,
        21 : 15,
        22 : 9,
        23 : 8,
        24 : 5,
        25 : 12,
        26 : 4,
        27 : 14,
        28 : 19,
        29 : 11}

    # The Real Shit
    p = SumSudoku(board, sum_boxes, end_sums)
    p.solve_fancy()

if __name__ == "__main__":
    main()