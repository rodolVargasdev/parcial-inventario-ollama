# MANUAL DE USUARIO - Asistente de Inventario para Ferreterias PYME
### Parte II-2 + Parte III (35% + 30%)

## 1. Que es

Software de escritorio que responde preguntas de inventario ferretero usando
inteligencia artificial 100% local (sin internet, sin nube). Te ayuda con:

- Registrar stock inicial por pasillo/estante (ej: Pasillo A: tornilleria)
- Definir stock minimo de alta rotacion (tornillos, discos 4 1/2, cemento, PVC)
- Calcular costo unitario y precio de venta
- Controlar entradas/salidas y alertas de agotado
- Hacer inventario fisico y reportes simples

Ejemplo: *"Tengo 200 tornillos de 1/4 y vendo 30 por semana, cual es mi stock minimo?"*

## 2. Caracteristicas de la computadora (Parte III)

### Minimo para aprobar en clase
- OS: Windows 10/11 64-bit
- CPU: i3 / Ryzen 3 o superior
- RAM: 8 GB (el modelo 3B usa ~2-3 GB + Windows + Python)
- Disco: 5 GB libres (Ollama ~2 GB + modelo qwen3.5:0.8b ~1 GB + Python)
- Pantalla: 1024x768 o superior (la app es fija 600x600)
- No requiere GPU ni internet para usar (solo para instalar)

### Recomendado ferreteria real
- RAM 12-16 GB para respuestas mas rapidas
- SSD para carga del modelo en <10 seg

## 3. Caracteristicas para el funcionamiento del proyecto

1. **Ollama instalado y corriendo.** Descargar de https://ollama.com/download
2. **Modelo <=3B descargado:**
   ```
   ollama pull qwen3.5:0.8b
   ollama list
   ```
   Alternativas validas (<=3B): `llama3.2:3b`, `tinyllama:1.1b`
3. **Python 3.10+ + dependencias:**
   ```
   pip install -r requirements.txt
   ```
4. **Archivos:** `main.py`, `assets/foto.jpg` (foto grupal)

Todo el proceso es local: tu consulta NUNCA sale a internet.

## 4. Como abrir el programa (Ejecutarlo)

### Opcion A - Doble clic / clase
1. Instala Ollama y ejecuta `ollama pull qwen3.5:0.8b` una sola vez.
2. Abre terminal en la carpeta del proyecto.
3. Ejecuta:
   ```
   python main.py
   ```
4. Se abre ventana 600x600 titulada "Asistente de Inventario - Ferreteria PYME".

### Opcion B - Verificar antes de exponer
```
ollama list        # debe aparecer qwen3.5:0.8b
python -m py_compile main.py
python main.py
```

## 5. Uso paso a paso

### Ventana principal (600x600)
- **Título:** nombre del asistente.
- **Área blanca central:** preguntas y respuestas.
- **Consulta:** campo de texto + botón verde **Enviar consulta**.
- **Botonera:** **Guardar en .txt** + **Ver integrantes**.

### Enviar consulta
1. Escribe en el campo de consulta, por ejemplo: *"Como ordeno mi bodega por pasillos?"*
2. Presiona **Enviar consulta**.
3. Abajo aparece "Consultando a Ollama..." mientras el modelo responde.
4. La respuesta aparece como "Respuesta:" debajo de la pregunta.

Buenas preguntas ferreteras para la demo:
- "Ficha para registrar un martillo Stanley en inventario, dame formato"
- "Vendo 2 quintales de cemento por semana, cuanto stock de seguridad dejo?"
- "Como hago inventario fisico sin cerrar todo el dia?"

### Guardar en .txt
1. Presiona **Guardar en .txt**.
2. Se crea `consulta_FECHA.txt` en la carpeta del programa.
3. El .txt incluye todas las preguntas y respuestas.
4. Ideal como evidencia para el docente.

### Ver integrantes
1. Presiona **Ver integrantes**.
2. Se abre ventana 400x450 con foto grupal (`assets/foto.jpg`) + nombres.
3. Si aparece "(Falta la foto en assets/foto.jpg)", falta colocar la foto.

## 6. Colores (justificación)
- Fondo verde claro `#E8F0E8` y título verde oscuro: orden y control.
- Botón Enviar verde `#2E7D5B`: acción principal visible.

## 7. Problemas comunes

| Sintoma | Causa | Solucion |
|---|---|---|
| "Error de Ollama" | Ollama no instalado / modelo no descargado | Instala Ollama, `ollama pull qwen3.5:0.8b`, reintenta |
| Ventana no abre / error `ollama` | Falta `pip install -r requirements.txt` | Ejecuta pip install |
| Foto no aparece | No existe `assets/foto.jpg` | Coloca la foto como assets/foto.jpg |
| Respuesta lenta (>30 seg) | PC 8GB + primer carga | Normal primera vez, luego acelera. Cierra Chrome/Excel |
| Estado "Consultando..." | El modelo está pensando | Espere unos segundos |

## 8. Privacidad

100% offline. Inventario, precios y proveedores quedan en tu PC. El .txt solo se crea si presionas Guardar.
