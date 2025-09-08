import curses
import signal
from keyboardFunctions.keyboard import shortcuts
from syntax_leng.lang_sintax import draw_lines
from keyboardFunctions.commands import runCommand
import time

stdscr_global = None

def resize_handler(signum, frame):
    if stdscr_global:
        curses.resizeterm(*stdscr_global.getmaxyx())

def setup_colors(stdscr):
    curses.start_color()
    if not curses.has_colors():
        stdscr.addstr(0, 0, "Tu terminal no admite colores")
        stdscr.clear()
        stdscr.getch()
        return False
    try:
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        return True
    except curses.error:
        stdscr.addstr(0, 0, "Error al iniciar colores.")
        stdscr.refresh()
        stdscr.getch()
        return False

def main(stdscr):
    global stdscr_global
    stdscr_global = stdscr
    curses.curs_set(1)
    #curses.raw permite un mejor manejo de teclas.
    curses.raw()
    if not setup_colors(stdscr):
        return
    stdscr.clear()
    stdscr.keypad(True)
    buffer = [""]
    open_file_name = None
    extension = None
    line_number_width = 5
    y, x = 0, 0
    offset_y = 0

    signal.signal(signal.SIGWINCH, resize_handler)

    BACKSPACE_KEYS = {'\x7f', '\177'}
    BACKSPACE_CODES = {curses.KEY_BACKSPACE, 127, 8, 263}

    while True:
        max_y, max_x = stdscr.getmaxyx()
        stdscr.erase()

        for i in range(offset_y, offset_y + max_y - 1):
            if i < len(buffer):
                line_number = f"{i+1}".rjust(line_number_width - 1) + " "
                draw_lines(stdscr, i - offset_y, buffer[i], line_number_width, max_x, num_line=i)

        status = f"Estado: Ln {y+1}, Col {x+1} | Screen: {max_y}x{max_x}"
        stdscr.addstr(max_y - 1, 0, status[:max_x - 1])

        x = max(0, min(x, max_x - line_number_width - 1))
        y = max(0, y)

        if y - offset_y >= max_y - 2:
            offset_y += 1
        elif y - offset_y < 0:
            offset_y = max(0, offset_y - 1)

        stdscr.move(y - offset_y, x + line_number_width)
        stdscr.refresh()

        try:
            key = stdscr.get_wch()
        except curses.error:
            continue

        if isinstance(key, int) and key in (127, 8, 263, curses.KEY_BACKSPACE):
            key = '\x7f'

        if isinstance(key, str):
            res_cmd, buffer, open_file_name, new_y, new_x = runCommand(
                stdscr, key, buffer, open_file_name, max_x
            )
            res_short, buffer, open_file_name, new_y2, new_x2 = shortcuts(
                stdscr, key, buffer, open_file_name, max_x
            )

            if res_cmd == "exit" or res_short == "exit":
                break

            # Solo actualiza si se devuelve una nueva posición
            if new_y2 is not None and new_x2 is not None:
                y, x = new_y2, new_x2
            elif new_y is not None and new_x is not None:
                y, x = new_y, new_x

            if key == '\n':  # ENTER
                buffer.insert(y+1, buffer[y][x:])
                buffer[y] = buffer[y][:x]
                y += 1
                x = 0

            elif key == "\x7f":
            #in ('\x08', '\x7f', '\x1b', 127, 8, 263, curses.KEY_BACKSPACE) :
                if x > 0:
                    buffer[y] = buffer[y][:x-1] + buffer[y][x:]
                    x -= 1
                elif y > 0 and y-1 < len(buffer):
                    x = len(buffer[y-1])
                    buffer[y-1] += buffer[y]
                    buffer.pop(y)
                    y -= 1

            elif key.isprintable():
                if x >= max_x - line_number_width - 1:
                    if y == len(buffer) - 1:
                        buffer.append("")
                    y += 1
                    x = 0
                while y >= len(buffer):
                    buffer.append("")
                buffer[y] = buffer[y][:x] + key + buffer[y][x:]
                x += 1

            elif key == "\t":
                if x >= max_x - line_number_width -1:
                    if y == len(buffer) - 1:
                        buffer.append("")
                    y += 1
                    x = 0
                while y > len(buffer):
                    buffer.append("")
                buffer[y] = buffer[y][:x] + (" " * 4) + buffer[y][:x]
                x += 4


        elif isinstance(key, int):
            if key == curses.KEY_UP:
                y = max(0, y - 1)
                x = min(x, len(buffer[y]))
            elif key == curses.KEY_DOWN:
                y = min(len(buffer) - 1, y + 1)
                x = min(x, len(buffer[y]))
            elif key == curses.KEY_LEFT:
                x = max(0, x - 1)
            elif key == curses.KEY_RIGHT:
                x = min(len(buffer[y]), x + 1)

curses.wrapper(main)