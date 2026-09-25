# Manual del desarrollador

Asistente de Inventario PYME con Ollama local.

## 1. Visión general

El programa está en un solo archivo, main.py, escrito con Python, Tkinter (con widgets ttk) y la librería ollama. Se ejecuta 100% en local con el modelo destilado qwen3.5:0.8b, de menos de 3B parámetros.

Flujo: el usuario escribe una consulta, el botón Enviar llama a ollama.chat, la respuesta se agrega al historial y todo el historial se puede guardar en un .txt.

## 2. Configuración (inicio del archivo)

- MODELO: nombre del modelo de Ollama. Cambiarlo aquí cambia el modelo en todo el programa.
- CONTEXTO: mensaje de sistema que le indica al modelo que actúe como asistente de inventario para PYMES e incluye un inventario de ejemplo (arroz, frijol, aceite, azúcar, leche en polvo y café) para que pueda responder preguntas como "¿cuál es el inventario que tenemos?".
- WINDOW_WIDTH y WINDOW_HEIGHT: 600x600, tamaño exigido. La ventana no se puede redimensionar.
- COLORS: paleta verde azulado con fondo claro, asociada a orden, confianza y control, adecuada para un asistente de inventario.

## 3. Clase InventarioApp

- __init__: crea la ventana, fija el tamaño y construye estilos e interfaz. Guarda la conversación en la lista self.conversacion.
- construir_estilos: define los estilos ttk del botón principal y de los secundarios.
- construir_interfaz: arma el encabezado, el historial (Text de solo lectura con barra de desplazamiento), el campo de consulta, el botón Enviar y los botones de guardar e integrantes. La tecla Enter también envía.
- agregar_mensaje: inserta un mensaje en el historial y lo guarda en self.conversacion.
- obtener_respuesta: llama a ollama.chat con el CONTEXTO, la consulta y think=False. Si Ollama no está abierto o falta el modelo, devuelve un mensaje con la solución en lugar de cerrar el programa.
- enviar_consulta: valida que la consulta no esté vacía, la muestra, desactiva el botón (que dice "Pensando...") y lanza la consulta en un hilo aparte.
- consultar_en_segundo_plano y mostrar_respuesta: el hilo espera al modelo y, con root.after, devuelve la respuesta al hilo principal, que es el único que puede modificar la ventana.
- guardar_conversacion: abre un cuadro para elegir dónde guardar (por defecto documento.txt) y escribe la fecha y toda la conversación en UTF-8.
- mostrar_integrantes: abre una ventana nueva con la primera imagen de la carpeta "foto integrantes" y los nombres y carnés del grupo. La imagen se guarda en self.imagen_referencia porque, si no se guarda una referencia, Tkinter la borra y no aparece.

## 4. Detalles importantes

- La consulta corre en un hilo aparte (threading) para que la ventana no se congele mientras el modelo responde.
- think=False desactiva el razonamiento previo de qwen3.5. En pruebas del 24/09/2026, la misma pregunta tardó 68.9 s con razonamiento y 7.3 s sin él.
- Si Pillow no está instalado, el botón de integrantes muestra un aviso en lugar de fallar.
- No se usa internet, base de datos ni servicios en la nube.

## 5. Dependencias

- ollama 0.6.2: cliente para hablar con el servidor Ollama local.
- pillow 12.3.0: para mostrar la foto JPEG.
- Tkinter viene incluido con Python.

## 6. Posibles mejoras

- Mostrar la respuesta por partes con stream=True.
- Guardar el inventario real en una base sqlite3.
- Enviar el historial completo al modelo para que recuerde la conversación.
