###################################################
 _____  ______          _____        __  __ ______ 
|  __ \|  ____|   /\   |  __ \      |  \/  |  ____|
| |__) | |__     /  \  | |  | |     | \  / | |__   
|  _  /|  __|   / /\ \ | |  | |     | |\/| |  __|  
| | \ \| |____ / ____ \| |__| |  _  | |  | | |____ 
|_|  \_\______/_/    \_\_____/  (_) |_|  |_|______|
                                                   
###################################################

# 🧠 ZafiroEd — Editor de texto ligero en terminal
# Un editor de texto y código ligero diseñado para equipos con recursos limitados.

---

## ✨ Características

- 📄 Edición de texto con numeración de líneas
- 💾 Guardar y abrir archivos (`save`, `save_as`, `open`)
- 🎨 Resaltado de sintaxis para Python y C
- 🖥️Detección dinámica del tamaño de la terminal
- 🧭 Navegación con flechas y scroll vertical

---

## 🛠️ compilación e instalación

#compilar e instalar para debian.
requisitos.
1- python3.
2- dpkg.

instalación
1- el sistema debe de tener lla siguiente estructura.
.
├── DEBIAN
│   └── control
└── usr
    └── bin
        ├── lang_sintax.py
        ├── main.py
        ├── open_file.py
        ├── saveFiles.py
        └── zafiroed

2- en el archivo "zafiroed" debe de ir el siguiente encabezado.
#!/usr/bin/env python3

3- ejecutamos el siguiente comando.
dpkg-deb --build zafiroed

4- instalación.
sudo dpkg -i zafiroed
(nos debemos posicionar el el directorio donde esta el .deb)
una vez instalado, podremos acceder a el con el comando zafiroed.

#compilar e instalar para windows.
--Requisitos--
1- python3
2- pip
3- pyinstaller

procedimiento.
1- posicionase en el directorio donde se encuentra el main.py

2- ejecutar el siguiente comando.
pyinstaller --onefile zafiroed.py
esto creara un ejecutable con la terminal.

---

## 🔨 Funcionamiento.

Es un editor de texto y código simialr a nano y vim.
Para ejecutar comando presionamos la tecla "esc", esto permite introducir comandos en donde se encuentra la barra de
status.

#Comandos funcionales.
exit -- "Termina el programa".
save_as -- "Guardar como".
save -- "Guardar cambios en archivos ya existentes".
open -- "Abrir archivos guardados en nuestro equipo".
help -- "Muestra los comandos disponibles y su funcion".
return -- "regresamos al modo edicion".

---

## 🧠 Filosofía

ZafiroEd nace del deseo de crear herramientas que respeten el entorno del terminal, sin depender de interfaces gráficas
ni librerías pesadas. Cada línea está pensada para ser clara, funcional y extensible.

---

## 📜 Licencia

Este proyecto es de código abierto. Puedes usarlo, modificarlo y compartirlo libremente.
