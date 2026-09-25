"""Asistente de inventario inteligente para pequeñas empresas, con Ollama local."""

from datetime import datetime
from pathlib import Path
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import ollama

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


MODELO = "qwen3.5:0.8b"
CONTEXTO = (
    "Eres un asistente de inventario para pequeñas empresas (PYMES) de El Salvador. "
    "Ayudas con existencias, productos con bajo stock, compras, proveedores, ventas "
    "y fechas de vencimiento. Responde en español, de forma breve y práctica. "
    "Este es el inventario actual de la empresa: "
    "Arroz 1 lb: 45 unidades (mínimo 20). "
    "Frijol rojo 1 lb: 8 unidades (mínimo 15). "
    "Aceite 1 L: 30 unidades (mínimo 10). "
    "Azúcar 5 lb: 12 unidades (mínimo 10). "
    "Leche en polvo 400 g: 5 unidades (mínimo 8, vence en 20 días). "
    "Café molido 250 g: 25 unidades (mínimo 10)."
)

# Carpeta del programa: junto al .exe si está compilado, o junto a main.py
CARPETA = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
FONT_FAMILY = "Segoe UI"
FONT_TITLE_SIZE = 18
FONT_BODY_SIZE = 10
FONT_SMALL_SIZE = 9
COLORS = {
    "background": "#F4F7F9",
    "surface": "#FFFFFF",
    "primary": "#1F6F78",
    "primary_dark": "#15515A",
    "accent": "#E49B4D",
    "text": "#23343B",
    "muted": "#6B7C83",
    "border": "#D5E0E4",
    "assistant_bubble": "#E7F2F3",
}


