import numpy as np
import tkinter as tk
from time import time
from random import random
from puzzle_solver import Puzzle, PuzzleGui

# DISCLAIMER
# this is very hacky and its supposed to be because youre not supposed to do stuff like this
# yk, making a puzzle thats solvable over and over again, most (all) puzzles dont work like that
# please for the love of god dont do any of this in your own solvers

class TestGui(PuzzleGui):
    def __init__(self, master):
        stats = Puzzle.load_stats()
        i = stats["GuiTest"]["amount_recorded"] if "GuiTest" in stats else 0
        self.my_label = tk.Label(master, text = i)
        self.my_label.place(anchor = tk.CENTER, relx = 0.5, rely = 0.5)
    
    def get_board_state(self):
        return int(self.my_label.cget("text")), # yes this has to be a tuple

    def set_board_state(self, board):
        self.my_label.configure(text = max(board[0,0]))

class GuiTest(Puzzle):
    def __init__(self, i: np.ndarray, reduction_args=None):
        super().__init__(np.array([[{i, -1}]]), reduction_args)
        # the -1 is there so that max_entropy + 1 is 3 so that we can have entropy = 2 for n = 0
        # since entropy = 1 is not possible and entropy = max_entropy + 1 would mean the puzzle is solved
        # but we dont want that to happen for n = 0, hence the placeholder -1
        self.n = 0

    def reduce(self, board):
        if self.n == 1:
            t2 = 1 + random()
            t = 0
            t1 = time()
            
            # since we cant really control the printing of solve_fancy,
            # we just block it and print stuff ourselves for the determined amount of time
            while t < t2:
                t = time() - t1
                print(f"{t} s")
            
            board[0,0] = {max(board[0,0]) + 1} # removes the -1 and increments i
        
        self.n += 1 # n will be increased for n = 0  and n = 1 (extra check)
        # n doesnt have to be reset after solve because
        # for every solve a new instance of the solver class is made

    input_gui = TestGui

def main():
    #print(GuiTest.load_stats())
    GuiTest.reset_my_stats()
    #print(GuiTest.load_stats())

if __name__ == "__main__":
    main()