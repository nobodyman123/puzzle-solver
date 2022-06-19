import numpy as np
from puzzle_solver import Puzzle
    
class Jigoku(Puzzle):
    def __init__(self, start_board: np.ndarray, comps_hor: np.ndarray, comps_vert: np.ndarray):
        # check shapes
        if start_board.shape != (9,9):
            raise ValueError(f"start_board has wrong dimensions: {start_board.shape} (should be (9,9))")
        if comps_hor.shape != (9,8):
            raise ValueError(f"comps_hor has wrong dimensions: {comps_hor.shape} (should be (9,8))")
        if comps_vert.shape != (8,9):
            raise ValueError(f"comps_vert has wrong dimensions: {comps_vert.shape} (should be (8,9))")
        
        # construct sets from ints
        board = np.array([[set(range(1,10)) for j in range(9)] for i in range(9)])
        for i, e in np.ndenumerate(start_board):
            if e < 0 or e > 9:
                raise ValueError(f"board: {e} in position {i} not in range(0,10)")
            if e != 0:
                board[i] = {e}
        
        super().__init__(board, (comps_hor, comps_vert))

    def reduce(self, board):
        comps_hor, comps_vert = self.reduction_args

        def compare(a, b, c):
            if len(a) == 0 or len(b) == 0 or c == 0:
                return
            if c == -1:
                if max(a) >= max(b):
                    a.remove(max(a))
                    return
                if min(a) >= min(b):
                    b.remove(min(b))
                    return
            elif c == 1:
                if max(b) >= max(a):
                    b.remove(max(b))
                    return
                if min(b) >= min(a):
                    a.remove(min(a))
                    return

        # Rows/Columns/Boxes
        certain = [pos for (pos, e) in np.ndenumerate(board) if len(e) == 1]
        
        for i, j in certain:
            value = board[i,j]
            board[i,:] -= value
            board[:,j] -= value
            board[3*(i//3):3*(i//3 + 1),3*(j//3):3*(j//3 + 1)] -= value
            board[i,j] = value
        
        # Compares
        for (i, j), e in np.ndenumerate(board):
            if i != 0: # above
                compare(board[i-1][j], e, comps_vert[i-1][j])
            if j != 8: # right
                compare(e, board[i][j+1], comps_hor[i][j])
            if i != 8: # under
                compare(e, board[i+1][j], comps_vert[i][j])
            if j != 0: # left
                compare(board[i][j-1], e, comps_hor[i][j-1])

def main():
    # Input
    board = np.zeros((9,9))
    comps_hor = np.array([
        [-1, 1, 0,-1,-1, 0, 1, 1],
        [ 1, 1, 0, 1, 1, 0, 1,-1],
        [-1, 1, 0,-1, 1, 0, 1, 1],
        [ 1,-1, 0,-1,-1, 0, 1,-1],
        [-1, 1, 0, 1, 1, 0, 1,-1],
        [ 1,-1, 0, 1,-1, 0,-1, 1],
        [-1, 1, 0,-1, 1, 0,-1, 1],
        [ 1,-1, 0, 1, 1, 0,-1, 1],
        [ 1, 1, 0,-1, 1, 0,-1, 1]
        ])
    comps_vert = np.array([
        [-1, 1, 1,-1,-1, 1,-1, 1,-1],
        [-1,-1,-1, 1,-1,-1,-1, 1, 1],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [-1,-1,-1, 1, 1, 1,-1, 1,-1],
        [-1, 1,-1, 1, 1,-1, 1,-1, 1],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [-1,-1,-1, 1, 1, 1, 1,-1, 1],
        [-1,-1, 1, 1, 1, 1,-1,-1,-1]
        ])
    
    # The Real Shit
    p = Jigoku(board, comps_hor, comps_vert)
    p.solve_fancy()

if __name__ == "__main__":
    main()