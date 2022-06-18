import tkinter as tk
import sys
from os import listdir
from threading import Thread
from puzzle_solver import Puzzle

def set_state(i):
    global selected_puzzle
    global selected_gui
    global input_frame
    global solve_button

    if i == 0: # no puzzle selected
        selected_puzzle = None
        selected_gui = None
        for child in input_frame.winfo_children():
            child.destroy()
        solve_button.configure(state = tk.DISABLED)
    elif i == 1: # puzzle selected but no gui
        selected_gui = None
        for child in input_frame.winfo_children():
            child.destroy()
        solve_button.configure(state = tk.DISABLED)
    elif i == 2: # puzzle selected with gui
        solve_button.configure(state = tk.NORMAL)
    elif i == 3: # solving
        solve_button.configure(state = tk.DISABLED)
    
    update_stats_frame()

def solve():
    def sub_solve():
        global selected_puzzle
        global selected_gui
        global solve_button
        
        set_state(3)
        try:
            puzzle_args = selected_gui.get_board_state()
            puzzle = selected_puzzle(*puzzle_args)
            solved_board = puzzle.solve_fancy()

            if puzzle.__class__ == selected_puzzle: #check if same puzzle is still selected when done solving
                selected_gui.set_board_state(solved_board)
                update_stats_frame()
            else:
                return
        except NotImplementedError as err:
            print(f"[ERR] {err}")
        finally:
            set_state(2)
    
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
    set_state(0)

    print("Puzzle list refreshed")

def update_stats_frame():
    global selected_puzzle
    global stats_selected
    global stats_average
    global stats_fastest

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

def load_puzzle(*_):
    global puzzles_list
    global selected_puzzle
    global selected_gui
    
    set_state(0) # to clear the previously loaded puzzle
    index, = puzzles_list.curselection()
    name = puzzles_list.get(index)
    try:
        exec(f"from {name} import {name}")
        selected_puzzle = eval(name)
        selected_gui = selected_puzzle.input_gui(input_frame)
        
        print(f"Loaded {name}")
        set_state(2)
    except SyntaxError:
        print(f"[ERR] name: {name!r} is not correctly formatted")
        set_state(0)
        return
    except ImportError:
        print(f"[ERR] {name} is not a puzzle")
        set_state(0)
        return
    except NotImplementedError as err:
        print(f"[ERR] {err}")
        set_state(1)
        return

class StdoutRedirector():
    def __init__(self, text_area: tk.Label):
        self.text_area = text_area

    def write(self, str):
        if str != "\n" and str != "\r":
            self.text_area.configure(text = str)
    
    def flush(self):
        pass

#region root
root = tk.Tk()
root.minsize(550, 350)
root.title("Puzzle Solver")
root.iconphoto(True, tk.PhotoImage(file = "icon.png"))
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)
root.columnconfigure(0, weight = 1)
#endregion

#region log
log = tk.Label(root, anchor = tk.W, justify = tk.LEFT, height = 1, text = "Welcome to Puzzle Solver")
log.grid(row = 1, column = 0, sticky = tk.E + tk.S + tk.W, padx = 1)

sys.stdout = StdoutRedirector(log)
#endregion

#region main
main_frame = tk.Frame(root)
main_frame.grid(row = 0, column = 0, sticky = tk.NSEW)
for i in range(11):
    main_frame.columnconfigure(i, weight = 1)

# main.toolbar
toolbar_frame = tk.Frame(main_frame, relief = tk.GROOVE, borderwidth = 2, width = 50, height = 200)
toolbar_frame.grid(row = 0, column = 0, sticky = tk.N)

# main.solve
solve_button = tk.Button(main_frame, text = "SOLVE", padx = 5, command = solve, state = tk.DISABLED)
solve_button.grid(row = 1, column = 1, columnspan = 10)

# keeps input_frame square (black magic)
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
#endregion

#region side
side_frame = tk.Frame(root, bg = "blue")
side_frame.grid(row = 0, column = 1, rowspan = 2, sticky = tk.NSEW)
side_frame.rowconfigure(0, weight = 0)
side_frame.rowconfigure(1, weight = 1)

#region side.stats
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
#endregion

#region side.puzzles
puzzles_frame = tk.LabelFrame(side_frame, text = "Puzzles")
puzzles_frame.grid(row = 1, sticky = tk.NSEW)
puzzles_frame.rowconfigure(0, weight = 1)
puzzles_frame.rowconfigure(1, weight = 1)

puzzles_list = tk.Listbox(puzzles_frame, selectmode = tk.SINGLE)
puzzles_list.grid(row = 0, sticky = tk.NSEW)
puzzles_list.bind("<<ListboxSelect>>", load_puzzle)
load_puzzle_list()

tk.Button(puzzles_frame, text = "Refresh", padx = 10, command = refresh_puzzle_list).grid(row = 1, padx = 5)
#endregion
#endregion

selected_puzzle = None
selected_gui = None

tk.mainloop()