import curses
import signal
import sys
import os
from keyboardFunctions.keyboard import shortcuts
from syntax_leng.lang_sintax import draw_lines
from keyboardFunctions.commands import runCommand
from filesFunctions.open_file import cargar_archivo
from config.load_config import cargar_configuracion

stdscr_global = None

def resize_handler(signum, frame):
    if stdscr_global:
        curses.resizeterm(*stdscr_global.getmaxyx())

def setup_colors(stdscr, config = None):
    curses.start_color()
    curses.use_default_colors()
    try:
        curses.curs_set(config.get("cursorVisible", 1))
    except Exception:
        pass

    stdscr.nodelay(False)
    stdscr.timeout(-1)

    if (config or {}).get("mouse", {}).get("enabled"):
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        
    # Verificamos que el terminal soporte colores.
    if not curses.has_colors():
        stdscr.addstr(0, 0, "Tu terminal no admite colores")
        stdscr.clear()
        stdscr.getch()
        return False, {}
    
    # Helper para resolver nombres de colores a códigos de curses.
    def color_by_name(name):
        if not isinstance(name, str):
            return curses.COLOR_WHITE
        try:
            return getattr(curses, "COLOR_" +  name.upper())
        except Exception:
            return curses.COLOR_WHITE
        
    # Valores por defecto.
    base_style = {
        "keyword": {"fg": "CYAN", "bg": "BLACK", "attr": ["bold"]},
        "string": {"fg": "GREEN", "bg": "BLACK", "attr": []},
        "comment": {"fg": "RED", "bg": "BLACK", "attr": []},
        "default": {"fg": "WHITE", "bg": "BLACK", "attr": []},
    }
    
    # Mezclar con configuración si está disponible.
    cfg_colors = {}
    if config:
        cfg_colors = config.get("colors", {})
        
    for toke, defaults in base_style.items():
        user = cfg_colors.get(toke, {})
        if "fg" in user:
            defaults["fg"] = user["fg"]
        if "bg" in user:
            defaults["bg"] = user["bg"]
        if "attr" in user and isinstance(user["attr"], list):
            defaults["attr"] = user["attr"]
            
    # Inicializar pares de colores.
    style_out = {}
    pair_index = 1
    for token, val in base_style.items():
        fg = color_by_name(val["fg"])
        bg = color_by_name(val["bg"])
        
        try:
            curses.init_pair(pair_index, fg, bg)
        except curses.error:
            curses.init_pair(pair_index, curses.COLOR_WHITE, curses.COLOR_BLACK)
        attr = 0
        for a in val.get("attr", []):
            if a.lower() == "bold":
                attr |= curses.A_BOLD
            elif a.lower() == "underline":
                attr |= curses.A_UNDERLINE
            elif a.lower() == "reverse":
                attr |= curses.A_REVERSE
        
        style_out[token] = {"pair": pair_index, "attr": attr}
        pair_index += 1
        
    return True, style_out
    
def main(stdscr):
    global stdscr_global
    stdscr_global = stdscr

    ruta_config = os.path.expanduser("~/.zafiro/config.json")
    config = cargar_configuracion(ruta_config)
    tabsize = config.get("tabSize", 4)

    curses.curs_set(1)
    #curses.raw permite un mejor manejo de teclas.
    curses.raw()
    ok, styles = setup_colors(stdscr, config)
    if not ok:
        return
    stdscr.clear()
    stdscr.keypad(True)
    #Verificamos la que exista el archivo que se envió como parametro.
    if len(sys.argv) > 1:
        file_to_open = sys.argv[1]
        if os.path.isfile(file_to_open):
            buffer = cargar_archivo(file_to_open)
            open_file_name = file_to_open
        else:
            buffer=[""]
            open_file_name = None
    else:
        buffer=[""]
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
        visible_lines = max_y - 1
        if y < offset_y:
            offset_y = y
        elif y>=offset_y + visible_lines - 1:
            offset_y = y - visible_lines + 2
        stdscr.erase()

        for i in range(offset_y, offset_y + visible_lines):
            if i < len(buffer):
                line_number = f"{i+1}".rjust(line_number_width - 1) + " "
                draw_lines(stdscr, i - offset_y, buffer[i], line_number_width, max_x, num_line=i, styles = styles)

        status = f"Estado: Ln {y+1}, Col {x+1} | Screen: {max_y}x{max_x}"
        stdscr.addstr(max_y - 1, 0, status[:max_x - 1])

        x = max(0, min(x, max_x - line_number_width - 1))
        y = max(0, y)

        if y - offset_y >= max_y - 2:
            offset_y += 1
        elif y - offset_y < 0:
            offset_y = max(0, offset_y - 1)

        cursor_y = y - offset_y
        cursor_x = x + line_number_width
        if 0 <= cursor_y < visible_lines and 0 <= cursor_x < max_x:
            stdscr.move(cursor_y, cursor_x)
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
                while y >= len(buffer):
                    buffer.append("")
                if x > len(buffer[y]):
                    buffer[y] = buffer[y] + (" " * (x - len(buffer[y])))
                buffer[y] = buffer[y][:x] + (" " * tabsize) + buffer[y][x:]
                x += tabsize


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
