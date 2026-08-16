}# Chaquito Marketing Automation Pipeline

Sistema automatizado de generación de contenido, validación de menús y optimización de assets para **El Chaquito de Felipe**.

## Estructura del Proyecto

- `main.py`: Orquestador principal que ejecuta todo el flujo.
- `scripts/validar_menu.py`: Validación de integridad de copys y menús en formato JSON.
- `scripts/optimizar_imagenes.py`: Conversión y compresión masiva de imágenes a formato WebP.
- `scripts/generador_contenido.py`: Generador de copys y estructuras de publicaciones.
- `scripts/exportar_csv.py`: Exportador a formato CSV compatible con Meta Business Suite.
- `contenido/posts/`: Directorio donde residen los JSON generados y CSVs de programación.
- `assets/imagenes/`: Directorio de entrada para material visual en alta resolución.
- `assets/optimizadas/`: Directorio de salida con assets listos para redes sociales.

## Requisitos y Configuración

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt