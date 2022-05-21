import numpy as np
import json
from time import time

# TODO: 
# 1) GUI
#   using tkinter (OK)
#   base layout: running time, solve button, stats bar (OK)
#   + puzzle specific visual input
# 2) settings

class PuzzleGui():
    def __init__(self, master = None):
        raise NotImplementedError(f"Method \"{self.__class__.__name__}.__init__\" not implemented")
    def get_board_state(self):
        raise NotImplementedError(f"Method \"{self.__class__.__name__}.get_board_state\" not implemented")
    def set_board_state(self, board):
        raise NotImplementedError(f"Method \"{self.__class__.__name__}.set_board_state\" not implemented")

class Puzzle():
    def __init__(self, start_board: np.ndarray, reduction_args = None):
        self.start_board = start_board.copy()
        self.reduction_args = reduction_args
        self.max_entropy = max(len(e) for _, e in np.ndenumerate(start_board))
    
    input_gui = PuzzleGui

    def reduce(self, board):
        raise NotImplementedError(f"Must implement \"{self.__class__.__name__}.reduce\" method")

    def get_entropy(self, board):
        entropy = self.max_entropy + 1
        pos = ()
        for i, e in np.ndenumerate(board):
            if len(e) == 0:
                return (), 0
            elif 1 < len(e) < entropy:
                pos, entropy = (i, len(e))
        return pos, entropy

    def solve(self, board=None):
        if board is None: board = self.start_board.copy()

        self.reduce(board)
        pos, entropy = self.get_entropy(board)

        if entropy == 0:
            return
        elif entropy == self.max_entropy + 1:
            return board
        else:
            for e in board[pos]:
                board_copy = board.copy()
                board_copy[pos] = {e}
                r = self.solve(board_copy)
                if r is not None:
                    return r

    _stats_path = "stats.json"

    @classmethod
    def load_stats(self):
        try:
            with open(Puzzle._stats_path, "r") as f:
                try:
                    return json.load(f)
                except:
                    if "yes" == input("Cannot read stats , do you wish to reset \"{Puzzle._stats_path}\"? (yes/no)"):
                        Puzzle.reset_all_stats()
                    else:
                        return {}
        except:
            if "yes" == input("Cannot open \"{Puzzle._stats_path}\", do you wish to reset it? (yes/no)"):
                Puzzle.reset_all_stats()
            else:
                return {}
    
    @classmethod
    def write_stats(self, stats):
        with open(Puzzle._stats_path, "w") as f:
            json.dump(stats, f)
    
    @classmethod
    def reset_all_stats(self):
        with open(Puzzle._stats_path, "w") as f:
            json.dump({}, f)
            return {}

    @classmethod
    def reset_my_stats(self):
        stats = Puzzle.load_stats()
        if self.__name__ in stats:    
            del stats[self.__name__]
            Puzzle.write_stats(stats)

    def _update_stats(self, solve_time):
        stats = Puzzle.load_stats()
        
        puzzle_name = self.__class__.__name__
        if puzzle_name in stats:
            this_puzzle = stats[puzzle_name]
            this_puzzle["amount_recorded"] += 1
            this_puzzle["average_recorded_solve_speed"] = (this_puzzle["average_recorded_solve_speed"] * (this_puzzle["amount_recorded"] - 1) + (solve_time)) / this_puzzle["amount_recorded"]
            if solve_time < this_puzzle["fastest_recorded_solve_speed"]:
                this_puzzle["fastest_recorded_solve_speed"] = solve_time
        else:
            stats[puzzle_name] = {
                "amount_recorded": 1,
                "average_recorded_solve_speed": solve_time,
                "fastest_recorded_solve_speed": solve_time
            }
        
        Puzzle.write_stats(stats)

    def solve_fancy(self, board=None, n=0, t=0):
        if board is None: board = self.start_board.copy()
        if n == 0: t = time()

        self.reduce(board)
        pos, entropy = self.get_entropy(board)

        print(f"Running for {time() - t:.3f} s", end="\r")
        #print(n, entropy, max([len(e) for (_,e) in np.ndenumerate(board)]))
        
        if entropy == 0:
            return
        elif entropy == self.max_entropy + 1:
            # idk if this extra check is necessary but fuck it
            self.reduce(board)
            _, entropy = self.get_entropy(board)
            if entropy == 0:
                return
            else:
                return board
        else:
            for e in board[pos]:
                board_copy = board.copy()
                board_copy[pos] = {e}
                r = self.solve_fancy(board_copy, n + 1, t)
                if r is not None:
                    if n == 0:
                        end_time = time()
                        solve_time = end_time - t
                        
                        print(f"\n{r}\a")
                        print(f"DONE ({solve_time:.3f} s)")
                        self._update_stats(solve_time)
                    return r