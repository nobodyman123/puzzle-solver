import numpy as np
from puzzle_solver import Puzzle
    
class Jigoku(Puzzle):
    def __init__(self, start_board: np.ndarray):
        super().__init__(start_board, None)

    def reduce(self, board):
        # Rows/Columns/Boxes
        certain = []
        for pos, e in np.ndenumerate(board):
            if len(e) == 1:
                certain.append(pos)
        
        for i, j in certain:
            value = board[i,j]
            board[i,:] -= value
            board[:,j] -= value
            board[3*(i//3):3*(i//3 + 1),3*(j//3):3*(j//3 + 1)] -= value
            board[i,j] = value

def main():
    # Input
    board = np.array([[set(range(1,10)) for i in range(9)] for j in range(9)])
    board1 = np.array([
        [0, 4, 0, 0, 0, 0, 6, 0, 2],
        [8, 0, 0, 2, 0, 9, 0, 4, 3],
        [0, 9, 2, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 6, 9, 0, 4, 5, 7],
        [0, 0, 6, 0, 4, 0, 1, 0, 0],
        [4, 5, 7, 0, 1, 2, 0, 3, 0],
        [0, 0, 0, 0, 0, 0, 3, 7, 0],
        [2, 6, 0, 9, 0, 7, 0, 0, 4],
        [3, 0, 9, 0, 0, 0, 0, 6, 0],
    ])
    for i, e in np.ndenumerate(board1):
        if e != 0:
            board[i] = {e}
    
    # The Real Shit
    p = Jigoku(board)
    p.solve_fancy()

if __name__ == "__main__":
    main()