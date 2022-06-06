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
        self.my_label.configure(text = board)

class GuiTest(Puzzle):
    def __init__(self, start_board: np.ndarray, reduction_args=None):
        self.i = start_board

    def solve_fancy(self):
        target_time = 1 + random()
        solve_time = 0
        t1 = time()

        while solve_time < target_time:
            solve_time = time() - t1
            print(f"{solve_time} s")
        print(f"DONE ({solve_time} s)")
        
        self._update_stats(solve_time)
        return self.i + 1
    
    input_gui = TestGui

def main():
    #print(GuiTest.load_stats())
    GuiTest.reset_my_stats()
    #print(GuiTest.load_stats())

if __name__ == "__main__":
    main()