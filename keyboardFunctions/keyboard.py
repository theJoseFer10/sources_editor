# keyboard.py
import time
from filesFunctions.saveFiles import save_files, pront_status
from filesFunctions.open_file import cargar_archivo

def shortcuts(stdscr, key, buffer, open_file_name, max_x):
    max_y, _ = stdscr.getmaxyx()
    new_y, new_x = None, None

    if key == '\x13':  # Ctrl+S
        if open_file_name:
            save_files(open_file_name, buffer)
            status = f"Archivo '{open_file_name}' guardado..."
            stdscr.addstr(max_y - 1, 0, status[:max_x - 1])
            stdscr.refresh()
            time.sleep(2)

    elif key == '\x01':  # Ctrl+A
        file_name = pront_status(stdscr, "guardar como: ", max_x)
        if file_name:
            save_files(file_name, buffer)
            open_file_name = file_name
            status = f"Archivo '{file_name}' guardado..."
            stdscr.addstr(max_y - 1, 0, status[:max_x - 1])
            stdscr.refresh()
            time.sleep(2)
            stdscr.clear()

    elif key == '\x0F':  # Ctrl+O
        file_name = pront_status(stdscr, "Abrir archivo: ", max_x)
        open_file_name = file_name
        try:
            buffer = cargar_archivo(file_name)
            status = f"Archivo '{file_name}' cargado correctamente.."
        except FileNotFoundError:
            status = f"Archivo '{file_name}' no encontrado.."
        stdscr.addstr(max_y - 1, 0, status[:max_x - 1])
        stdscr.refresh()
        time.sleep(2)

    elif key == '\x18':  # Ctrl+X
        if open_file_name:
            save_files(open_file_name, buffer)
        else:
            res = pront_status(stdscr, "Quieres guardar antes de cerrar? (s/n): ", max_x)
            if res == "s":
                file_name = pront_status(stdscr, "Guardar archivo antes de cerrar: ", max_x)
                save_files(file_name, buffer)
        buffer = [""]
        open_file_name = None
        new_y, new_x = 0,0
        status = "Archivo cerrado correctamente"
        stdscr.clear()
        stdscr.addstr(max_y - 1, 0, status[:max_x - 1])
        stdscr.refresh()
        time.sleep(1)

    elif key == '\x11':  # Ctrl+Q
        res = pront_status(stdscr, "Quieres guardar antes de cerrar? (s/n): ", max_x)
        if res == "s":
            file_name = pront_status(stdscr, "Guardar archivo antes de cerrar: ", max_x)
            save_files(file_name, buffer)
        return "exit", buffer, open_file_name, new_y, new_x

    return None, buffer, open_file_name, new_y, new_x
