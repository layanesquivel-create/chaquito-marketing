import json
import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_CAMPAÑA = BASE_DIR / "contenido" / "posts" / "campana_activa.json"
RUTA_PROMPTS = BASE_DIR / "assets" / "prompts"

RUTA_PROMPTS.mkdir(parents=True, exist_ok=True)

IMAGEN_BASE = """Fotografía macro gastronómica profesional de {plato} en {restaurante}. \
Iluminación cálida de brasas de carbón, contraluz suave, texturas detalladas: \
grasa fundida, jugos cristalinos, crosta dorada, humo ligero en suspensión. \
Estilo realista, 8K, f/2.8, lente 100mm macro, fondo oscuro madera rústica, \
partículas de sal y pimienta, gotas de jugo congeladas en slow motion virtual, \
sin personas, solo comida y parrilla."""

VIDEO_BASE = """Video vertical 9:16 cinemático de {plato} en {restaurante}. \
Cámara lenta 120fps: corte de carne con cuchillo, jugosidad extrema saliendo, \
humo ascendiendo en hilos translúcidos, brasas iluminando bordes, texturas close-up, \
música ambiente parrilla leve, transición humo a plato servido, \
4K vertical, color grading cálido, focus pulling suave."""


def cargar_campaña():
    with open(RUTA_CAMPAÑA, "r", encoding="utf-8") as f:
        return json.load(f)


def extraer_platillos(datos):
    platillos = set()
    for pub in datos.get("publicaciones", []):
        asset = pub.get("asset_sugerido", "")
        if asset:
            nombre = Path(asset).stem
            platillos.add(nombre)
    return sorted(platillos)


def generar_prompts(datos):
    nombre_rest = datos.get("restaurante", "El Chaquito de Felipe")
    platillos = extraer_platillos(datos)
    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")

    prompts = {"imagenes": [], "videos": []}

    for platillo in platillos:
        prompts["imagenes"].append({
            "platillo": platillo,
            "prompt": IMAGEN_BASE.format(plato=platillo, restaurante=nombre_rest),
        })
        prompts["videos"].append({
            "platillo": platillo,
            "prompt": VIDEO_BASE.format(plato=platillo, restaurante=nombre_rest),
        })

    ruta_img = RUTA_PROMPTS / f"prompts_imagenes_{marca_tiempo}.json"
    ruta_vid = RUTA_PROMPTS / f"prompts_videos_{marca_tiempo}.json"
    ruta_all = RUTA_PROMPTS / f"prompts_ia_{marca_tiempo}.json"

    with open(ruta_img, "w", encoding="utf-8") as f:
        json.dump(prompts["imagenes"], f, ensure_ascii=False, indent=2)

    with open(ruta_vid, "w", encoding="utf-8") as f:
        json.dump(prompts["videos"], f, ensure_ascii=False, indent=2)

    with open(ruta_all, "w", encoding="utf-8") as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)

    print(f"[OK] Prompts de imagen: {ruta_img}")
    print(f"[OK] Prompts de video: {ruta_vid}")
    print(f"[OK] Prompts combinados: {ruta_all}")
    return prompts


def main():
    print("[+] Leyendo campaña activa...")
    datos = cargar_campaña()
    print(f"[+] Restaurante: {datos.get('restaurante')}")
    print(f"[+] Campaña: {datos.get('campana')}")
    generar_prompts(datos)
    print("\n=== GENERACIÓN DE PROMPTS COMPLETADA ===")


if __name__ == "__main__":
    main()