class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Asistente de Inventario PYME")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.conversacion = []
        self.imagen_referencia = None
        self.construir_estilos()
        self.construir_interfaz()

    def construir_estilos(self):
        self.estilos = ttk.Style()
        self.estilos.theme_use("clam")
        self.estilos.configure(
            "Primary.TButton",
            background=COLORS["primary"],
            foreground="white",
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"),
            padding=(12, 7),
        )
        self.estilos.map(
            "Primary.TButton",
            background=[("active", COLORS["primary_dark"])],
        )
        self.estilos.configure(
            "Secondary.TButton",
            background=COLORS["surface"],
            foreground=COLORS["primary_dark"],
            font=(FONT_FAMILY, FONT_SMALL_SIZE),
            padding=(8, 6),
        )
        self.estilos.configure(
            "TEntry",
            fieldbackground=COLORS["surface"],
            foreground=COLORS["text"],
            padding=7,
        )

    def construir_interfaz(self):
        self.root.configure(bg=COLORS["background"])

        encabezado = tk.Frame(self.root, bg=COLORS["primary"], height=88)
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)
        tk.Label(
            encabezado,
            text="Asistente de Inventario",
            bg=COLORS["primary"],
            fg="white",
            font=(FONT_FAMILY, FONT_TITLE_SIZE, "bold"),
        ).pack(anchor="w", padx=24, pady=(16, 0))
        tk.Label(
            encabezado,
            text="Control claro para las decisiones diarias de tu negocio",
            bg=COLORS["primary"],
            fg="#D8EFF0",
            font=(FONT_FAMILY, FONT_SMALL_SIZE),
        ).pack(anchor="w", padx=25, pady=(2, 0))

        contenido = tk.Frame(self.root, bg=COLORS["background"])
        contenido.pack(fill="both", expand=True, padx=20, pady=16)

        tk.Label(
            contenido,
            text="Conversacion",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"),
        ).pack(anchor="w")

        historial_marco = tk.Frame(
            contenido,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
        )
        historial_marco.pack(fill="both", expand=True, pady=(6, 12))
        self.historial = tk.Text(
            historial_marco,
            wrap="word",
            state="disabled",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            relief="flat",
            borderwidth=0,
            padx=12,
            pady=10,
            font=(FONT_FAMILY, FONT_BODY_SIZE),
            height=10,
        )
        scrollbar = ttk.Scrollbar(historial_marco, command=self.historial.yview)
        self.historial.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.historial.pack(side="left", fill="both", expand=True)
        self.historial.tag_configure("usuario", foreground=COLORS["primary_dark"], font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"))
        self.historial.tag_configure("asistente", foreground=COLORS["text"])
        self.agregar_mensaje("Asistente", "Hola. Puedo ayudarte a revisar existencias, productos con bajo stock y pedidos pendientes.", "asistente")

        tk.Label(
            contenido,
            text="Escribe una consulta sobre tu inventario",
            bg=COLORS["background"],
            fg=COLORS["muted"],
            font=(FONT_FAMILY, FONT_SMALL_SIZE),
        ).pack(anchor="w")
        entrada_marco = tk.Frame(contenido, bg=COLORS["background"])
        entrada_marco.pack(fill="x", pady=(5, 10))
        self.entrada = ttk.Entry(entrada_marco)
        self.entrada.pack(side="left", fill="x", expand=True)
        self.entrada.bind("<Return>", lambda _event: self.enviar_consulta())
        self.boton_enviar = ttk.Button(
            entrada_marco,
            text="Enviar",
            style="Primary.TButton",
            command=self.enviar_consulta,
        )
        self.boton_enviar.pack(side="left", padx=(8, 0))

        acciones = tk.Frame(contenido, bg=COLORS["background"])
        acciones.pack(fill="x")
        ttk.Button(
            acciones,
            text="Guardar consultas en documento.txt",
            style="Secondary.TButton",
            command=self.guardar_conversacion,
        ).pack(side="left")
        ttk.Button(
            acciones,
            text="Mostrar integrantes del grupo",
            style="Secondary.TButton",
            command=self.mostrar_integrantes,
        ).pack(side="right")

    def agregar_mensaje(self, autor, mensaje, etiqueta):
        self.historial.configure(state="normal")
        self.historial.insert("end", f"{autor}: ", etiqueta)
        self.historial.insert("end", f"{mensaje}\n\n")
        self.historial.configure(state="disabled")
        self.historial.see("end")
        self.conversacion.append((autor, mensaje))

    def obtener_respuesta(self, consulta):
        try:
            respuesta = ollama.chat(
                model=MODELO,
                think=False,  # sin razonamiento previo: responde mucho más rápido
                messages=[
                    {"role": "system", "content": CONTEXTO},
                    {"role": "user", "content": consulta},
                ],
            )
            return respuesta["message"]["content"]
        except Exception as error:
            return (
                "No se pudo consultar a Ollama. Verifique que Ollama esté abierto "
                f"y que el modelo esté descargado (ollama pull {MODELO}). "
                f"Detalle: {error}"
            )

    def enviar_consulta(self):
        consulta = self.entrada.get().strip()
        if not consulta:
            messagebox.showwarning("Consulta vacia", "Escribe una pregunta antes de enviar.")
            return
        self.agregar_mensaje("Tu", consulta, "usuario")
        self.entrada.delete(0, "end")
        self.boton_enviar.config(state="disabled", text="Pensando...")
        # La consulta corre en otro hilo para que la ventana no se congele
        threading.Thread(target=self.consultar_en_segundo_plano, args=(consulta,), daemon=True).start()

    def consultar_en_segundo_plano(self, consulta):
        respuesta = self.obtener_respuesta(consulta)
        # Tkinter solo se modifica desde el hilo principal
        self.root.after(0, self.mostrar_respuesta, respuesta)

    def mostrar_respuesta(self, respuesta):
        self.agregar_mensaje("Asistente", respuesta, "asistente")
        self.boton_enviar.config(state="normal", text="Enviar")

    def guardar_conversacion(self):
        if not self.conversacion:
            messagebox.showwarning("Sin conversacion", "Todavia no hay contenido para guardar.")
            return
        ruta = filedialog.asksaveasfilename(
            title="Guardar conversacion",
            initialfile="documento.txt",
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt")],
        )
        if not ruta:
            return
        with Path(ruta).open("w", encoding="utf-8") as archivo:
            archivo.write("Asistente de Inventario PYME\n")
            archivo.write(f"Fecha: {datetime.now():%Y-%m-%d %H:%M}\n\n")
            for autor, mensaje in self.conversacion:
                archivo.write(f"{autor}: {mensaje}\n\n")
        messagebox.showinfo("Conversacion guardada", "La respuesta y la conversacion se guardaron correctamente.")

    def mostrar_integrantes(self):
        if Image is None or ImageTk is None:
            messagebox.showerror(
                "Falta Pillow",
                "Para mostrar fotografias JPEG instala Pillow con: pip install Pillow",
            )
            return
        directorio_fotos = CARPETA / "foto integrantes"
        fotos = list(directorio_fotos.glob("*.jp*g")) + list(directorio_fotos.glob("*.png"))
        
        if not fotos:
            messagebox.showerror(
                "Imagen no encontrada",
                "No se encontró ninguna imagen en la carpeta 'foto integrantes'."
            )
            return
            
        ruta = str(fotos[0])
        ventana_foto = tk.Toplevel(self.root)
        ventana_foto.title("Integrantes del grupo")
        ventana_foto.geometry("520x600")
        ventana_foto.configure(bg=COLORS["background"])
        try:
            imagen = Image.open(ruta)
            imagen.thumbnail((480, 430))
            self.imagen_referencia = ImageTk.PhotoImage(imagen)
            tk.Label(ventana_foto, image=self.imagen_referencia, bg=COLORS["background"]).pack(pady=10)
            tk.Label(
                ventana_foto,
                text="Integrantes del Grupo:",
                bg=COLORS["background"],
                fg=COLORS["text"],
                font=(FONT_FAMILY, 14, "bold"),
            ).pack()
            tk.Label(
                ventana_foto,
                text="Andrea Saraí Durán Chamul - DC100223\nJosé Rodolfo Vargas Blanco - VB100222\nOmar Esaú Fuentes Gonzalez - FG100222\nFabio Alejandro Ordoñez Cerritos - OC100122",
                bg=COLORS["background"],
                fg=COLORS["text"],
                font=(FONT_FAMILY, 12),
            ).pack()
        except Exception as error:
            ventana_foto.destroy()
            messagebox.showerror("No se pudo abrir la imagen", f"El archivo no pudo cargarse: {error}")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = InventarioApp(ventana)
    ventana.mainloop()
