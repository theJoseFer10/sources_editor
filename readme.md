###################################################
 _____  ______          _____        __  __ ______ 
|  __ \|  ____|   /\   |  __ \      |  \/  |  ____|
| |__) | |__     /  \  | |  | |     | \  / | |__   
|  _  /|  __|   / /\ \ | |  | |     | |\/| |  __|  
| | \ \| |____ / ____ \| |__| |  _  | |  | | |____ 
|_|  \_\______/_/    \_\_____/  (_) |_|  |_|______|
                                                   
###################################################

# 🧠 ZafiroEd — Editor de texto ligero en terminal Un editor de texto y código ligero diseñado para equipos con recursos limitados.

## Características

- 📄 Edición de texto con numeración de líneas
- 💾 Guardar y abrir archivos (`save`, `save_as`, `open`)
- 🎨 Resaltado de sintaxis para Python y C
- 🖥️Detección dinámica del tamaño de la terminal
- 🧭 Navegación con flechas y scroll vertical
- 🎨 Personalización mediante archivo Json.
---

## compilación e instalación

### compilar e instalar para debian.
requisitos.
- python3.
- dpkg.

#### instalación
- Ingresa al apartado de descargas en el sitio web.
- Descarga el archivo correspondiente para tu sistema linux.
- Sistemas basados en debian ejecuta el comando: ```sudo dpkg -i zafiro.deb```
- Sistemas basados en arch ejecuta el comando: ```sudo pacman -i zafiro-1.0.1-1-any.pkg.tar.zst```

#### Comprovación
- Ejecuta el comando zafiro.

---
### compilar e instalar para windows.
#### Requisitos
- python3
- pip
- pyinstaller

#### procedimiento.
- posicionase en el directorio donde se encuentra el main.py

- ejecutar el siguiente comando.
```
pyinstaller --onefile zafiroed.py
# esto creara un ejecutable con la terminal.
```
---
## Funcionamiento.

Es un editor de texto y código simialr a nano y vim.
Para ejecutar comando presionamos la tecla "esc", esto permite introducir comandos en donde se encuentra la barra de
status.

## Parametros de comando.
Si quieres abrir un archivo con zafiro que se encuentra dentro del mismo directorio, puedes ejecutrar el siguiente comando.
"zafiro archivo.extension"

```zafiro main.py```

Si el editor encuentra el archivo en ese directorio entonces lo abrirá.

## Comandos funcionales.
```
exit --> "Termina el programa".
save_as --> "Guardar como".
save --> "Guardar cambios en archivos ya existentes".
open --> "Abrir archivos guardados en nuestro equipo".
help --> "Muestra los comandos disponibles y su funcion".
return --> "regresamos al modo edicion".
```
```
#Atajos de teclado.
ctrl + a --> "Guardar como".
ctrl + s --> "Guardar".
ctrl + o --> "Abrir archivo".
ctrl + q --> "Terminar el programa".
ctrl + x --> "Cerrar archivo y vaciar buffer".
```
---
## Personalización del editor.
Si quieres personalizar el editor a tu gusto, puedes hacerlo de la siguiente manera.
- Crea el directorio oculto .zafiro con el siguiente comando: "mkdit .zafiro"
- Ingresa al directorio con el siguiente comando: ```cd ~/.zafiro```
- Crea un archivo llamado "config.json".
- Puedes crear tu propia configuración o puedes visitar nuestra biblioteca de temas en nuestro sitio web.

---
## Filosofía

ZafiroEd nace del deseo de crear herramientas que respeten el entorno del terminal, sin depender de interfaces gráficas
ni librerías pesadas. Cada línea está pensada para ser clara, funcional y extensible.

---
## Licencia

Este proyecto es de código abierto. Puedes usarlo, modificarlo y compartirlo libremente.
