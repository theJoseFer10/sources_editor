import curses

python_keywords = {"False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", 
"continue", "def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import", 
"in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with", "yield"
}

def draw_lines(stdscr, y, line, line_number_width, max_x, language="python"):

	x = line_number_width
	stdscr.addstr(y, 0, f"{y+1}".rjust(line_number_width - 1)+" ")

	i = 0
	while i < len(line) :
		frament = line[i:]
		matched = False

		#Establecemos las palabras.
		kw_set = python_keywords if language == "python" else set()
		for kw in kw_set:
			if frament.startswith(kw) and (i+len(kw) == len(line) or not line[i+len(kw)].isalnum()):
				stdscr.addstr(y, x, kw, curses.color_pair(1))
				x += len(kw)
				i += len(kw)
				matched = True
				break

		#Cadenas de texto.
		if not matched and line[i] in('"', '"'):
			quote = line[i]
			end = i + 1
			while end < len(line) and line[end] != quote:
				end += 1
			stdscr.addstr(y, x, line[i:end+1], curses.color_pair(2))
			x += (end - i + 1)
			i = end + 1
			matched = True

		#Comentarios.
		if not matched and line[i] == "#":
			stdscr.addstr(y, x, line[i:], curses.color_pair(3))
			break

		#Texto por defecto.
		if not matched:
			stdscr.addstr(y, x, line[i], curses.color_pair(4))
			x += 1
			i += 1