import json
import os
import sys

VALID_COLORS = {"black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"}
VALID_ATTRS = {"bold", "underline", "reverse"}


def _norm_color(name):
    if not isinstance(name, str):
        return "white"
    n = name.lower()
    return n if n in VALID_COLORS else "white"

def _norm_attrs_list(lts):
    if not isinstance(list, list):
        return []
    return [a.lower() for a in lts if isinstance(a, str) and a.lower() in VALID_ATTRS]

def cargar_configuracion(ruta="~/.zafiro/config.json"):
    ruta = os.path.expanduser(ruta)
    if not os.path.isfile(ruta):
        return {}
    try:
        with open(ruta, "r", encoding="UTF-8") as f:
            return json.load(f)
    except Exception:
        sys.stderr.write("Error al cargar configuración desde {}.\n".format(ruta))
        return {}
    
    color = cfg.get("colors", {})
    if isinstance(color, dict):
        for token, spec in color.items():
            if not isinstance(spec, dict):
                continue
            spec["fg"] = _norm_color(spec.get("fg"))
            spec["bg"] = _norm_color(spec.get("bg"))
            spec["attr"] = _norm_attrs_list(spec.get("attr"))
    return cfg
