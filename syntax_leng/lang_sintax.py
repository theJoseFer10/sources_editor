import curses

python_keywords = {
    "False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", 
    "continue", "def", "del", "elif", "else", "except", "finally", "for", "from", "global", 
    "if", "import", "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", 
    "try", "while", "with", "yield"
}

c_keywords = {
    "auto", "break", "case", "char", "const", "continue", "default", "do", "double", 
    "else", "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", 
    "return", "short", "signed", "sizeof", "static", "struct", "switch", "typedef", 
    "union", "unsigned", "void", "volatile", "while"
}

def draw_lines(stdscr, y, line, line_number_width, max_x, language, num_line):
    #Agregamos un número una validación para verificar que no haya errores en caso de 
	#que la línea este fuera de la pantalla.
    x = line_number_width
    try:
        stdscr.addstr(y, 0, f"{num_line+1}".rjust(line_number_width - 1) + " ")
    except curses.error:
        return

    i = 0
    while i < len(line):
        frament = line[i:]
        matched = False

        #Seleccionamos las palabras clave dependiendo de la extención del archivo que se este
        #editando.
        kw_set = python_keywords if language == "py" else c_keywords if language == "c" else set()
        for kw in kw_set:
            if frament.startswith(kw) and (i + len(kw) == len(line) or not line[i + len(kw)].isalnum()):
                try:
                    stdscr.addstr(y, x, kw, curses.color_pair(1))
                except curses.error:
                    pass
                x += len(kw)
                i += len(kw)
                matched = True
                break

        #Texto que este dentro de comillas.
        if not matched and line[i] in ('"', "'"):
            quote = line[i]
            end = i + 1
            while end < len(line):
                if line[end] == quote:
                    break
                end += 1
            if end >= len(line):
                #Validamos en caso de que sea un texto de comillas sin cerrar.
                fragment = line[i:]
                try:
                    stdscr.addstr(y, x, fragment, curses.color_pair(2))
                except curses.error:
                    pass
                x += len(fragment)
                i = len(line)
            else:
                fragment = line[i:end+1]
                try:
                    stdscr.addstr(y, x, fragment, curses.color_pair(2))
                except curses.error:
                    pass
                x += len(fragment)
                i = end + 1
            matched = True

        #Comentarios
        if not matched and line[i] == "#":
            try:
                stdscr.addstr(y, x, line[i:], curses.color_pair(3))
            except curses.error:
                pass
            break

        #Texto por defecto
        if not matched:
            try:
                stdscr.addstr(y, x, line[i])
            except curses.error:
                pass
            x += 1
            i += 1
