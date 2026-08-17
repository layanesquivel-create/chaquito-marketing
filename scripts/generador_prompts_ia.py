import json
import hashlib
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

TEMPLATES_EXTRA = {
    "brasas": "Brasas encendidas en primer plano, partículas incandescentes ascendiendo.",
    "corte": "Corte transversal delgado en primer plano mostrando cocción interna jugosa.",
    "humo": "Humo volumétrico denso, contrapesado por luz cálida lateral.",
}


def cargar_campaña():
    with open(RUTA_CAMPAÑA, "r", encoding="utf-8") as f:
        return json.load(f)


def hash_prompt(texto: str) -> str:
    return hashlib.sha1(texto.encode("utf-8")).hexdigest()[:8]


def extraer_platillos(datos):
    platillos = set()
    for pub in datos.get("publicaciones", []):
        asset = pub.get("asset_sugerido", "")
        if asset:
            platillos.add(Path(asset).stem)
    return sorted(platillos)


def generar_prompts(datos):
    nombre_rest = datos.get("restaurante", "El Chaquito de Felipe")
    platillos = extraer_platillos(datos)
    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")

    prompts = {"imagenes": [], "videos": [], "metadata": {"restaurante": nombre_rest, "campaña": datos.get("campana"), "marca_tiempo": marca_tiempo, "total": len(platillos)}}

    for platillo in platillos:
        imagen = IMAGEN_BASE.format(plato=platillo, restaurante=nombre_rest)
        imagen += " " + TEMPLATES_EXTRA["brasas"] + " " + TEMPLATES_EXTRA["corte"] + " " + TEMPLATES_EXTRA["humo"]
        prompts["imagenes"].append({"platillo": platillo, "prompt": imagen, "hash": hash_prompt(imagen)})

        video = VIDEO_BASE.format(plato=platillo, restaurante=nombre_rest)
        video += " " + TEMPLATES_EXTRA["brasas"] + " " + TEMPLATES_EXTRA["corte"] + " " + TEMPLATES_EXTRA["humo"]
        prompts["videos"].append({"platillo": platillo, "prompt": video, "hash": hash_prompt(video)})

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
    return prompts, ruta_all


def main():
    print("[+] Leyendo campaña activa...")
    datos = cargar_campaña()
    print(f"[+] Restaurante: {datos.get('restaurante')}")
    print(f"[+] Campaña: {datos.get('campana')}")
    _, ruta = generar_prompts(datos)
    print(f"\n[OK] Lote base generado en: {ruta}")
    print("=== GENERACIÓN DE PROMPTS COMPLETADA ===")


if __name__ == "__main__":
    main()
