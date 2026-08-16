import json
import os
import sys

JSON_PATH = r"D:\chaquito-marketing\contenido\posts\campana_activa.json"

def validar():
    if not os.path.exists(JSON_PATH):
        print(f"[!] Error: No se encontro el archivo de campana: {JSON_PATH}")
        sys.exit(1)

    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[!] Error de sintaxis JSON: {e}")
        sys.exit(1)

    publicaciones = data.get("publicaciones", [])
    if not publicaciones:
        print("[!] Advertencia: No hay publicaciones definidas en la campana.")
        sys.exit(1)

    for i, pub in enumerate(publicaciones, start=1):
        if not pub.get("copy"):
            print(f"[!] Error en publicacion #{i}: Falta el texto (copy).")
            sys.exit(1)
        if not pub.get("red_social"):
            print(f"[!] Error en publicacion #{i}: Falta definir la red social.")
            sys.exit(1)

    print(f"[OK] Validacion exitosa: {len(publicaciones)} publicaciones verificadas correctamente.")

if __name__ == "__main__":
    validar()