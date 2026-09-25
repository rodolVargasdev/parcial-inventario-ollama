# Manual de usuario

Asistente de Inventario PYME con Ollama local.

## 1. Qué es

Un programa de escritorio que responde preguntas sobre el inventario de una pequeña empresa: existencias, productos con bajo stock, compras, proveedores, ventas y vencimientos. Funciona sin internet, con un modelo de inteligencia artificial que se ejecuta en la propia computadora.

## 2. Características de la computadora

| Componente | Mínimo | Recomendado |
|---|---|---|
| Sistema operativo | Windows 10 de 64 bits | Windows 11 |
| Procesador | 4 núcleos | 6 núcleos o más |
| Memoria RAM | 8 GB | 16 GB |
| Espacio en disco | 5 GB libres | 10 GB libres |
| Tarjeta de video | No es necesaria | Opcional, acelera las respuestas |

## 3. Programas necesarios

- Python 3.10 o superior (https://www.python.org/downloads), marcando la opción "Add Python to PATH" al instalar.
- Ollama (https://ollama.com/download).
- El modelo qwen3.5:0.8b, de menos de 3B parámetros.
- Las librerías del archivo requirements.txt: ollama y pillow.

## 4. Instalación (una sola vez)

1. Instale Python y Ollama.
2. Abra una terminal en la carpeta del proyecto.
3. Descargue el modelo:

```
ollama pull qwen3.5:0.8b
```

4. Instale las librerías:

```
pip install -r requirements.txt
```

## 5. Cómo abrir el programa

### Opción rápida: AsistenteInventario.exe
1. Verifique que Ollama esté abierto y que el modelo esté descargado (ollama pull qwen3.5:0.8b).
2. Haga doble clic en AsistenteInventario.exe. No necesita Python instalado.
3. Mantenga la carpeta "foto integrantes" junto al .exe para que se vea la foto.
4. Si Windows muestra "Windows protegió su PC", presione "Más información" y luego "Ejecutar de todas formas"; aparece porque el .exe no tiene firma digital.

### Opción con Python

1. Verifique que Ollama esté abierto (su ícono aparece junto al reloj de Windows).
2. En la carpeta del proyecto ejecute:

```
python main.py
```

3. Se abre la ventana "Asistente de Inventario PYME" de 600x600.

## 6. Uso

### Hacer una consulta
1. Escriba la pregunta en el campo "Escribe una consulta sobre tu inventario".
2. Presione Enviar o la tecla Enter.
3. El botón cambia a "Pensando..." mientras el modelo responde; la ventana se puede seguir moviendo. La primera consulta puede tardar más.
4. La respuesta aparece en el historial como "Asistente".

Ejemplos:
- ¿Cuál es el inventario que tenemos?
- ¿Qué hago con los productos que tienen menos de 10 unidades?
- ¿Cómo organizo las compras por proveedor?
- ¿Cómo controlo los productos próximos a vencer?

### Guardar las consultas
1. Presione "Guardar consultas en documento.txt".
2. Elija la carpeta y el nombre (por defecto documento.txt).
3. El archivo contiene la fecha y toda la conversación.

### Ver los integrantes
1. Presione "Mostrar integrantes del grupo".
2. Se abre una ventana con la foto del grupo y los nombres y carnés.

## 7. Problemas comunes

| Síntoma | Causa | Solución |
|---|---|---|
| "No se pudo consultar a Ollama" | Ollama cerrado o modelo no descargado | Abra Ollama y ejecute ollama pull qwen3.5:0.8b |
| Error "No module named ollama" | Faltan las librerías | Ejecute pip install -r requirements.txt |
| "Falta Pillow" | No se instaló pillow | Ejecute pip install -r requirements.txt |
| "Imagen no encontrada" | La carpeta "foto integrantes" está vacía | Coloque la foto del grupo en esa carpeta |
| Respuesta lenta | Primera carga del modelo o poca RAM | Espere y cierre otros programas pesados |

## 8. Privacidad

Todo se procesa en la computadora. Ninguna consulta sale a internet, y el .txt solo se crea cuando se presiona el botón de guardar.
