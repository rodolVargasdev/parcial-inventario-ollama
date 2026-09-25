import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import ollama

MODELO = "qwen3.5:0.8b"

INTEGRANTES = [
    "Omar Esaú Fuentes Gonzalez - FG100222",
    "Andrea Saraí Durán Chamul - DC100223",
    "Fabio Alejandro Ordoñez Cerritos - OC100122",
    "José Rodolfo Vargas Blanco - VB100222",
]

# Contexto que se le da al modelo para que responda como asistente de inventario
CONTEXTO = (
    "Eres un asistente de inventario para una ferretería PYME de El Salvador. "
    "Ayudas con stock, stock mínimo, entradas y salidas, precios, costos y proveedores. "
    "Responde en español, de forma breve y con ejemplos sencillos."
)

CARPETA = os.path.dirname(os.path.abspath(__file__))


def enviar():
    pregunta = entry_pregunta.get().strip()

    # Validación: campo vacío
    if not pregunta:
        messagebox.showerror("Error", "Por favor, escribe una consulta.")
        return

    label_estado.config(text="Consultando a Ollama (" + MODELO + ")...", fg="blue")
    root.update()  # Actualizar UI

    try:
        response = ollama.chat(
            model=MODELO,
            messages=[
                {"role": "system", "content": CONTEXTO},
                {"role": "user", "content": pregunta},
            ]
        )
        respuesta = response["message"]["content"]

        texto_respuesta.insert(tk.END, "Pregunta: " + pregunta + "\n")
        texto_respuesta.insert(tk.END, "Respuesta: " + respuesta + "\n\n")
        texto_respuesta.see(tk.END)
        entry_pregunta.delete(0, tk.END)
        label_estado.config(text="Consulta finalizada.", fg="green")
    except Exception as e:
        messagebox.showerror("Error de Ollama", f"Ocurrió un error al consultar el modelo:\n{e}")
        label_estado.config(text="Error en la consulta.", fg="red")


def guardar():
    contenido = texto_respuesta.get("1.0", tk.END).strip()

    if not contenido:
        messagebox.showerror("Error", "No hay ninguna consulta para guardar.")
        return

    nombre = "consulta_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
    ruta = os.path.join(CARPETA, nombre)
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)

    messagebox.showinfo("Guardado", "Consulta guardada en:\n" + ruta)


def ver_integrantes():
    ventana = tk.Toplevel(root)
    ventana.title("Integrantes del proyecto")
    ventana.geometry("400x450")

    tk.Label(ventana, text="Integrantes", font=("Arial", 12, "bold")).pack(pady=10)

    # Foto del grupo (assets/foto.jpg)
    ruta_foto = os.path.join(CARPETA, "assets", "foto.jpg")
    if os.path.exists(ruta_foto):
        from PIL import Image, ImageTk
        imagen = Image.open(ruta_foto)
        imagen.thumbnail((300, 220))
        ventana.foto = ImageTk.PhotoImage(imagen)  # se guarda para que no se borre
        tk.Label(ventana, image=ventana.foto).pack(pady=5)
    else:
        tk.Label(ventana, text="(Falta la foto en assets/foto.jpg)").pack(pady=5)

    for nombre in INTEGRANTES:
        tk.Label(ventana, text=nombre, font=("Arial", 10)).pack()


# Configuración de la ventana principal
root = tk.Tk()
root.title("Asistente de Inventario con Ollama")
root.geometry("600x600")
root.resizable(False, False)
root.config(bg="#E8F0E8")

# Título
tk.Label(root, text="Asistente de Inventario para PYMES", font=("Arial", 14, "bold"),
         bg="#E8F0E8", fg="#1F4E3D").pack(pady=10)

# Input para la consulta
tk.Label(root, text="Escribe tu consulta:", bg="#E8F0E8").pack()
entry_pregunta = tk.Entry(root, width=70)
entry_pregunta.pack(pady=5)

# Botón enviar
tk.Button(root, text="Enviar consulta", command=enviar, font=("Arial", 10, "bold"),
          bg="#2E7D5B", fg="white").pack(pady=5)

# Área de respuestas
texto_respuesta = tk.Text(root, width=70, height=20, wrap="word")
texto_respuesta.pack(pady=5)

# Botones de guardar e integrantes
frame_botones = tk.Frame(root, bg="#E8F0E8")
frame_botones.pack(pady=5)
tk.Button(frame_botones, text="Guardar en .txt", command=guardar).grid(row=0, column=0, padx=10)
tk.Button(frame_botones, text="Ver integrantes", command=ver_integrantes).grid(row=0, column=1, padx=10)

# Etiqueta de estado
label_estado = tk.Label(root, text="Esperando consulta...", bg="#E8F0E8")
label_estado.pack(pady=5)

root.mainloop()
