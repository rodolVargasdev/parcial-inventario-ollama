# Asistente de Inventario Inteligente para Ferreterias PYME

Proyecto UFG - 100% local con Ollama (modelo destilado <=3B parametros).

## Enfoque: Ferreterias

Asistente que ayuda al ferretero a controlar stock por pasillo/estante, alta rotacion
(tornilleria, discos, cemento, PVC, pinturas), stock minimo, costos, proveedores
y reportes simples. Todo offline, sin nube.

## Requisitos

- Windows 10/11, 8GB RAM minimo (recomendado 12GB+)
- Python 3.10+
- Ollama instalado: https://ollama.com/download
- Modelo local <=3B: `qwen2.5:3b` (recomendado) o `llama3.2:3b` / `tinyllama`

## Instalacion

```bash
ollama pull qwen2.5:3b
pip install -r requirements.txt
python main.py
```

## Estructura

```
main.py                  # App Tkinter 600x600 (Parte I)
requirements.txt         # ollama + pillow
assets/foto.jpg          # Foto grupal (poner aqui)
assets/LEEME.txt
docs/MANUAL_USUARIO.md       # Parte II-2 + Parte III
docs/MANUAL_DESARROLLADOR.md # Parte II-1
docs/STACK_TECNOLOGICO.md    # Dependencias
```

## Funciones (Parte I)

1. Ventana 600x600 fija, colores ferreteros (acero + naranja + carton).
2. Boton **Enviar**: consulta a Ollama local.
3. Boton **Guardar consulta (.txt)**: exporta conversacion.
4. Boton **Integrantes**: ventana nueva con foto + nombres.

## Equipo

Editar nombres en `main.py: INTEGRANTES` y poner foto en `assets/foto.jpg`.

## Documentacion completa

- Manual Usuario: `docs/MANUAL_USUARIO.md`
- Manual Desarrollador: `docs/MANUAL_DESARROLLADOR.md`
