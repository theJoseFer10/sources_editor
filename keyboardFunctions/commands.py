# commands.py
import time
from filesFunctions.saveFiles import save_files, pront_status
from filesFunctions.open_file import cargar_archivo

def runCommand(stdscr, key, buffer, open_file_name, max_x):
    max_y, _ = stdscr.getmaxyx()
    new_y, new_x = None, None

    if key == '\x1b':  # ESC
        commant = pront_status(stdscr, "| ", max_x)
        status = ""  # Initialize status variable

        if commant == "exit":
            return "exit", buffer, open_file_name, new_y, new_x
        elif commant == "save_as":
            file_name = pront_status(stdscr, "guardar como: ", max_x)
            if file_name:
                save_files(file_name, buffer)
                open_file_name = file_name
                status = f"Archivo '{file_name}' guardado..."
        elif commant == "open":
            file_name = pront_status(stdscr, "Abrir archivo: ", max_x)
            open_file_name = file_name
            try:
                buffer = cargar_archivo(file_name)
                status = f"Archivo '{file_name}' cargado correctamente.."
            except FileNotFoundError:
                status = f"Archivo '{file_name}' no encontrado.."
        elif commant == "save":
            if open_file_name:
                save_files(open_file_name, buffer)
                status = f"Archivo '{open_file_name}' guardado..."
            else:
                status = "No hay archivo abierto para guardar"
        elif commant == "help":
            status = "exit = salir | save_as = guardar como | save = guardar | open = abrir"
        elif commant == "return":
            status = "regresando..."
        else:
            status = f"Comando desconocido: {commant}"

        stdscr.addstr(max_y - 1, 0, status[:max_x - 1])
        stdscr.refresh()
        time.sleep(2)
        stdscr.clear()

    return None, buffer, open_file_name, new_y, new_x
