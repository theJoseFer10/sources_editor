from curses import textpad
import curses

def pront_status(stdscr, mensaje, max_x):
    curses.echo()
    stdscr.addstr(curses.LINES -1, 0, mensaje[:max_x - 1])
    stdscr.clrtoeol()
    stdscr.refresh()
    entrada = stdscr.getstr(curses.LINES - 1, len(mensaje), max_x - len(mensaje) - 1)
    curses.noecho()
    return entrada.decode("utf-8").strip()

"""
def file_name_window(stdscr):
    win = curses.newwin(3, 40, 5, 10)
    win.border()
    stdscr.refresh()
    box = textpad.Textbox(win.derwin(1, 38, 1, 1))
    win.clear()
    win.refresh()
    del win 
    return box.edit().strip()
"""

def save_files(file_name, buffer):
    with open(file_name, "w", encoding='UTF-8') as f:
        for line in buffer:
            f.write(line+"\n")
