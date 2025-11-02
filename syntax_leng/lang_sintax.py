import curses

python_keywords = {
    "False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", 
    "continue", "def", "del", "elif", "else", "except", "finally", "for", "from", "global", 
    "if", "import", "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", 
    "try", "while", "with", "yield", "print", "main"
}

c_keywords = {
    "auto", "break", "case", "char", "const", "continue", "default", "do", "double", 
    "else", "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", 
    "return", "short", "signed", "sizeof", "static", "struct", "switch", "typedef", 
    "union", "unsigned", "void", "volatile", "while", "printf", "main", "scanf"
}

def draw_lines(stdscr, y, line, line_number_width, max_x, num_line, styles=None):
    #Agregamos un número una validación para verificar que no haya errores en caso de 
	#que la línea este fuera de la pantalla.
    x = line_number_width
    try:
        stdscr.addstr(y, 0, f"{num_line+1}".rjust(line_number_width - 1) + " ")
    except curses.error:
        return
    
    # helpers para optener atributos seguros.
    def style_for(token):
        if not styles:
            return curses.color_pair(1) | 0
        s = styles.get(token, {"pair": 1, "attr": 0})
        return curses.color_pair(s["pair"]) | s["attr"]
    
    def is_ident_char(ch):
        return ch.isalnum() or ch == '_'
    
    i = 0
    while i < len(line):
        frament = line[i:]
        matched = False

        #Seleccionamos las palabras clave dependiendo de la extención del archivo que se este
        #editando.
        kw_set = python_keywords.union(c_keywords)
        for kw in sorted(kw_set, key=len, reverse=True):
            start_ok = (i == 0) or (not is_ident_char(line[i - 1]))
            end_pos = i + len(kw)
            end_ok = (end_pos >= len(line)) or (not is_ident_char(line[end_pos]))
            if frament.startswith(kw) and start_ok and end_ok:
                try:
                    stdscr.addstr(y, x, kw, style_for("keyword"))
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
                    stdscr.addstr(y, x, fragment, style_for("string"))
                except curses.error:
                    pass
                x += len(fragment)
                i = len(line)
            else:
                fragment = line[i:end+1]
                try:
                    stdscr.addstr(y, x, fragment, style_for("string"))
                except curses.error:
                    pass
                x += len(fragment)
                i = end + 1
            matched = True

        #Comentarios
        if not matched and line[i] == "#":
            try:
                stdscr.addstr(y, x, line[i:], style_for("comment"))
            except curses.error:
                pass
            break

        #Texto por defecto
        if not matched:
            try:
                stdscr.addstr(y, x, line[i], style_for("default"))
            except curses.error:
                pass
            x += 1
            i += 1
