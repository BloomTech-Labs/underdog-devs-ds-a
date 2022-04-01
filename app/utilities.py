import sys
from typing import Dict


def dict_to_str(data: Dict) -> str:
    """Convert dictionaries into easy to read strings."""
    return "\n" + "\n".join(f"{k}: {v}" for k, v in data.items())


def financial_aid_gen(profile):
    """This is a function that queries the database
    for variables attached to a mentees profile id and applies
    that information into a forumla that returns financial aid
    probability"""

    e_l_dict = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Expert": 4}
    f_i = (1 if profile['formerly_incarcerated'] else 0)
    l_i = 1 if profile['low_income'] else 0
    e_l = e_l_dict[profile['experience_level']]

    def f_a_func(f_i, l_i, e_l):
        """Algorithm (from McGraw_Papenburg.ipynb)
        This can be modified to include future Mentee
        database variables"""

        f_i /= 2
        l_i += f_i
        e_l = l_i + pow(9.9*e_l, -1)
        return (e_l - 0.025) / 1.577

    return f"{f_a_func(f_i, l_i, e_l):.2%}"


def b_f_exec(code):
    class _Getch:
        """Gets a single character from standard input."""
        def __init__(self):
            try:
                self.impl = _GetchWindows()
            except ImportError:
                self.impl = _GetchUnix()

        def __call__(self): return self.impl()

    class _GetchUnix:
        def __call__(self):
            import tty
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                _ = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return

    class _GetchWindows:
        def __call__(self):
            import msvcrt
            return msvcrt.getch()

    getch = _Getch()

    def cleanup(code):
        return ''.join(filter(lambda x: x
                              in ['.', ',', '[', ']', '<', '>', '+', '-'],
                              code))

    def buildbracemap(code):
        temp_bracestack, bracemap = [], {}
        for position, command in enumerate(code):
            if command == "[":
                temp_bracestack.append(position)
            if command == "]":
                start = temp_bracestack.pop()
                bracemap[start] = position
                bracemap[position] = start
        return bracemap

    def evaluate(code):
        code = cleanup(list(code))
        bracemap = buildbracemap(code)
        cells, codeptr, cellptr = [0], 0, 0

        temp_string = ""
        while codeptr < len(code):
            command = code[codeptr]
            if command == ">":
                cellptr += 1
                if cellptr == len(cells):
                    cells.append(0)
            if command == "<":
                cellptr = 0 if cellptr <= 0 else cellptr - 1
            if command == "+":
                temp = cells[cellptr] + 1 if cells[cellptr] < 255 else 0
                cells[cellptr] = temp
            if command == "-":
                temp = cells[cellptr] - 1 if cells[cellptr] > 0 else 255
                cells[cellptr] = temp
            if command == "[" and cells[cellptr] == 0:
                codeptr = bracemap[codeptr]
            if command == "]" and cells[cellptr] != 0:
                codeptr = bracemap[codeptr]
            if command == ".":
                temp_string += str(chr(cells[cellptr]))
            if command == ",":
                cells[cellptr] = ord(getch.getch())

            codeptr += 1
        return temp_string

    return(evaluate(code))
