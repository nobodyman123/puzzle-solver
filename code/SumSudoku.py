import numpy as np
from puzzle_solver import Puzzle

class SumSudoku(Puzzle):
    def __init__(self, start_board: np.ndarray, reverse_sum_boxes, end_sums):
        super().__init__(start_board, (reverse_sum_boxes, end_sums))
    
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
    board = np.array([[set(range(1,10)) for i in range(9)] for j in range(9)])
    sum_boxes = [
    "a b c c d d e f f",
    "a b g g h i e f f",
    "k b j j h i i f m",
    "k k k k l l l m m",
    "n n o o o o o p p",
    "q q r r r s s s s",
    "q t u u w y y B s",
    "t t v u w z z B C",
    "t t v x x A A B C"]
    sum_boxes = np.array([[f for f in e.replace(" ", "")] for e in sum_boxes])
    end_sums = {"a" : 9, "b" : 16, "c" : 10, "d" : 11, "e" : 11, "f" : 25, "g" : 5, "h" : 17, "i" : 9, "j" : 15, "k" : 20, "l" : 20, "m" : 12, "n" : 14, "o" : 24, "p" : 7, "q" : 11, "r" : 9, "s" : 30, "t" : 33, "u" : 15, "v" : 9, "w" : 8, "x" : 5, "y" : 12, "z" : 4, "A" : 14, "B" : 19, "C" : 11}
    
    reverse_sum_boxes = {}
    for i, e in np.ndenumerate(sum_boxes):
        if not e in reverse_sum_boxes:
            reverse_sum_boxes[e] = [i]
        else:
            reverse_sum_boxes[e].append(i)

    # The Real Shit
    p = SumSudoku(board, reverse_sum_boxes, end_sums)
    p.solve_fancy()

if __name__ == "__main__":
    main()