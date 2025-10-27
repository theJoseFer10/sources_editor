#Función para dibujar la barra de estados.
#En dado caso de que el valor de "y" no es especifique, su valor será el de la ultima linea. (se recomienda siempre especificar el valor de Y).
import curses
def draw_status(win, text, max_x, y = None, color_pair=0):
	height, _ = win.getmaxyx()
	#Una linea antes del borde.
	line_y = y if y is not None else height - 2
	try:
		if color_pair:
			win.attron(curses.color_pair(color_pair))
		win.addstr(line_y, 1, text[:max_x - 2])
		if color_pair:
			win.attroff(curses.color_pair(color_pair))
		win.refresh()
	except curses.error:
		pass