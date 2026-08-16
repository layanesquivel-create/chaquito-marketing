import json
import os
from datetime import datetime

OUTPUT_FILE = r"D:\chaquito-marketing\contenido\posts\campana_activa.json"
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

menu_data = {
    "restaurante": "El Chaquito de Felipe",
    "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "campana": "Especial Parrillero",
    "publicaciones": [
        {
            "red_social": "Instagram / Facebook",
            "tipo": "Post",
            "copy": "🔥 ¡El auténtico sabor a la parrilla te espera en El Chaquito de Felipe! Cortes jugosos, guarniciones tradicionales y la mejor atención. 🥩✨\n\n📍 Te esperamos hoy. ¡Haz tu reserva por WhatsApp!",
            "hashtags": ["#ElChaquitoDeFelipe", "#ParrillaBolivia", "#CarnesLaPaz", "#SaborTradicional"],
            "asset_sugerido": "parrillada_premium.webp"
        },
        {
            "red_social": "WhatsApp Business",
            "tipo": "Estado / Mensaje Masivo",
            "copy": "👋 ¡Hola! Hoy tenemos parrillada especial lista para servir en El Chaquito de Felipe. 🍖🔥 Consulta nuestro menú del día respondiendo a este mensaje.",
            "hashtags": [],
            "asset_sugerido": "menu_dia.webp"
        }
    ]
}

def guardar_campana():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(menu_data, f, ensure_ascii=False, indent=4)
    print(f"[OK] Campaña generada exitosamente en: {OUTPUT_FILE}")

if __name__ == "__main__":
    guardar_campana()