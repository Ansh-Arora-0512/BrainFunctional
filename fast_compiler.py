from time import time
import numpy as np
from collections import deque
from typing import Tuple, List, Dict


# Finds matching pairs of brackets/braces or any other given pair of chars in a string
def build_brace_map(bf: str, braces: Tuple[str, str]) -> Dict[int, int]:
    brace_map = {}
    brace_stack = deque()
    for i, c in enumerate(bf):
        if c == braces[0]:
            brace_stack.append(i)
        if c == braces[1]:
            open_brace = brace_stack.pop()
            brace_map[open_brace] = i
            brace_map[i] = open_brace
    return brace_map


# Executes brainfuck, with default arguments being used to handle recursion
def execute(bf: str, inputs: List[int] | Tuple[int] = tuple()) -> deque:

    # Declares key variables
    loops = build_brace_map(bf, ("[", "]"))
    funcs = build_brace_map(bf, ("{", "}"))
    mem_scopes = deque()
    cell_ptr_scopes = deque()
    func_scopes = deque()
    inputs_scopes = deque()
    outputs_scopes = deque()
    mem_scopes.append(np.zeros(30_000, dtype=np.uint8))
    cell_ptr_scopes.append(0)
    func_scopes.append({})
    inputs_scopes.append(deque(inputs))
    outputs_scopes.append(deque())
    bf_ptr = 0

    # Executes all commands
    while bf_ptr < len(bf):

        # Creates references to the current local scope
        mem = mem_scopes[-1]
        cell_ptr = cell_ptr_scopes[-1]
        func = func_scopes[-1]
        inputs = inputs_scopes[-1]
        outputs = outputs_scopes[-1]

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
                inp = inputs.popleft()
                if isinstance(inp, int):
                    mem[cell_ptr] = inp
                else:
                    mem[cell_ptr] = 0
                    func[cell_ptr] = inp

            case ".":
                # Outputs value or function at cell
                if cell_ptr in func:
                    outputs.append(func[cell_ptr])
                else:
                    outputs.append(int(mem[cell_ptr]))

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

            case "(":
                # Creates a new local scope for the first half of the function call's outputs and stores the cell pointer of the function being called
                outputs_scopes.append(deque())
                call_ptr = cell_ptr

            case "|":
                # Moves to the beginning of the function which has been called and passes the outputs from the call as arguments to the function
                mem_scopes.append(np.zeros(30_000, dtype=np.uint8))
                cell_ptr_scopes.append(0)
                func_scopes.append({})
                inputs_scopes.append(outputs)
                outputs_scopes.pop()
                outputs_scopes.append(deque())
                bf_ptr, call_ptr = func[call_ptr][0], bf_ptr

            case ")":
                inputs_scopes.pop()

        # Increments code pointer to execute next command
        bf_ptr += 1

    return outputs_scopes[0]


if __name__ == "__main__":
    st = time()
    code = "+[>-]"
    print(execute(code))
    print(time() - st)
