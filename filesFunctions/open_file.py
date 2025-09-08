def cargar_archivo(file_name):
	with open(file_name, "r", encoding='UTF-8') as f:
		lines = f.read().splitlines()
	return lines if lines else [""]
