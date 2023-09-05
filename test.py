from typing import Tuple, Dict
import tkinter as tk
from tkmacosx import Button
import numpy as np
from threading import Thread, Event
from collections import deque
from time import sleep, time
from pyperclip import copy


# Finds matching pairs of brackets/braces or any other given pair of chars in a string
def build_brace_map(bf: str, braces: Tuple[str, str]) -> Dict[int, int]:
    brace_map = {}
    brace_stack = deque()
    for i, c in enumerate(bf):
        if c == braces[0]:
            brace_stack.append(i)
        if c == braces[1] and brace_stack:
            open_brace = brace_stack.pop()
            brace_map[open_brace] = i
            brace_map[i] = open_brace
    return brace_map


# Places custom borders around widgets by creating a container frame for them with the borders
class Border(tk.Frame):

    def __init__(self, parent: tk.Frame, side: str = "news", bw: int = 0, *args, bg: str = "#111111", **kwargs) -> None:
        super().__init__(parent, *args, **kwargs, highlightthickness=0)
        self.parent = parent
        borders = np.full((3, 3), False)
        borders[1][1] = True

        if bw:
            for c in side:
                match c:
                    case "w":
                        t_borders = borders.T
                        t_borders[0] = t_borders[1]
                        borders = t_borders.T
                    case "e":
                        t_borders = borders.T
                        t_borders[2] = t_borders[1]
                        borders = t_borders.T
                    case "n":
                        borders[0] = borders[1]
                    case _:
                        borders[2] = borders[1]

            borders[1, 1] = False
            x, y, w, h = self.bbox(1, 1)
            h_border = deque([tk.Frame(self, bg="#111111", width=bw, height=h, highlightthickness=0) for _ in range(2)])
            v_border = deque([tk.Frame(self, bg="#111111", width=w, height=bw, highlightthickness=0) for _ in range(2)])
            c_border = deque([tk.Frame(self, bg="#111111", width=bw, height=bw, highlightthickness=0) for _ in range(4)])

            self.rowconfigure(1, weight=1)
            self.columnconfigure(1, weight=1)
            for i, x in np.ndenumerate(borders):
                if x:
                    if np.sum(i) == 2 or i[0] == i[1]:
                        c_border.pop().grid(row=i[0], column=i[1], sticky="news")
                    elif i[0] == 1:
                        h_border.pop().grid(row=1, column=i[1], sticky="news")
                    else:
                        v_border.pop().grid(row=i[0], column=1, sticky="news")


# Highest level widget, separating the code-based section and metadata on the code
class MainApp(tk.Frame):

    def __init__(self, parent: tk.Tk, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs, highlightthickness=0)
        self.parent = parent
        self.bf = Bf(self, bg="#222222")
        self.info_border = Border(self, side="w", bw=1)
        self.info = Info(self.info_border, bg="#222222")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3, uniform="main")
        self.columnconfigure(1, weight=1, uniform="main")
        self.bf.grid(row=0, column=0, sticky="nsew")
        self.info_border.grid(row=0, column=1, sticky="nsew")
        self.info.grid(row=1, column=1, sticky="nsew")


# Contains all code related features, separating lines, code and options to control how the code is run
class Bf(tk.Frame):

    def __init__(self, parent: tk.Frame, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs, highlightthickness=0)
        self.parent = parent
        self.top_bar_border = Border(self, side="s", bw=1)
        self.top_bar = TopBar(self.top_bar_border, bg="#444444")
        self.lines = Lines(self, bg="#444444", width=30)
        self.code = Code(self, bg="#333333", fg="#aaaaaa", font=("Courier", 14), wrap="none")
        self.lines.attach(self.code)

        self.code.bind("<<Change>>", self._on_change)
        self.code.bind("<Configure>", self._on_change)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=50)
        self.top_bar_border.grid(row=0, columnspan=2, sticky="nsew")
        self.top_bar.grid(row=1, column=1, sticky="nsew")
        self.lines.grid(row=1, column=0, sticky="nsew")
        self.code.grid(row=1, column=1, sticky="nsew")

    # Modifies lines when necessary
    def _on_change(self, event):
        self.lines.redraw()


