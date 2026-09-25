# Asistente de Inventario Inteligente para PYMES

Proyecto de la Universidad Francisco Gavidia, Problema 7. Se ejecuta 100% en local con Ollama y el modelo destilado qwen3.5:0.8b.

## Integrantes

- Omar Esaú Fuentes Gonzalez - FG100222
- Andrea Saraí Durán Chamul - DC100223
- Fabio Alejandro Ordoñez Cerritos - OC100122
- José Rodolfo Vargas Blanco - VB100222

## Ejecución rápida

```
ollama pull qwen3.5:0.8b
pip install -r requirements.txt
python main.py
```

## Funciones

1. Ventana de 600x600 con colores acordes a un asistente de inventario.
2. Botón Enviar: consulta al modelo local.
3. Botón Guardar consultas en documento.txt.
4. Botón Mostrar integrantes del grupo: ventana con la foto y los nombres.

## Estructura

```
main.py                        Programa
requirements.txt               Librerías (ollama, pillow)
foto integrantes/              Foto del grupo
docs/MANUAL_USUARIO.md         Manual de usuario
docs/MANUAL_DESARROLLADOR.md   Documentación para desarrolladores
docs/STACK_TECNOLOGICO.md      Dependencias y versiones
entrega/                       Los mismos documentos en Word
```
