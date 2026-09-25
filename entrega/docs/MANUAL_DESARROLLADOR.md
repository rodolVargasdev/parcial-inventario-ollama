# Manual del desarrollador

Asistente de Inventario para PYMES con Ollama local.

## 1. Visión general

Todo el programa está en un solo archivo, main.py, escrito con Python, Tkinter y la librería ollama, siguiendo el estilo de los ejemplos vistos en clase (ollama1.py a ollama5.py).

Flujo: el usuario escribe una consulta, el botón Enviar llama a ollama.chat con el modelo qwen3.5:0.8b y la respuesta se muestra en el área de texto.

No usa internet, ni base de datos, ni servicios en la nube.

## 2. Partes del código

### 2.1 Configuración
- MODELO = "qwen3.5:0.8b": modelo destilado de menos de 3B parámetros, el mismo de la guía de clase.
- INTEGRANTES: lista con nombre y carné de cada integrante.
- CONTEXTO: mensaje de sistema que le indica al modelo que actúe como asistente de inventario de una ferretería. Sin este mensaje el modelo responde de forma genérica.
- CARPETA: ruta donde está main.py, para encontrar la foto y guardar los .txt aunque el programa se ejecute desde otra carpeta.

### 2.2 Función enviar()
- Valida que el campo no esté vacío.
- Cambia la etiqueta de estado a "Consultando..." y llama root.update() para que se vea el cambio antes de esperar al modelo.
- Llama ollama.chat con dos mensajes: el de sistema (CONTEXTO) y el del usuario.
- Agrega la pregunta y la respuesta al área de texto.
- Si Ollama no está abierto o el modelo no está descargado, muestra el error en un messagebox.

Detalle importante: ollama.chat espera la respuesta completa, por lo que la ventana queda ocupada mientras el modelo responde. Se eligió así por simplicidad, igual que en ollama5.py.

### 2.3 Función guardar()
- Toma todo el texto del área de respuestas.
- Lo guarda en un archivo consulta_AAAAMMDD_HHMMSS.txt junto a main.py, con codificación UTF-8.

### 2.4 Función ver_integrantes()
- Abre una ventana nueva (Toplevel).
- Si existe assets/foto.jpg, la muestra reducida con Pillow. La imagen se guarda en ventana.foto porque, si no se guarda una referencia, Tkinter la borra y no aparece.
- Muestra los nombres y carnés de INTEGRANTES.

### 2.5 Ventana principal
- Tamaño fijo de 600x600 con resizable(False, False).
- Colores verdes, asociados a orden, control y dinero, adecuados para un asistente de inventario.
- Controles: título, campo de consulta, botón Enviar consulta, área de respuestas, botones Guardar en .txt y Ver integrantes, y etiqueta de estado.

## 3. Dependencias

- ollama 0.6.2: cliente para hablar con el servidor Ollama local.
- pillow 12.3.0: para mostrar la foto JPG.
- Tkinter viene incluido con Python.

## 4. Posibles mejoras

- Mostrar la respuesta por partes con stream=True, como en ollama2.py.
- Guardar el inventario en una base sqlite3.
- Permitir elegir el modelo desde una lista.
