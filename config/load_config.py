import json
def cargar_configuracion(ruta="config.json"):
	try:
		with open(ruta, "r", encoding="UTF-8") as f:
			return json.load(f)
	except Exception:
		return {}