# Contains interactive widgets which can modify how and when code is run
class TopBar(tk.Frame):

    def __init__(self, parent: tk.Frame, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs, highlightthickness=0)
        self.parent = parent
        self.delay_label_border = Border(self, side="e", bw=1)
        self.delay_label = tk.Label(self.delay_label_border, bg="#444444", fg="#ffffff", text="Delay:", anchor="center")
        self.delay = tk.IntVar()
        self.delay_scale_border = Border(self, side="e", bw=1)
        self.delay_scale = tk.Scale(self.delay_scale_border, bg="#444444", fg="#ffffff", orient="horizontal", from_=0, to=100, variable=self.delay)
        self.start = Button(self, bg="#00aa00", activebackground="#008800", command=lambda: root.event_generate("<<Run>>", when="tail"), width=0, borderless=1, focuscolor="")
        self.pause = Button(self, bg="#fa9c1b", activebackground="#f58216", command=lambda: root.event_generate("<<Pause>>", when="tail"), width=0, borderless=1, focuscolor="")
        self.kill = Button(self, bg="#ff3c32", activebackground="#ff2222", command=lambda: root.event_generate("<<Kill>>", when="tail"), width=0, borderless=1, focuscolor="")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=20)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.delay_label_border.grid(row=0, column=0, sticky="news")
        self.delay_label.grid(row=1, column=1, sticky="news")
        self.delay_scale_border.grid(row=0, column=1, sticky="news")
        self.delay_scale.grid(row=1, column=1, sticky="news")
        self.start.grid(row=0, column=2, sticky="news")
        self.pause.grid(row=0, column=3, sticky="news")
        self.kill.grid(row=0, column=4, sticky="news")


