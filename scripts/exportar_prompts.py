import json
import os
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_PROMPTS = BASE_DIR / "assets" / "prompts"
RUTA_LOTE = RUTA_PROMPTS / "lote_produccion.json"


def resolver_ultimo_archivo(nombre_base: str) -> Path:
    candidatos = sorted(RUTA_PROMPTS.glob(f"{nombre_base}_*.json"))
    if not candidatos:
        raise FileNotFoundError(f"No se encontraron archivos que coincidan con {nombre_base}_*.json")
    return candidatos[-1]


def compilar_lote() -> Path:
    imagenes_path = resolver_ultimo_archivo("prompts_imagenes")
    videos_path = resolver_ultimo_archivo("prompts_videos")

    with open(imagenes_path, "r", encoding="utf-8") as f:
        imagenes = json.load(f)

    with open(videos_path, "r", encoding="utf-8") as f:
        videos = json.load(f)

    lote = {
        "metadata": {
            "compilado_en": datetime.now().isoformat(),
            "imagenes_archivo": imagenes_path.name,
            "videos_archivo": videos_path.name,
        },
        "imagenes": imagenes,
        "videos": videos,
    }

    with open(RUTA_LOTE, "w", encoding="utf-8") as f:
        json.dump(lote, f, ensure_ascii=False, indent=2)

    print(f"[OK] Lote compilado: {RUTA_LOTE}")
    return RUTA_LOTE


def main():
    print("=== EXPORTAR PROMPTS A LOTE DE PRODUCCIÓN ===")
    ruta = compilar_lote()
    print(f"[+] Listo para generación por lotes: {ruta}")
    print("=== EXPORTACIÓN COMPLETADA ===")


if __name__ == "__main__":
    main()
