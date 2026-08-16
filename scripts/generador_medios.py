import os
import json
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_PROMPTS = BASE_DIR / "assets" / "prompts"
RUTA_IMAGENES = BASE_DIR / "assets" / "imagenes"
RUTA_VIDEOS = BASE_DIR / "assets" / "videos"

RUTA_IMAGENES.mkdir(parents=True, exist_ok=True)
RUTA_VIDEOS.mkdir(parents=True, exist_ok=True)


class BaseGenerator(ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    @abstractmethod
    def generar_imagen(self, prompt: str, salida: Path):
        pass

    @abstractmethod
    def generar_video(self, prompt: str, salida: Path, duracion: int = 4, ratio: str = "9:16"):
        pass


class OpenAIImageGenerator(BaseGenerator):
    ENDPOINT = "https://api.openai.com/v1/images/generations"

    def generar_imagen(self, prompt: str, salida: Path, tamano: str = "1024x1024"):
        print(f"[+] Generando imagen: {salida.name}")
        payload = {"model": "dall-e-3", "prompt": prompt, "n": 1, "size": tamano}
        r = requests.post(
            self.ENDPOINT,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=180,
        )
        r.raise_for_status()
        data = r.json()
        url = data["data"][0]["url"]
        img = requests.get(url, timeout=180)
        img.raise_for_status()
        salida.write_bytes(img.content)
        print(f"[OK] Imagen guardada: {salida}")

    def generar_video(self, prompt: str, salida: Path, duracion: int = 4, ratio: str = "9:16"):
        raise NotImplementedError("OpenAI DALL-E no genera videos en esta integración.")


class PikaVideoGenerator(BaseGenerator):
    ENDPOINT = "https://api.pika.art/v1/videos"

    def generar_imagen(self, prompt: str, salida: Path):
        raise NotImplementedError("Pika se usa para video en esta integración.")

    def generar_video(self, prompt: str, salida: Path, duracion: int = 4, ratio: str = "9:16"):
        print(f"[+] Generando video: {salida.name}")
        payload = {"prompt": prompt, "seconds": duracion, "aspect_ratio": ratio}
        r = requests.post(
            self.ENDPOINT,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=180,
        )
        r.raise_for_status()
        data = r.json()
        url = data.get("video_url") or data.get("url")
        if not url:
            raise RuntimeError(f"No se obtuvo URL de video: {data}")
        vid = requests.get(url, timeout=180)
        vid.raise_for_status()
        salida.write_bytes(vid.content)
        print(f"[OK] Video guardado: {salida}")


class StabilityImageGenerator(BaseGenerator):
    ENDPOINT = "https://api.stability.ai/v2beta/stable-image/generate/core"

    def generar_imagen(self, prompt: str, salida: Path, tamano: str = "1024x1024"):
        print(f"[+] Generando imagen: {salida.name}")
        width, height = tamano.split("x")
        r = requests.post(
            self.ENDPOINT,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"prompt": prompt, "output_format": "png", "width": int(width), "height": int(height)},
            timeout=180,
        )
        r.raise_for_status()
        salida.write_bytes(r.content)
        print(f"[OK] Imagen guardada: {salida}")

    def generar_video(self, prompt: str, salida: Path, duracion: int = 4, ratio: str = "9:16"):
        raise NotImplementedError("Stability no genera videos en esta integración.")


def cargar_prompts_recientes():
    candidatos = sorted(RUTA_PROMPTS.glob("prompts_ia_*.json"))
    if not candidatos:
        raise FileNotFoundError("No se encontraron prompts en assets/prompts/. Ejecuta primero generador_prompts_ia.py.")
    ruta = candidatos[-1]
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f), ruta


def resolver_generador(provider: str, api_key: str) -> BaseGenerator:
    provider = provider.lower()
    if provider == "openai":
        return OpenAIImageGenerator(api_key=api_key)
    if provider == "stability":
        return StabilityImageGenerator(api_key=api_key)
    if provider == "pika":
        return PikaVideoGenerator(api_key=api_key)
    raise ValueError(f"Proveedor no soportado: {provider}")


def main():
    print("=== GENERADOR DE MEDIOS CHAQUITO ===")

    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("STABILITY_API_KEY") or os.getenv("PIKA_API_KEY")
    if not api_key:
        raise EnvironmentError("Falta OPENAI_API_KEY / STABILITY_API_KEY / PIKA_API_KEY en .env")

    provider = os.getenv("MEDIA_PROVIDER", "openai")
    generador = resolver_generador(provider, api_key)
    print(f"[+] Proveedor activo: {provider}")

    prompts, ruta = cargar_prompts_recientes()
    print(f"[+] Usando prompts: {ruta.name}")

    marca = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("\n[+] Generando imágenes...")
    for item in prompts.get("imagenes", []):
        platillo = item["platillo"]
        prompt = item["prompt"]
        salida = RUTA_IMAGENES / f"{platillo}_{marca}.png"
        generador.generar_imagen(prompt=prompt, salida=salida)

    print("\n[+] Generando videos...")
    for item in prompts.get("videos", []):
        platillo = item["platillo"]
        prompt = item["prompt"]
        salida = RUTA_VIDEOS / f"{platillo}_{marca}.mp4"
        generador.generar_video(prompt=prompt, salida=salida)

    print("\n=== GENERACIÓN DE MEDIOS COMPLETADA ===")


if __name__ == "__main__":
    main()
