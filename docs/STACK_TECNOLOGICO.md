# Stack tecnológico

| Dependencia | Versión | Para qué | Alternativa descartada |
|---|---|---|---|
| Python | 3.10+ | Lenguaje, incluye Tkinter para la interfaz | PyQt (licencia y peso) |
| ollama (cliente Python) | 0.6.2 | Hablar con el servidor Ollama local | requests directo a la API REST |
| pillow | 12.3.0 | Mostrar la foto JPG/PNG de integrantes | Solo PNG con tk.PhotoImage |
| Ollama (servidor) | última estable | Ejecutar el modelo en local | LM Studio |
| qwen3.5:0.8b | 0.8B parámetros | Modelo destilado local (regla de 3B o menos) | llama3.2:3b, tinyllama |

La auditoría de vulnerabilidades corre en CI con `pip-audit` (ver `.github/workflows/audit.yml`).
