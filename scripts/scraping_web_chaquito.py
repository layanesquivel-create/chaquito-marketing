import json
import re
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("[!] Faltan dependencias. Instala requests y beautifulsoup4.")
    raise

URL = "https://chaquitodefelipe1.netlify.app/"
BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_SALIDA = BASE_DIR / "config" / "restaurante_perfil.json"


def obtener_html():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    r = requests.get(URL, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text


def extraer_menu(soup):
    categorias = []
    categorias_conocidas = [
        "Parrillas y Asados",
        "Cortes y Especialidades",
        "Express y Piqueos",
        "Bebidas y Vinos",
    ]
    secciones = []
    for nombre in categorias_conocidas:
        heading = soup.find(lambda tag: tag.name in ["h2", "h3", "h4"] and tag.get_text(strip=True) == nombre)
        if not heading:
            continue
        items = []
        elem = heading.find_next_sibling()
        while elem and elem.name not in ["h2", "h3", "h4"]:
            if elem.name == "div":
                nombre_tag = elem.find(["h3", "h4", "strong"])
                if not nombre_tag:
                    elem = elem.find_next_sibling()
                    continue
                platillo = nombre_tag.get_text(strip=True)
                descripcion = ""
                desc_tag = nombre_tag.find_next_sibling()
                if desc_tag and desc_tag.name in ["p", "div"]:
                    descripcion = desc_tag.get_text(strip=True)
                precio = ""
                precio_match = re.search(r"(\d+)\s*Bs\.?", elem.get_text())
                if precio_match:
                    precio = f"{precio_match.group(1)} Bs."
                items.append({"nombre": platillo, "descripcion": descripcion, "precio": precio})
            elem = elem.find_next_sibling()
        if items:
            categorias.append({"categoria": nombre, "items": items})
    return categorias


def extraer_info_general(soup):
    texto = soup.get_text(" ", strip=True)

    nombre = "El Chaquito de Felipe"
    desc_match = re.search(r"(20 Años Encendiendo la Pasión por el Asado[^$]+)", texto)
    descripcion = desc_match.group(1).strip() if desc_match else ""

    horario_match = re.search(r"Atendemos de ([^.]+\.)", texto)
    horario = horario_match.group(1).strip() if horario_match else "Lunes a Sábado, 12:00 PM - 22:00 PM"

    direccion_match = re.search(r"Calle Panamá[^$]+", texto)
    direccion = direccion_match.group(0).strip() if direccion_match else "Calle Panamá, casi esquina Plaza Uyuni (Miraflores / Centro), La Paz, Bolivia"

    telefono_match = re.search(r"\+591\s*\d{6,}", texto)
    telefono = telefono_match.group(0).strip().replace(" ", "") if telefono_match else "+591 68133991"

    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", texto)
    email = email_match.group(0).strip() if email_match else "info@elchaquitodefelipe.com"

    redes = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        txt = a.get_text(strip=True)
        if txt and "facebook" in href.lower():
            redes.append({"nombre": txt, "url": href})
        elif txt and "instagram" in href.lower():
            redes.append({"nombre": txt, "url": href})
        elif txt and "tiktok" in href.lower():
            redes.append({"nombre": txt, "url": href})
    redes = [dict(t) for t in {tuple(d.items()) for d in redes}]

    whatsapp = ""
    for a in soup.find_all("a", href=True):
        if "wa.me" in a["href"]:
            whatsapp = a["href"]
            break

    return {
        "nombre": nombre,
        "descripcion": descripcion,
        "horario_atencion": horario,
        "direccion": direccion,
        "telefono": telefono,
        "email": email,
        "web_oficial": URL,
        "redes_sociales": redes,
        "whatsapp": whatsapp,
    }


def main():
    print("[+] Obteniendo HTML de la web...")
    html = obtener_html()
    soup = BeautifulSoup(html, "html.parser")

    print("[+] Extrayendo información general...")
    info = extraer_info_general(soup)

    print("[+] Extrayendo menú...")
    menu = extraer_menu(soup)

    perfil = {
        "nombre": info["nombre"],
        "tipo": "Restaurante de parrillas y comida criolla tradicional",
        "ubicacion": "La Paz, Bolivia",
        "descripcion": info["descripcion"],
        "menu_principal": [
            {
                "categoria": cat["categoria"],
                "items": [
                    {
                        "nombre": item["nombre"],
                        "descripcion": item["descripcion"],
                        "precio": item["precio"],
                    }
                    for item in cat["items"]
                ],
            }
            for cat in menu
        ],
        "tono_comunicacion": "Cercano, familiar, apetitoso, tradicional y festivo",
        "llamado_a_la_accion": "Pedidos a domicilio y reservas por WhatsApp",
        "web_oficial": info["web_oficial"],
        "contacto": {
            "telefono": info["telefono"],
            "email": info["email"],
            "whatsapp": info["whatsapp"],
            "direccion": info["direccion"],
            "horario_atencion": info["horario_atencion"],
        },
        "redes_sociales": info["redes_sociales"],
        "estilo_visual": "Fotografia gastronomica macro, humo de brasas, cortes jugosos, iluminacion calida, tablas de madera rustica, videos verticales 9:16 en camara lenta",
    }

    RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
        json.dump(perfil, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Perfil guardado en: {RUTA_SALIDA}")
    print("\n=== JSON RESULTANTE ===\n")
    print(json.dumps(perfil, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
