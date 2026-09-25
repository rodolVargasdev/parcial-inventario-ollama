# MANUAL DEL DESARROLLADOR - Asistente Inventario Ferreteria PYME
### Parte II-1: explicacion del codigo en general y detalles vitales

## 1. Vision general (30 segundos)

App monolitica Python + Tkinter + Ollama local.

```
Usuario (Tkinter 600x600) -> Thread -> ollama.chat(qwen2.5:3b) -> Respuesta en chat
                         -> Guardar .txt (filedialog)
                         -> Toplevel Integrantes (Pillow)
```

Sin backend, sin API cloud, sin base de datos. El "cerebro" es el modelo 3B
inyectado con un `SYSTEM_PROMPT` ferretero. Historial en memoria (`list[dict]`).

Ficheros:
- `main.py` (~230 lineas): todo (UI + logica + Ollama). Decision intencional para clase: un solo archivo = facil de explicar/defender.
- `requirements.txt`: `ollama>=0.4.0`, `pillow>=10.0.0`
- `assets/foto.jpg`: foto grupal, carga opcional con fallback.

## 2. Mapa del codigo (por bloques)

### 2.1 Configuracion (main.py:26-54)
- `VENTANA_W, VENTANA_H = 600, 600` -> restriccion de catedra. `resizable(False, False)` la hace cumplir.
- `MODEL_NAME = "qwen2.5:3b"` -> cumple regla <=3B. Cambiar aqui cambia todo el sistema. Alternativas: `llama3.2:3b`, `tinyllama`.
- `SYSTEM_PROMPT` -> EL CORAZON del enfoque ferretero. Sin esto el modelo 3B responde generico. Incluye: rol, inventario por pasillo, ejemplos reales (tornillo 1/4, disco 4 1/2, cemento CESSA), redireccion de temas.
- `INTEGRANTES` -> lista editable, se renderiza en ventana secundaria.
- Paleta `C_AZUL, C_VERDE...` -> justificacion en Manual Usuario seccion 6.

### 2.2 Capa Ollama (main.py:56-68)
```python
import ollama
ollama.chat(model=MODEL_NAME, messages=historial)
```
- `historial` formato OpenAI: `[{role: system|user|assistant, content}]`.
- Se envia HISTORIAL COMPLETO cada vez (memoria conversacional). Ojo vital: crece sin limite -> en PC 8GB con charlas >50 turnos puede alentarse. Mejora futura: truncar a ultimos 10.
- `OLLAMA_LIB_OK` flag para degradar con mensaje util si falta `pip install`.
- Toda excepcion (modelo no descargado, Ollama apagado) se captura y se traduce a 3 pasos accionables para el usuario. Detalle VITAL para la demo en clase.

### 2.3 UI Tkinter (main.py:71-129, clase App)
- `App(tk.Tk)`: ventana raiz 600x600.
- `_build_ui()`: header Frame 70px + ScrolledText (chat read-only `state=disabled`) + Entry + Boton Enviar + botonera inferior.
- `ScrolledText` se habilita solo para insertar (`state=normal`) y se vuelve a bloquear. Evita edicion accidental.
- `Entry.bind("<Return>")` -> Enter = Enviar (UX).
- `ventana_integrantes()`: `Toplevel` 400x480, busca `assets/foto.jpg|foto.png|integrantes.jpg`, `thumbnail((320,240))` con Pillow. Guarda referencia `self._tkimg` para evitar garbage collector (BUG CLASICO Tkinter: si no guardas referencia la imagen desaparece).
- Si no hay foto, placeholder con instrucciones. La app NUNCA crashea por falta de foto.

### 2.4 Concurrencia (main.py:140-167)
```python
threading.Thread(target=self._responder, daemon=True).start()
...
self.after(0, self._mostrar_respuesta, respuesta)
```
DETALLE VITAL a defender ante el docente:
- `ollama.chat` es bloqueante (5-30 seg en CPU). Sin thread, la UI 600x600 se congelaria.
- El thread hace la consulta, luego `after(0,...)` vuelve al hilo principal (Tkinter NO es thread-safe, solo el main thread toca widgets).
- `daemon=True` para que al cerrar la ventana no quede hilo colgado.
- Boton cambia a "..." y se deshabilita para evitar doble envio.

### 2.5 Persistencia (main.py:169-183)
- `filedialog.asksaveasfilename` + `open(..., encoding=utf-8)`.
- Incluye timestamp + modelo para trazabilidad academica.
- Sin dependencias externas.

## 3. Decisiones de arquitectura y tradeoffs

1. **Tkinter vs PyQt/CustomTkinter:** Tkinter viene en stdlib, cero friccion instalacion en lab UFG. Contra: feo por defecto, se compensa con paleta plana.
2. **Un solo archivo vs hexagonal:** Para 600x600 + 3 botones, separar en capas es over-engineering y complica la defensa. Se documenta para escalar a `src/ui, src/core` si crece.
3. **Modelo 3B vs 7B+:** Catedra exige <=3B y 100% local en laptops 8GB. qwen2.5:3b equilibra espanol + instrucciones. tinyllama es mas rapido pero peor espanol.
4. **Historial completo vs RAG:** No hay base vectorial; el dominio ferretero va en prompt. Suficiente para alcance clase. Evolucion: SQLite para Kardex real + RAG sobre catalogo.

## 4. Como extender (ideas para defender nota)

- Agregar `ComboBox` selector de modelo (`qwen2.5:3b`, `llama3.2:3b`) leyendo `ollama list`.
- Guardar Kardex en `sqlite3` (stdlib): tabla `movimientos(fecha, sku, tipo, cant)`.
- Limitar historial: `self.historial[-11:]` + system.
- Exportar a CSV ademas de .txt para Excel de la ferreteria.

## 5. Guia GitHub (subir todo)

```bash
cd parcial-inventario-ollama
git init -b main
git add main.py requirements.txt README.md .gitignore assets/ docs/
git commit -m "feat: asistente inventario ferreteria PYME con Ollama local 3B"
# crear repo vacio en github.com (ej: ferreteria-inventario-ufg) y luego:
git remote add origin https://github.com/TU_USUARIO/ferreteria-inventario-ufg.git
git push -u origin main
```

No subir: `__pycache__/`, `*.txt` generados (ya en `.gitignore`).
Foto: subir `assets/foto.jpg` (si pesa >10MB, comprimir).

## 6. Checklist defensa Parte II

- [ ] Mostrar `ollama list` con modelo <=3B.
- [ ] Abrir con `python main.py`, verificar 600x600.
- [ ] Pregunta ferretera en vivo + Guardar .txt + abrir ventana Integrantes.
- [ ] Explicar thread + `after()` y por que sin eso se congela.
- [ ] Explicar SYSTEM_PROMPT como especializacion sin reentrenar.
