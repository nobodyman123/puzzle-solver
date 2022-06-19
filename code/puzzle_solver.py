import numpy as np
import json
from time import time

class PuzzleGui():
    def __init__(self, master):
        raise NotImplementedError(f"Method \"{self.__class__.__name__}.__init__\" not implemented")
    
    def get_board_state(self):
        raise NotImplementedError(f"Method \"{self.__class__.__name__}.get_board_state\" not implemented")
    
    def set_board_state(self, board):
        raise NotImplementedError(f"Method \"{self.__class__.__name__}.set_board_state\" not implemented")

class Puzzle():
    def __init__(self, start_board: np.ndarray, reduction_args: tuple):
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

    # you can study this method to understand the basic solving algorithm
    def solve(self, board=None):
        if board is None: board = self.start_board.copy()

        self.reduce(board) # use reduction rules defined in reduce method
        pos, entropy = self.get_entropy(board) # finds a position with shortest set length but not 1, 0 and max_entropy + 1 are special cases

        if entropy == 0: # contradiction found
            return
        elif entropy == self.max_entropy + 1: # all positions certain
            return board
        else:
            for e in board[pos]: # recurse through all options of lowest entropy pos
                board_copy = board.copy()
                board_copy[pos] = {e}
                r = self.solve(board_copy) # recursion my beloved
                if r is not None:
                    return r # this is how the final solved board gets passed up the recursion tree

    _STATS_PATH = "stats.json"

    @classmethod
    def load_stats(self):
        try:
            with open(Puzzle._STATS_PATH, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return Puzzle.reset_all_stats()
        except json.decoder.JSONDecodeError:
            if "yes" == input(f"Problem reading stats, do you wish to reset them? (yes/no) "):
                return Puzzle.reset_all_stats()
        except Exception as err:
            print(err)

    @classmethod
    def write_stats(self, stats):
        with open(Puzzle._STATS_PATH, "w") as f:
            json.dump(stats, f)
    
    @classmethod
    def reset_all_stats(self):
        with open(Puzzle._STATS_PATH, "w") as f:
            json.dump({}, f)
            return {}

    @classmethod
    def reset_my_stats(self):
        stats = Puzzle.load_stats()
        if self.__name__ in stats:    
            del stats[self.__name__]
            Puzzle.write_stats(stats)

    # alternative version of solve with more fancy user feedback and performance tracking
    def solve_fancy(self, board=None, n=0, t=0):
        def done(r):
            end_time = time()
            solve_time = end_time - t
            
            print(f"\n{r}\a")
            print(f"DONE ({solve_time:.3f} s)")

            stats = Puzzle.load_stats()
            if stats == None: return
            
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
                for i, e in np.ndenumerate(board):
                    board[i] = max(e)
                return board
        else:
            for e in board[pos]:
                board_copy = board.copy()
                board_copy[pos] = {e}
                r = self.solve_fancy(board_copy, n + 1, t)
                if r is not None:
                    if n == 0:
                        done(r)
                    return r
            if n == 0:
                print(f"\a")
                print("NO SOLUTION (please check input)")