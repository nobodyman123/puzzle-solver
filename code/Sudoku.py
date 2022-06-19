import numpy as np
import tkinter as tk
from puzzle_solver import Puzzle, PuzzleGui

class SudokuGui(PuzzleGui):
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.place(relwidth = 1, relheight = 1)
        for i in range(9):
            self.frame.rowconfigure(i, weight = 1)
            self.frame.columnconfigure(i, weight = 1)
        
        self.activated = None

        def activate(btn: tk.Button):
            [deactivate(other_btn) for (_, other_btn) in np.ndenumerate(self.buttons)]
            btn.config(bg = "red", command = lambda: deactivate(btn))
            self.activated = btn
            self.frame.focus_force()
            self.frame.bind("<Key>", set_value)
        
        def deactivate(btn: tk.Button):
            btn.config(bg = "white", command = lambda: activate(btn))
            self.frame.unbind("<Key>")
        
        def set_value(evt):
            key = evt.char
            if key == "":
                deactivate(self.activated)
            elif key in "123456789":
                self.activated.configure(text = key)
            elif key == "0":
                self.activated.configure(text = "")

        self.buttons = np.array([[tk.Button(self.frame, text = "") for j in range(9)] for i in range(9)])
        for (i, j), btn in np.ndenumerate(self.buttons):
            btn.grid(row = i, column = j, sticky = tk.NSEW)
            deactivate(btn)

    def get_board_state(self):
        board = np.zeros((9,9))
        
        for (pos, btn) in np.ndenumerate(self.buttons):
            btn.configure(state = tk.DISABLED)
            board[pos] = int(btn["text"]) if btn["text"] != "" else 0
        
        return board, # yes this has to be a tuple

    def set_board_state(self, board):
        for pos, value in np.ndenumerate(board):
            self.buttons[pos].configure(text = str(int(value)))

        [btn.configure(state = tk.NORMAL) for (_, btn) in np.ndenumerate(self.buttons)]

class Sudoku(Puzzle):
    def __init__(self, start_board: np.ndarray):
        # check shape
        if start_board.shape != (9,9):
            raise ValueError(f"start_board has wrong dimensions: {start_board.shape} (should be (9,9))")

        # construct sets from ints
        board = np.array([[set(range(1,10)) for j in range(9)] for i in range(9)])
        for i, e in np.ndenumerate(start_board):
            if e < 0 or e > 9:
                raise ValueError(f"board: {e} in position {i} not in range(0,10)")
            if e != 0:
                board[i] = {e}
        
        super().__init__(board, ())

    input_gui = SudokuGui

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