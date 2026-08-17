import json
import random
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_PERFIL = BASE_DIR / "config" / "restaurante_perfil.json"
RUTA_SALIDA = BASE_DIR / "assets" / "prompts" / "pilares_creativos.json"


class EstrategaCreativo:
    PILARES = [
        "Comercial",
        "Curiosidades de la Parrilla",
        "Tips Parrilleros",
        "Tradición Criolla",
    ]

    PLANTILLAS = {
        "Comercial": {
            "copy": "🔥 Hoy en {restaurante} te recomendamos {plato}. A solo {precio}. Pedí ahora por WhatsApp y reservá tu mesa.",
            "hashtags": ["#Parrilla", "#Pedidos", "#{restaurante_slug}"],
            "cta": "Pedí por WhatsApp",
        },
        "Curiosidades de la Parrilla": {
            "copy": "¿Sabías por qué la carne en la parrilla desarrolla ese sabor único? En {restaurante} usamos carbón seleccionado y técnica artesanal para potenciar la reacción de Maillard sin quemar la fibra.",
            "hashtags": ["#CienciaAsado", "#Parrilla", "#{restaurante_slug}"],
            "cta": "Reservá y probalo",
        },
        "Tips Parrilleros": {
            "copy": "Tip parrillero: sellá la carne a fuego alto sin moverla los primeros 90 segundos. Así conservás los jugos y obtenés esa crosta dorada perfecta. En {restaurante} lo hacemos así en cada corte.",
            "hashtags": ["#TipsParrilla", "#Asado", "#{restaurante_slug}"],
            "cta": "Consultá nuestro menú",
        },
        "Tradición Criolla": {
            "copy": "20 años de tradición chapaca en cada mesa. En {restaurante} el asado no es solo comida, es el encuentro de la familia y la parrilla con alma paceña.",
            "hashtags": ["#Tradicion", "#CocinaBoliviana", "#{restaurante_slug}"],
            "cta": "Escribinos por WhatsApp",
        },
    }

    def __init__(self, perfil: dict):
        self.perfil = perfil
        self.menu = perfil.get("menu_principal", [])
        self.restaurante = perfil.get("nombre", "El Chaquito de Felipe")
        self.restaurante_slug = self.restaurante.replace(" ", "").replace("á", "a").replace("é", "e")

    def plato_aleatorio(self):
        items = []
        for categoria in self.menu:
            for item in categoria.get("items", []):
                items.append(item)
        return random.choice(items) if items else {"nombre": "nuestro menú", "precio": "precio de temporada"}

    def generar_post(self, pilar: str) -> dict:
        plantilla = self.PLANTILLAS[pilar]
        plato = self.plato_aleatorio()
        precio = plato.get("precio", "precio de temporada")
        copy = plantilla["copy"].format(
            restaurante=self.restaurante,
            plato=plato.get("nombre", "nuestro menú"),
            precio=precio,
            restaurante_slug=self.restaurante_slug,
        )
        hashtags = [h.format(restaurante_slug=self.restaurante_slug) for h in plantilla["hashtags"]]
        return {
            "pilar": pilar,
            "copy": copy,
            "hashtags": hashtags,
            "cta": plantilla["cta"],
            "plato_recomendado": plato.get("nombre"),
            "precio": precio,
            "generado_en": datetime.now().isoformat(),
        }


class DirectorArte:
    PROMPTS = {
        "Comercial": {
            "imagen_1x1": "Foto cuadrada 1:1 gastronómica profesional de {plato} en {restaurante}. Primer plano sobre tabla de madera rústica, jugosidad visible, humo leve, luz cálida lateral, f/2.8, 8K.",
            "video_9x16": "Video vertical 9:16 de {plato} en {restaurante}. Corte lento de la carne con cuchillo, jugo escurriendo, brasas al fondo, focus pull suave, 4K vertical, color grading cálido.",
        },
        "Curiosidades de la Parrilla": {
            "imagen_1x1": "Macro cuadrada 1:1 del carbón encendido con brasas incandescentes y partículas de humo en suspensión. Textura íntima de la parrilla, contraluz suave, fondo oscuro madera carbonizada, 8K.",
            "video_9x16": "Video vertical 9:16 cinematic: acercamiento extremo a brasas encendidas, humo volumétrico ascendiendo en hilos translúcidos, chispas leves, profundidad reducida, 4K vertical.",
        },
        "Tips Parrilleros": {
            "imagen_1x1": "Foto cuadrada 1:1 close-up del corte transversal de la carne mostrando cocción interna jugosa. Superficie dorada, fibras visibles, jugo cristalino sobre tabla rústica, estilo didáctico premium.",
            "video_9x16": "Video vertical 9:16 tutorial rápido: cuchillo cortando carne lentamente, close-up del interior jugoso, brasas desenfocadas al fondo, transición humo a plato servido.",
        },
        "Tradición Criolla": {
            "imagen_1x1": "Foto cuadrada 1:1 con ambiente familiar parrilla: mesa rústica con plato principal, copa de vino, pan casero, decoración con carbón y leña, luz cálida acogedora, 8K.",
            "video_9x16": "Video vertical 9:16 narrativo: primeros planos de manos sirviendo parrilla, risas de fondo, humo suave, movimiento natural de la cámara, estética documental gastronómica.",
        },
    }

    def generar_prompts(self, pilar: str, plato: str = "nuestro menú") -> dict:
        prompts = self.PROMPTS[pilar]
        imagen = prompts["imagen_1x1"].format(plato=plato, restaurante="El Chaquito de Felipe")
        video = prompts["video_9x16"].format(plato=plato, restaurante="El Chaquito de Felipe")
        return {"pilar": pilar, "imagen_1x1": imagen, "video_9x16": video}


def generar_lote(perfil: dict, estratega: EstrategaCreativo, director: DirectorArte) -> dict:
    pilares_objetivo = ["Comercial", "Curiosidades de la Parrilla", "Tips Parrilleros", "Tradición Criolla"]
    lote = {"metadata": {"restaurante": perfil.get("nombre"), "generado_en": datetime.now().isoformat(), "total": len(pilares_objetivo)}, "posts": []}
    for pilar in pilares_objetivo:
        post = estratega.generar_post(pilar)
        prompts = director.generar_prompts(pilar, post.get("plato_recomendado", "nuestro menú"))
        lote["posts"].append({"post": post, "prompts_visuales": prompts})
    return lote


def main():
    print("[+] Cargando perfil del restaurante...")
    perfil = json.loads(RUTA_PERFIL.read_text(encoding="utf-8"))

    estratega = EstrategaCreativo(perfil)
    director = DirectorArte()

    print("[+] Generando lote completo del día...")
    lote = generar_lote(perfil, estratega, director)

    RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
        json.dump(lote, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Lote guardado en: {RUTA_SALIDA}")
    print("\n=== RESUMEN FINAL ===\n")
    for entrada in lote["posts"]:
        post = entrada["post"]
        prompts = entrada["prompts_visuales"]
        print(f"Pilar: {post['pilar']}")
        print(f"Copy: {post['copy']}")
        print(f"Hashtags: {', '.join(post['hashtags'])}")
        print(f"CTA: {post['cta']}")
        print(f"Plato: {post['plato_recomendado']} | Precio: {post['precio']}")
        print(f"Imagen 1x1: {prompts['imagen_1x1']}")
        print(f"Video 9:16: {prompts['video_9x16']}")
        print("-" * 80)
    print("\n=== ENTREGA COMPLETA ===")


if __name__ == "__main__":
    main()
