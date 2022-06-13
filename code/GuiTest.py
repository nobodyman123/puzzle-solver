import numpy as np
import tkinter as tk
from time import time
from random import random
from puzzle_solver import Puzzle, PuzzleGui

class TestGui(PuzzleGui):
    def __init__(self, master=None):
        stats = Puzzle.load_stats()
        self.my_label = tk.Label(master, text = stats["GuiTest"]["amount_recorded"] if "GuiTest" in stats else 0)
        self.my_label.place(anchor = tk.CENTER, relx = 0.5, rely = 0.5)
    
    def get_board_state(self):
        return int(self.my_label.cget("text")),

    def set_board_state(self, board):
        self.my_label.configure(text = max(board[0,0]))

class GuiTest(Puzzle):
    def __init__(self, i: np.ndarray, reduction_args=None):
        super().__init__(np.array([[{i}]]), reduction_args)

    def reduce(self, board):
        if max(board[0,0]) != max(self.start_board[0,0]) + 1:
            t2 = 1 + random()
            t = 0
            t1 = time()
            
            while t < t2:
                t = time() - t1
                print(f"{t} s")
            
            board[0,0] = {max(board[0,0]) + 1}

    input_gui = TestGui

def main():
    #print(GuiTest.load_stats())
    GuiTest.reset_my_stats()
    #print(GuiTest.load_stats())

if __name__ == "__main__":
    main()