# Handles running and entry of code
class Code(tk.Text):

    def __init__(self, parent: tk.Frame, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs, highlightthickness=0)
        self.parent = parent
        self.config(insertbackground="#cccccc")
        self.reset()
        self.t = 0
        self.paused = False
        self.dead = False
        self.closed = False
        self.closing = tk.IntVar()
        self.key = 0
        self.event = Event()
        self.event.set()
        self.tag_config("exe_char", background="#555555")
        self.tag_config("error_char", background="#ff4f4b", foreground="#ffffff")

        # Allows buttons to trigger actions in the current thread
        root.bind("<<Run>>", self.start)
        root.bind("<<Pause>>", self.pause)
        root.bind("<<Kill>>", self.kill)

        # Enacts syntax highlighting
        self.colourmap = {
            "[": "#ffffff",
            "]": "#ffffff",
            "{": "#ffffff",
            "}": "#ffffff",
            "(": "#ffffff",
            ")": "#ffffff",
            "|": "#ffffff",
            ">": "#9090ff",
            "<": "#9090ff",
            "+": "#ff5000",
            "-": "#ff5000",
            ".": "#ff781f",
            ",": "#ff781f",
            "#": "#ffffa0",
        }
        self.bind("<KeyRelease>", self.syntax_highlight, add="+")
        for c in self.colourmap:
            self.tag_config(c, foreground=self.colourmap[c])

        # Highlights the pair of brackets the cursor is on
        self.tag_config("cursor", background="#555555", foreground="#ffffa0")
        self.bind("<KeyRelease>", self.cursor_highlight, add="+")
        self.bind("<<Selection>>", lambda _: self.tag_remove("cursor", "1.0", "end"), add="+")
        self.bind("<ButtonRelease-1>", self.cursor_highlight)
        self.bind("<Key>", self.double_brackets, add="+")
        self.bind("<BackSpace>", self.double_backspace)

        # Allows for copying from widget
        self.bind("<Key>", self.ctrl_event, add="+")

        # Creates a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    # Resets attributes to default
    def reset(self):
        self.mem = np.zeros(30_000, dtype=np.uint8)
        self.ptr = 0
        self.funcs = {}
        self.func_mem = np.zeros(30_000, dtype=np.uint8)
        self.func_ptr = 0
        self.func_funcs = {}
        root.event_generate("<<Redraw>>")
        root.event_generate("<<RedrawFunc>>")

    # Initiates the thread to run code
    def start(self, event: tk.Event) -> None:
        self.key += 1
        self.dead = False
        self.paused = False
        self.outputs = []
        self.reset()
        self.parent.parent.info.output_box.config(text="Outputs: ")
        self.tag_remove("exe_char", "1.0", "end")
        self.tag_remove("error_char", "1.0", "end")
        bf = self.get("1.0", "end-1c")
        inputs = tuple((ord(i) if "\\" not in i else int(i[1:]) for i in self.parent.parent.info.input.get()[8:].split(" ")))
        print(inputs)
        if self.parent.top_bar.delay.get() or "#" in bf:
            self.t = Thread(target=self.run_bf, args=(bf, self.key, inputs))
            self.t.start()
        else:
            self.run_bf(bf, self.key, inputs)

    # Pauses the execution of code
    def pause(self, event: tk.Event) -> None:
        self.paused = not self.paused

    # Ends the execution of code and kills the thread
    def kill(self, event: tk.Event) -> None:
        self.dead = True

    def close(self):
        self.closing.set(1)
        self.dead = True
        if self.t and self.t.is_alive():
            self.wait_variable(self.closing)
        root.destroy()

    # Handles the colouring of characters each time a new character is entered
    def syntax_highlight(self, event: tk.Event) -> None:
        for tag in self.colourmap:
            self.tag_remove(tag, "1.0", "end")
        for i, c in enumerate(self.get("1.0", "end-1c")):
            if c in self.colourmap:
                self.tag_add(c, f"1.0+{i}c", f"1.0+{i + 1}c")

    # Highlights the pair of braces the cursor is on
    def cursor_highlight(self, event: tk.Event) -> None:
        self.tag_remove("cursor", "1.0", "end")
        loops = build_brace_map(self.get("1.0", "end-1c"), ("[", "]"))
        loops.update(build_brace_map(self.get("1.0", "end-1c"), ("{", "}")))
        loops.update(build_brace_map(self.get("1.0", "end-1c"), ("(", ")")))
        cursor = self.count("1.0", "insert")
        if cursor is None:
            cursor = 0
        else:
            cursor = cursor[0]
        brackets = True
        if cursor - 1 in list(loops.values()):
            cursor -= 1
            other = [key for key, value in loops.items() if value == cursor][0]
        elif cursor in list(loops.values()):
            other = [key for key, value in loops.items() if value == cursor][0]
        elif cursor in loops:
            other = loops[cursor]
        elif cursor - 1 in loops:
            cursor -= 1
            other = loops[cursor]
        else:
            brackets = False
        if brackets and self.index("sel.first") == "None":
            self.tag_add("cursor", f"1.0+{str(cursor)}c")
            self.tag_add("cursor", f"1.0+{str(other)}c")

    # Enters 2 braces at once and places cursor between them
    def double_brackets(self, event: tk.Event) -> str | None:
        bracket = True
        if event.char == "[":
            keys = ("[", "]")
        elif event.char == "{":
            keys = ("{", "}")
        elif event.char == "(":
            keys = ("(", ")")
        else:
            bracket = False
        if bracket:
            if self.index("sel.first") == "None":
                first = "insert"
                last = "insert"
                insert = "insert-1c"
            else:
                first = "sel.first"
                last = "sel.last"
                insert = "sel.first"
            self.insert(first, keys[0])
            if first == "sel.first" or self.get(last) not in self.colourmap or self.get(last) in ("]", "}", ")"):
                self.insert(last, keys[1])
                self.mark_set("insert", insert)
            return "break"

    # Deletes 2 brackets at once if there are no chars between them
    def double_backspace(self, event: tk.Event) -> None:
        if (
            (self.get("insert-1c", "insert") == "[" and self.get("insert", "insert+1c") == "]") or
            (self.get("insert-1c", "insert") == "{" and self.get("insert", "insert+1c") == "}") or
            (self.get("insert-1c", "insert") == "(" and self.get("insert", "insert+1c") == ")")
        ):
            self.delete("insert", "insert+1c")

    # Allows the user to save text to the clipboard when they copy or cut
    def ctrl_event(self, event: tk.Event) -> str | None:
        if event.state == 8 and event.keysym in ("c", "x") and self.index("sel.first") == "None":
            return "break"
        elif event.state == 8 and event.keysym == "c":
            copy(self.selection_get())
            return "break"
        elif event.state == 8 and event.keysym == "x":
            copy(self.selection_get())
            self.delete("sel.first", "sel.last")
            return "break"

    # Complex tcl, stolen shamelessly from Bryan Oakley
    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        try:
            result = self.tk.call(cmd)
        except tk.TclError:
            return

        # generate an event if something was added or deleted, or the cursor position changed
        if (
            args[0] in ("insert", "replace", "delete") or
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result

    # Thread to be instantiated - runs the code. Passes metadata to Info, displays current characters being exeuted, and executes them
    def run_bf(self, bf: str, key: int, inputs: Tuple[int] = tuple()) -> deque:
        st = time()
        # Waits for previous thread to die if program is rerun
        self.event.wait()
        self.event.clear()

        # Declares key variables
        loops = build_brace_map(bf, ("[", "]"))
        funcs = build_brace_map(bf, ("{", "}"))
        mem_scopes = deque([np.zeros(30_000, dtype=np.uint8)])
        cell_ptr_scopes = deque([0])
        func_scopes = deque([{}])
        inputs_scopes = deque([deque(inputs)])
        outputs_scopes = deque([deque()])
        bf_ptr = 0
        is_func = False
        is_call = False
        is_call2 = False

        # Executes all commands
        while bf_ptr < len(bf):

            # Creates references to the current local scope
            mem = mem_scopes[-1]
            cell_ptr = cell_ptr_scopes[-1]
            func = func_scopes[-1]
            inputs = inputs_scopes[-1]
            outputs = outputs_scopes[-1]
            comment = False

            # Executes current command
            match bf[bf_ptr]:

                case ">":
                    # Increments cell pointer, handles wrapping, and updates stack (because integers for the pointer are immutable)
                    cell_ptr += 1
                    if cell_ptr == 30_000:
                        cell_ptr = 0
                    cell_ptr_scopes.pop()
                    cell_ptr_scopes.append(cell_ptr)

                case "<":
                    # Decrements cell pointer, handles wrapping, and updates stack (because integers for the pointer are immutable)
                    cell_ptr -= 1
                    if cell_ptr == -1:
                        cell_ptr = 29_999
                    cell_ptr_scopes.pop()
                    cell_ptr_scopes.append(cell_ptr)

                case "+":
                    # Increments value at cell and deletes any functions present in cell
                    mem[cell_ptr] += 1
                    if cell_ptr in func:
                        func.pop(cell_ptr)

                case "-":
                    # Decrements value at cell and deletes any functions present in cell
                    mem[cell_ptr] -= 1
                    if cell_ptr in func:
                        func.pop(cell_ptr)

                case ",":
                    # Passes input to memory or function memory
                    if not inputs:
                        self.tag_add("error_char", f"1.0+{bf_ptr}c")
                        break
                    inp = inputs.popleft()
                    if isinstance(inp, int):
                        mem[cell_ptr] = inp
                    else:
                        mem[cell_ptr] = 0
                        func[cell_ptr] = inp

                case ".":
                    # Outputs value or function at cell
                    if is_func or (is_call and not is_call2):
                        if cell_ptr in func:
                            outputs.append(func[cell_ptr])
                        else:
                            outputs.append(int(mem[cell_ptr]))
                    else:
                        output = self.parent.parent.info.output_box
                        output.config(text=output.cget("text") + chr(mem[cell_ptr]) + " ")

                case "[" if mem[cell_ptr] == 0:
                    # Moves to end of loop if cell is 0
                    bf_ptr = loops[bf_ptr]

                case "]" if mem[cell_ptr] != 0:
                    # Moves to the beginning of loop if cell is not 0
                    bf_ptr = loops[bf_ptr]

                case "{":
                    # Finds start and end characters of the function and stores these for when the function at this pointer is called
                    mem[cell_ptr] = 0
                    func[cell_ptr] = (bf_ptr, funcs[bf_ptr])
                    bf_ptr = funcs[bf_ptr]

                case "}":
                    # Deletes the current function's local scopes and moves back to the function call
                    mem_scopes.pop()
                    cell_ptr_scopes.pop()
                    func_scopes.pop()
                    inputs_scopes.pop()
                    outputs_scopes.pop()
                    inputs_scopes.append(outputs)
                    bf_ptr = call_ptr
                    if not is_func:
                        is_func = False
                    is_call = True
                    is_call2 = True

                case "(":
                    # Creates a new local scope for the first half of the function call's outputs and stores the cell pointer of the function being called
                    if cell_ptr not in func:
                        self.tag_add("error_char", f"1.0+{bf_ptr}c")
                        break
                    outputs_scopes.append(deque())
                    call_ptr = cell_ptr
                    is_call = True

                case "|":
                    # Moves to the beginning of the function which has been called and passes the outputs from the call as arguments to the function
                    if not is_call:
                        self.tag_add("error_char", f"1.0+{bf_ptr}c")
                        break
                    mem_scopes.append(np.zeros(30_000, dtype=np.uint8))
                    cell_ptr_scopes.append(0)
                    func_scopes.append({})
                    inputs_scopes.append(outputs)
                    outputs_scopes.pop()
                    outputs_scopes.append(deque())
                    bf_ptr, call_ptr = func[call_ptr][0], bf_ptr
                    is_func = True
                    is_call = False

                case ")":
                    if not is_call:
                        self.tag_add("error_char", f"1.0+{bf_ptr}c")
                        break
                    inputs_scopes.pop()
                    is_call = False
                    is_call2 = False

                case "#":
                    self.paused = True

                case _:
                    comment = True

            # Highlights current command and enacts delay
            delay = self.parent.top_bar.delay.get()
            if not comment and delay:
                self.tag_remove("exe_char", "1.0", "end")
                self.tag_add("exe_char", f"1.0+{bf_ptr}c")
                sleep(delay / 20)
                if is_func:
                    self.func_mem = mem
                    self.func_ptr = cell_ptr
                    self.func_funcs = func
                    root.event_generate("<<RedrawFunc>>", when="tail")
                else:
                    self.mem = mem
                    self.ptr = cell_ptr
                    self.funcs = func
                    root.event_generate("<<Redraw>>", when="tail")

            # Increments code pointer to execute next command
            bf_ptr += 1

            # Gracefully kills thread if thread is rerun or stopped
            if self.dead or self.key != key:
                self.reset()
                break

            # Pauses thread if paused and enacts closing and killing if necessary
            if self.paused:
                self.tag_remove("exe_char", "1.0", "end")
                self.tag_add("exe_char", f"1.0+{bf_ptr-1}c", f"1.0+{bf_ptr}c")
                if is_func:
                    self.func_mem = mem
                    self.func_ptr = cell_ptr
                    self.func_funcs = func
                    root.event_generate("<<RedrawFunc>>", when="tail")
                else:
                    self.mem = mem
                    self.ptr = cell_ptr
                    self.funcs = func
                    root.event_generate("<<Redraw>>", when="tail")
            while self.paused:
                if self.dead or self.key != key:
                    self.reset()
                    break

        print(time() - st)
        self.tag_remove("exe_char", "1.0", "end")
        self.event.set()
        if self.closing.get() == 1:
            self.closing.set(0)
        return outputs_scopes[0]


# Displays and updates lines on the sidebar
class Lines(tk.Canvas):

    def __init__(self, parent: tk.Frame, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs, highlightthickness=0)
        self.parent = parent
        self.code = None

    # Stores the code widget as an attribute to read and capture events
    def attach(self, text_widget: tk.Text) -> None:
        self.code = text_widget

    # Redraws lines when the code is modified, stolen shamelessly from Bryan Oakley
    def redraw(self, *args) -> None:
        # redraw line numbers
        self.delete("all")

        i = self.code.index("@0,0")
        while True:
            dline = self.code.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            linenum = linenum.rjust(4)
            self.create_text(2, y, anchor="nw", text=linenum, font=("Courier", 14), fill="grey")
            i = self.code.index("%s+1line" % i)


# Separates memory displays, input and output bars
class Info(tk.Frame):

    def __init__(self, parent: tk.Frame, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs, highlightthickness=0)
        self.parent = parent
        self.input = tk.StringVar(self)
        self.input_box = tk.Entry(self, bg="#333333", fg="#ffffff", font=("Courier", 14), exportselection=False, textvariable=self.input, insertbackground="#ffffff", borderwidth=0, highlightthickness=0)
        self.input_box.insert("1", "Inputs: ")
        self.input_box.bind("<BackSpace>", lambda _: "break" if self.input_box.index("insert") == 8 else None)
        self.output_border = Border(self, side="ns", bw=1)
        self.output_box = tk.Label(self.output_border, bg="#333333", fg="#ffffff", text="Outputs: ", font=("Courier", 14), anchor="w", highlightthickness=0)
        self.mem = MemDisplay(self, False, bg="#444444", fg="#ffffff", font=("Courier", 14), wrap="none")
        self.func_border = Border(self, side="ns", bw=1)
        self.func_mem = MemDisplay(self.func_border, True, bg="#444444", fg="#ffffff", font=("Courier", 14), wrap="none")
        self.about = tk.Text(self, bg="#555555", fg="#ffffff", highlightthickness=0)

        self.rowconfigure(0, weight=2, uniform="box")
        self.rowconfigure(1, weight=2, uniform="box")
        self.rowconfigure(2, weight=3, uniform="box")
        self.rowconfigure(3, weight=3, uniform="box")
        self.rowconfigure(4, weight=30, uniform="box")
        self.columnconfigure(0, weight=1)
        self.input_box.grid(row=0, column=0, sticky="nsew")
        self.output_border.grid(row=1, column=0, sticky="nsew")
        self.output_box.grid(row=1, column=1, sticky="nsew")
        self.mem.grid(row=2, column=0, sticky="nsew")
        self.func_border.grid(row=3, column=0, sticky="nsew")
        self.func_mem.grid(row=1, column=1, sticky="nsew")
        self.about.grid(row=4, column=0, sticky="nsew")

        about = """About
        
Another Brainfuck derivative. But also so much 
more.

Some call it an esolang, others call it a 
particularly cruel method of torture, but 
personally, I say modern problems require modern 
solutions - so here is your modern solution.

By adding the slightly higher level power of 
functions and all that comes with them to 
brainfuck, I have created a language that maintains
that minimalistic but taunting mannerism of 
brainfuck but makes it actually useful. Saddled 
with it is an IDE to make life easier. If the new 
language is of no interest to you the IDE is 
perfectly capable of executing and assisting you 
with the writing of regular brainfuck. Note that 
the compiler isn't the fastest out there but it is 
certainly the best for debugging.

For more information, take a look at the github 
repository"""
        self.about.insert("1.0", about)
        self.about.config(state="disabled")


# Displays the memory in the current code thread, either for the main bf programme or for the current running function
class MemDisplay(tk.Text):

    def __init__(self, parent: tk.Frame, func: bool, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs, highlightthickness=0)
        self.parent = parent
        self.func = func
        self.config(state="disabled")
        self.tag_config("pointer", background="#666666")
        self.rewrite()
        root.bind("<<RedrawFunc>>" if self.func else "<<Redraw>>", self.rewrite)

    # Rewrites the memory each time its changed
    def rewrite(self, event: tk.Event | None = None) -> None:

        # Retrieves the nonzero values currently in the memory
        if self.func:
            mem = self.parent.parent.parent.parent.bf.code.func_mem
            pointer = self.parent.parent.parent.parent.bf.code.func_ptr
            funcs = self.parent.parent.parent.parent.bf.code.func_funcs
        else:
            mem = self.parent.parent.parent.bf.code.mem
            pointer = self.parent.parent.parent.bf.code.ptr
            funcs = self.parent.parent.parent.bf.code.funcs
        non_zero = np.nonzero(mem)[0]
        additional = np.append(np.array(list(funcs.keys()), dtype=np.uint), np.uint(pointer))
        non_zero = np.insert(non_zero, np.searchsorted(non_zero, additional), additional)

        # Finds the first and last memory values to display, accounting for negative nonzero indices
        if (
            non_zero[non_zero > 15_000].size > 0 and
            (non_zero[non_zero <= 15_000].size == 0 or
             non_zero[non_zero > 15_000][0] > non_zero[non_zero <= 15_000][-1] * 2)
        ):
            _min = non_zero[non_zero > 15_000][0] - 30_000
            _max = non_zero[-1] - 29_999 if non_zero[non_zero <= 15_000].size == 0 else non_zero[non_zero <= 15_000][-1] + 1
            if _max >= -10:
                _max = 1
            pointer -= _min + (30_000 if pointer > 15_000 else 0)
        else:
            _min = 0 if non_zero[0] < 10 else non_zero[0]
            _max = non_zero[-1] + 1
            pointer -= _min

        # Displays the section of the memory between the first and last values
        index = np.arange(_min, _max)
        mem = mem[index]
        self.config(state="normal")
        self.tag_remove("pointer", "1.0", "end")
        self.delete("1.0", "end")
        self.insert("1.0", f"   index|{'|'.join(str(i).rjust(6) for i in index)}\n")
        self.insert("2.0", "_" * 8 + "|______" * (_max - _min) + "\n")
        self.insert("3.0", f"  memory|{'|'.join((f'f{funcs[i][0]}'.rjust(6) if i in funcs else str(n).rjust(6)) for i, n in enumerate(mem))}\n")
        self.insert("4.0", " " * 8 + "|      " * (_max - _min) + "\n")
        self.tag_add("pointer", f"1.{9 + pointer * 7}", f"1.{15 + pointer * 7}")
        self.tag_add("pointer", f"2.{9 + pointer * 7}", f"2.{15 + pointer * 7}")
        self.tag_add("pointer", f"3.{9 + pointer * 7}", f"3.{15 + pointer * 7}")
        self.tag_add("pointer", f"4.{9 + pointer * 7}", f"4.{15 + pointer * 7}")
        self.see(f"1.{9 + 7 * (_max - _min)}")
        self.config(state="disabled")


if __name__ == "__main__":

    # Instantiates root
    root = tk.Tk()
    root.title("BrainFunc IDE")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # Instantiates main frame within the root
    main_app = MainApp(root, bd=0)
    main_app.grid(row=0, column=0, sticky="news")

    # Constantly updates the root till it closes, in which case the current code thread will be killed
    root.protocol("WM_DELETE_WINDOW", main_app.bf.code.close)
    root.mainloop()
