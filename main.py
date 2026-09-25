"""
Asistente de Inventario Inteligente para Ferreterias PYME - UFG
Parte I (35%): Software con Ollama local <=3B parametros.

Requisitos cumplidos:
1. Ventana grafica 600x600 fija
2. Colores enfoque inventario/business PYME (azul + verde + gris)
3. Boton Enviar consulta -> Ollama local
4. Boton Guardar consulta en .txt
5. Boton Integrantes -> nueva ventana con foto + nombres

Modelo recomendado (<=3B): qwen2.5:3b / llama3.2:3b / tinyllama
Instalacion previa:
  1. Instalar Ollama desde https://ollama.com/download
  2. ollama pull qwen2.5:3b
  3. pip install -r requirements.txt
  4. python main.py
"""

import os
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from datetime import datetime

# --- Configuracion ---
VENTANA_W, VENTANA_H = 600, 600
MODEL_NAME = "qwen2.5:3b"  # <=3B, 100% local. Alternativas: "llama3.2:3b", "tinyllama"

SYSTEM_PROMPT = (
    "Eres un Asistente de Inventario Inteligente para FERRETERIAS PYME de El Salvador. "
    "Respondes en espanol, breve y practico. "
    "Ayudas con: tornilleria, herramientas electricas y manuales, pinturas, "
    "cemento, PVC, fontaneria, electricidad, stock por pasillo/estante, "
    "stock minimo de alta rotacion, costos, precios, proveedores, "
    "entradas/salidas, alertas de agotado, inventarios fisicos y reportes simples. "
    "Da ejemplos con productos reales de ferreteria (ej: tornillo 1/4, disco 4 1/2, cemento CESSA). "
    "Si te preguntan algo fuera de inventario ferretero, redirige amablemente al tema. "
    "Usa listas y ejemplos con numeros cuando sea util."
)

# EDITAR: nombres reales del equipo
INTEGRANTES = [
    "Integrante 1 - Nombre Apellido",
    "Integrante 2 - Nombre Apellido",
    "Integrante 3 - Nombre Apellido",
    "Integrante 4 - Nombre Apellido",
]

# Paleta enfoque ferreteria PYME (acero + naranja herramienta + carton)
C_AZUL = "#3D405B"      # header, acero oscuro profesional
C_VERDE = "#E07A2C"     # enviar / naranja ferretero
C_FONDO = "#F2EFE9"     # fondo general, tono caja/carton claro
C_CHAT = "#FFFFFF"      # area chat
C_GRIS_BTN = "#6C757D"  # botones secundarios, gris herramienta
C_TEXTO = "#2B2D42"

try:
    import ollama
    OLLAMA_LIB_OK = True
except ImportError:
    OLLAMA_LIB_OK = False


