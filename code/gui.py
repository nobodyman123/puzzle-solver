import tkinter as tk
import sys
from os import listdir
from threading import Thread
from puzzle_solver import Puzzle

def solve():
    def sub_solve():
        global selected_puzzle
        global selected_gui
        global solve_button
        global load_button
        
        if selected_puzzle is None:
            print("[ERR] No puzzle selected")
            return
        
        solve_button.config(state = tk.DISABLED)
        load_button.config(state = tk.DISABLED)
        try:
            puzzle_args = selected_gui.get_board_state()
            puzzle = selected_puzzle(*puzzle_args)
            solved_board = puzzle.solve_fancy()
            selected_gui.set_board_state(solved_board)
            update_stats_frame()
        except NotImplementedError as err:
            print(f"[ERR] {err}")
        finally:
            solve_button.config(state = tk.NORMAL)
            load_button.config(state = tk.NORMAL)
    
    Thread(target = sub_solve).start()

def load_puzzle_list():
    global puzzles_list

    IGNORE = ["gui", "puzzle_solver"]
    puzzles = [e[:-3] for e in listdir() if e[-3:] == ".py" and not e[:-3] in IGNORE]
    
    for i, puzzle in enumerate(puzzles):
        puzzles_list.insert(i, str(puzzle))

def refresh_puzzle_list():
    global puzzles_list

    puzzles_list.delete(0, tk.END)
    load_puzzle_list()
    print("Puzzle list refreshed")

def update_stats_frame():
    global selected_puzzle

    stats = Puzzle.load_stats()
    try:
        stats_selected.config(text = selected_puzzle.__name__)
        a = stats[selected_puzzle.__name__]["average_recorded_solve_speed"]
        f = stats[selected_puzzle.__name__]["fastest_recorded_solve_speed"]
        stats_average.config(text = f"{a:.3f} s")
        stats_fastest.config(text = f"{f:.3f} s")
    except KeyError: # when selected_puzzle not in stats.json
        stats_selected.config(text = selected_puzzle.__name__)
        stats_average.config(text = "N/A")
        stats_fastest.config(text = "N/A")
    except AttributeError: # when selecte_puzzle == None
        stats_selected.config(text = "N/A")
        stats_average.config(text = "N/A")
        stats_fastest.config(text = "N/A")

def load_puzzle():
    global selected_puzzle
    global solve_button
    global input_frame
    global selected_gui

    if not puzzles_list.curselection():
        print("[ERR] Please select a puzzle to load")
        return
    
    selected_index, = puzzles_list.curselection()
    selected_name = puzzles_list.get(selected_index)
    exec(f"from {selected_name} import {selected_name}")
    selected_puzzle = eval(selected_name)

    try:
        for child in input_frame.winfo_children():
            child.destroy()
        selected_gui = selected_puzzle.input_gui(input_frame)
        print(f"Loaded {selected_name}")
    except NotImplementedError as err:
        selected_puzzle = None
        selected_gui = None
        print(f"[ERR] {err}")
    finally:
        update_stats_frame()

class StdoutRedirector():
    def __init__(self, text_area: tk.Label):
        self.text_area = text_area

    def write(self, str):
        if str != "\n" and str != "\r":
            self.text_area.configure(text = str)
    
    def flush(self):
        pass

# root
root = tk.Tk()
root.minsize(550, 350)
root.title("Puzzle Solver")
root.iconphoto(True, tk.PhotoImage(file = "icon.png"))
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)
root.columnconfigure(0, weight = 1)

# log
log = tk.Label(root, anchor = tk.W, justify = tk.LEFT, height = 1, text = "Welcome to Puzzle Solver")
log.grid(row = 1, column = 0, sticky = tk.E + tk.S + tk.W, padx = 1)

sys.stdout = StdoutRedirector(log)

# main
main_frame = tk.Frame(root)
main_frame.grid(row = 0, column = 0, sticky = tk.NSEW)
for i in range(11):
    main_frame.columnconfigure(i, weight = 1)

