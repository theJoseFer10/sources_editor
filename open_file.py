def cargar_archivo(file_name):
	with open(file_name, "r") as f:
		lines = f.read().splitlines()
	return lines if lines else [""]