def consultar_ollama(historial):
    """Llama a Ollama local. historial = lista de dicts {role, content}."""
    resp = ollama.chat(model=MODEL_NAME, messages=historial)
    return resp["message"]["content"]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Asistente de Inventario - Ferreteria PYME")
        self.geometry(f"{VENTANA_W}x{VENTANA_H}")
        self.resizable(False, False)
        self.configure(bg=C_FONDO)

        self.historial = [{"role": "system", "content": SYSTEM_PROMPT}]

        self._build_ui()
        self._mensaje_bot(
            "Hola! Soy tu Asistente de Inventario para Ferreterias.\n"
            "Pregúntame, por ejemplo: 'tengo 200 tornillos 1/4, cual es mi stock minimo?', "
            "'como ordeno mi bodega por pasillos?', 'cemento vs chispa: como controlo caducidad?'."
        )

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=C_AZUL, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="FERRETERIA - CONTROL DE INVENTARIO",
                 bg=C_AZUL, fg="white",
                 font=("Segoe UI", 13, "bold")).pack(pady=(10, 0))
        tk.Label(header, text=f"Modelo local: {MODEL_NAME}  |  100% offline con Ollama",
                 bg=C_AZUL, fg="#FFE8D6",
                 font=("Segoe UI", 8)).pack()

        # Chat
        self.chat = scrolledtext.ScrolledText(
            self, bg=C_CHAT, fg=C_TEXTO, font=("Segoe UI", 10),
            wrap="word", state="disabled", relief="flat", padx=10, pady=10,
            height=20)
        self.chat.pack(padx=12, pady=10, fill="both", expand=True)

        # Entrada
        entry_frame = tk.Frame(self, bg=C_FONDO)
        entry_frame.pack(fill="x", padx=12)
        self.entrada = tk.Entry(entry_frame, font=("Segoe UI", 10),
                                relief="solid", bd=1)
        self.entrada.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        self.entrada.bind("<Return>", lambda e: self.enviar())

        self.btn_enviar = tk.Button(entry_frame, text="Enviar", bg=C_VERDE,
                                    fg="white", font=("Segoe UI", 10, "bold"),
                                    relief="flat", padx=18, pady=6,
                                    command=self.enviar)
        self.btn_enviar.pack(side="right")

        # Botonera inferior
        btns = tk.Frame(self, bg=C_FONDO)
        btns.pack(fill="x", padx=12, pady=10)
        tk.Button(btns, text="Guardar consulta (.txt)", bg=C_GRIS_BTN, fg="white",
                  font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=7,
                  command=self.guardar).pack(side="left", expand=True, fill="x", padx=(0, 6))
        tk.Button(btns, text="Integrantes", bg=C_AZUL, fg="white",
                  font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=7,
                  command=self.ventana_integrantes).pack(side="right", expand=True, fill="x", padx=(6, 0))

    def _append(self, quien, texto):
        self.chat.configure(state="normal")
        self.chat.insert("end", f"{quien}: {texto}\n\n")
        self.chat.configure(state="disabled")
        self.chat.see("end")

    def _mensaje_bot(self, texto):
        self._append("Asistente", texto)

    def enviar(self):
        pregunta = self.entrada.get().strip()
        if not pregunta:
            return
        self.entrada.delete(0, "end")
        self._append("Tu", pregunta)
        self.btn_enviar.configure(state="disabled", text="...")
        threading.Thread(target=self._responder, args=(pregunta,), daemon=True).start()

    def _responder(self, pregunta):
        self.historial.append({"role": "user", "content": pregunta})
        try:
            if not OLLAMA_LIB_OK:
                respuesta = ("ERROR: falta la libreria 'ollama'.\n"
                             "Ejecuta: pip install -r requirements.txt")
            else:
                respuesta = consultar_ollama(self.historial)
            self.historial.append({"role": "assistant", "content": respuesta})
        except Exception as e:
            respuesta = (f"No pude conectar con Ollama.\n"
                         f"1. Instala Ollama: https://ollama.com/download\n"
                         f"2. Ejecuta: ollama pull {MODEL_NAME}\n"
                         f"3. Verifica: ollama list\n\nDetalle: {e}")
        self.after(0, self._mostrar_respuesta, respuesta)

    def _mostrar_respuesta(self, respuesta):
        self._mensaje_bot(respuesta)
        self.btn_enviar.configure(state="normal", text="Enviar")

    def guardar(self):
        contenido = self.chat.get("1.0", "end").strip()
        if not contenido:
            messagebox.showinfo("Guardar", "No hay consulta para guardar.")
            return
        nombre = f"consulta_inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt", initialfile=nombre,
            filetypes=[("Texto", "*.txt")])
        if not ruta:
            return
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(f"Ferreteria PYME - Asistente de Inventario - {datetime.now()}\n")
            f.write(f"Modelo: {MODEL_NAME}\n{'='*50}\n\n{contenido}")
        messagebox.showinfo("Guardar", f"Guardado en:\n{ruta}")

    def ventana_integrantes(self):
        win = tk.Toplevel(self)
        win.title("Integrantes del proyecto")
        win.geometry("400x480")
        win.resizable(False, False)
        win.configure(bg="white")

        tk.Label(win, text="INTEGRANTES DEL PROYECTO", bg="white",
                 fg=C_AZUL, font=("Segoe UI", 12, "bold")).pack(pady=10)
        tk.Label(win, text="Asistente de Inventario - Ferreteria PYME",
                 bg="white", fg=C_GRIS_BTN, font=("Segoe UI", 9)).pack()

        # Foto: assets/foto.jpg o placeholder
        foto_path = None
        base = os.path.dirname(os.path.abspath(__file__))
        for cand in ["foto.jpg", "foto.png", "integrantes.jpg"]:
            cand = os.path.join(base, "assets", cand)
            if os.path.exists(cand):
                foto_path = cand
                break

        if foto_path:
            try:
                from PIL import Image, ImageTk
                img = Image.open(foto_path)
                img.thumbnail((320, 240))
                self._tkimg = ImageTk.PhotoImage(img)  # evitar GC
                tk.Label(win, image=self._tkimg, bg="white").pack(pady=8)
            except Exception as e:
                tk.Label(win, text=f"[No se pudo cargar foto: {e}]",
                         bg="white", fg="red").pack(pady=8)
        else:
            tk.Label(win, text="[ Coloca tu foto grupal en assets/foto.jpg ]",
                     bg=C_FONDO, fg=C_GRIS_BTN, font=("Segoe UI", 9, "italic"),
                     width=40, height=6, relief="solid", bd=1).pack(pady=8)

        for n in INTEGRANTES:
            tk.Label(win, text="- " + n, bg="white",
                     fg=C_TEXTO, font=("Segoe UI", 10)).pack(anchor="w", padx=40)


if __name__ == "__main__":
    App().mainloop()