# main.toolbar
toolbar_frame = tk.Frame(main_frame, relief = tk.GROOVE, borderwidth = 2, width = 50, height = 200)
toolbar_frame.grid(row = 0, column = 0, sticky = tk.N)

# main.solve
solve_button = tk.Button(main_frame, text = "SOLVE", command = solve, padx = 5)
solve_button.grid(row = 1, column = 1, columnspan = 10)

# black magic (keeps input_frame square)
def set_aspect(content_frame, pad_frame, aspect_ratio):
    # a function which places a frame within a containing frame, and
    # then forces the inner frame to keep a specific aspect ratio

    def enforce_aspect_ratio(event):
        # when the pad window resizes, fit the content into it,
        # either by fixing the width or the height and then
        # adjusting the height or width based on the aspect ratio.

        # start by using the width as the controlling dimension
        desired_height = event.height
        desired_width = int(event.height / aspect_ratio)

        # if the window is too tall to fit, use the height as
        # the controlling dimension
        if desired_width > event.width:
            desired_width = event.width
            desired_height = int(event.width * aspect_ratio)

        # place the window, giving it an explicit size
        content_frame.place(in_=pad_frame, anchor = tk.N, relx = 0.5, rely = 0, width=desired_width, height=desired_height)

    pad_frame.bind("<Configure>", enforce_aspect_ratio)

# main.input
pad_frame = tk.Frame(main_frame, borderwidth = 0)
pad_frame.grid(row = 0, column = 1, columnspan = 10, padx = 5, sticky = tk.NSEW)
input_frame = tk.Frame(pad_frame, borderwidth = 2, relief = tk.GROOVE)
main_frame.rowconfigure(0, weight = 1)
main_frame.columnconfigure(1, weight = 1)

set_aspect(input_frame, pad_frame, aspect_ratio=1)

# side
side_frame = tk.Frame(root, bg = "blue")
side_frame.grid(row = 0, column = 1, rowspan = 2, sticky = tk.NSEW)
side_frame.rowconfigure(0, weight = 0)
side_frame.rowconfigure(1, weight = 1)

# side.stats
stats_frame = tk.LabelFrame(side_frame, text = "Statistics")
stats_frame.grid(row = 0, sticky = tk.NSEW)

tk.Label(stats_frame, text = "Puzzle:").grid(row = 0, column = 0, sticky = tk.W)
tk.Label(stats_frame, text = "Average:").grid(row = 1, column = 0, sticky = tk.W)
tk.Label(stats_frame, text = "Fastest:").grid(row = 2, column = 0, sticky = tk.W)

stats_selected = tk.Label(stats_frame, text = "N/A")
stats_selected.grid(row = 0, column = 1, sticky = tk.NSEW)

stats_average = tk.Label(stats_frame, text = "N/A")
stats_average.grid(row = 1, column = 1, sticky = tk.NSEW)

stats_fastest = tk.Label(stats_frame, text = "N/A")
stats_fastest.grid(row = 2, column = 1, sticky = tk.NSEW)

# side.puzzles
puzzles_frame = tk.LabelFrame(side_frame, text = "Puzzles")
puzzles_frame.grid(row = 1, sticky = tk.NSEW)
puzzles_frame.rowconfigure(0, weight = 1)
puzzles_frame.rowconfigure(1, weight = 1)

puzzles_list = tk.Listbox(puzzles_frame, selectmode = tk.SINGLE)
puzzles_list.grid(row = 0, column = 0, columnspan = 2, sticky = tk.NSEW)
load_puzzle_list()

load_button = tk.Button(puzzles_frame, text = "Load", padx = 10, command = load_puzzle)
load_button.grid(row = 1, column = 0, padx = 5)
tk.Button(puzzles_frame, text = "Refresh", padx = 10, command = refresh_puzzle_list).grid(row = 1, column = 1, padx = 5)

selected_puzzle = None
selected_gui = None

tk.mainloop()