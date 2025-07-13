import curses
from saveFiles import save_files, pront_status
from open_file import cargar_archivo
from syntax_leng.python_sintax import draw_lines
#from prompt_toolkit import prompt
def setup_colors(stdscr):
        curses.start_color()
        if not curses.has_colors():
            stdscr.addstr(0,0,"Tu terminal no admite colores")
            stdscr.clear()
            stdscr.getch()
            return
        try:
            curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            return True
        except curses.error:
            stdscr.addstr(0, 0, "Error al iniciar colores.")
            stdscr.refresh()
            stdscr.getch()
            return False
#inicamos el editor con la funcion main
#stdscr es el objeto principal, se encarga de dibuar y leer entradas de texto.
def main(stdscr):
    curses.curs_set(1)
    if not setup_colors(stdscr):
        return
    stdscr.clear()
    buffer = [""]
    open_file_name = None
    #Cuatro bits para números y uno para espacios.
    line_number_width = 5
    y, x = 0, 0
    offset_y = 0

#Manipulación del buffer de información.
    while True:
        #Obtenemos los valores maximos tanto de x como de y.
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()

        for i in range(offset_y, offset_y + max_y - 1):
            if i < len(buffer):
                line_number = f"{i+1}".rjust(line_number_width - 1) + " "
                text = line_number + buffer[i]
                draw_lines(stdscr, i - offset_y, buffer[i], line_number_width, max_x)
                #stdscr.addstr(i - offset_y, 0, text[:max_x - 1])        
        """
        for i, line in enumerate(buffer):
            if i < max_y - 1:  # evita escribir en la línea del status
                line_number = f"{i+1}".rjust(line_number_width - 1) + " "
                text = line_number + line
                stdscr.addstr(i, 0, text[:max_x - 1])  # trunca si es necesario
        """
                
                
        #Mostramos el status del cursor y de la pantalla en la fila que reservamos adelante.
        status = f"Estado: Ln {y+1}, Col {x+1} | Screen: {max_y}x{max_x}"
        stdscr.addstr(max_y - 1, 0, status[:max_x - 1])
        #Definimos un valor maximo para ambos.
        x = max(0, min(x, max_x - line_number_width - 1))
        y = max(0, y)
        if y - offset_y >= max_y -2:
            offset_y += 1
        elif y - offset_y < 0:
            offset_y = max(0, offset_y - 1)
        stdscr.move(y - offset_y, x + line_number_width)
        stdscr.refresh()
        key = stdscr.getch()

        #Termina el programa cuando se presiona "esc"
        if key == 27:
            commant = pront_status(stdscr,"| ", max_x)
            if commant == "exit":
                break

            elif commant == "save_as":
                file_name = pront_status(stdscr, "guardar como: ", max_x)
                #file_name = file_name_window(stdscr)
                #file_name = prompt("Nombre del archivo y extensión: ")
                if file_name:
                    save_files(file_name, buffer)
                    y, x = 0, 0
                    status = f"Archivo '{file_name}' guardado."
                stdscr.clear()

            elif commant == "open":
                    file_name = pront_status(stdscr, "Abrir archivo: ", max_x)
                    open_file_name = file_name
                    try:
                        buffer = cargar_archivo(file_name)
                        y, x = 0, 0
                        status = f"Archivo {file_name} cargado correctamente"
                    except FileNotFoundError:
                        status = f"Archivo {file_name} no encontrado"

            elif commant == "save":
                if open_file_name:
                    save_files(open_file_name, buffer)
                    status = f"Archivo '{open_file_name}' guardado."

        #Actualiza el buffer cada vez que ingresamos caracteres a la lista.
        elif 32 <= key <= 126:
            if x >= max_x -line_number_width -1:
                if y == len(buffer)-1:
                    buffer.append("")
                y += 1
                x = 0
            while y >= len(buffer):
                buffer.append("")

            buffer[y] = buffer[y][:x] + chr(key) + buffer[y][x:]
            x += 1

        #Actualiza rl buffer cada vez que quitamos caracteres de la lista.
        elif key in (curses.KEY_BACKSPACE, 127):
            if x > 0:
                buffer[y] = buffer[y][:x-1] + buffer[y][x:]
                x -= 1
            elif y > 0:
                x = len(buffer[y-1])
                buffer[y-1] += buffer[y]
                buffer.pop(y)
                y -= 1

        #Realiza un salto de linea cundo presiona "ENTER"
        elif key == curses.KEY_ENTER or key == 10:
            buffer.insert(y+1, buffer[y][x:])
            buffer[y] = buffer[y][:x]
            y += 1
            x = 0

        #Navegación por la pantalla usando las teclas de flecha.
        elif key == curses.KEY_UP:
            y = max(0, y - 1)
            x = min(x, len(buffer[y]))
        elif key == curses.KEY_DOWN:
            y = min(len(buffer) - 1, y + 1)
            x = min(x, len(buffer[y]))
        elif key == curses.KEY_LEFT:
            x = max(0, x - 1)
        elif key == curses.KEY_RIGHT:
            x = min(len(buffer[y]), x + 1)

        else:
            buffer[y] = buffer[y][:x] + chr(key) + buffer[y][x:]
            x += 1

curses.wrapper(main)
