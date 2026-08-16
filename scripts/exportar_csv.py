import json
import csv
import os

JSON_PATH = r"D:\chaquito-marketing\contenido\posts\campana_activa.json"
CSV_PATH = r"D:\chaquito-marketing\contenido\posts\programacion_meta.csv"

def exportar_csv():
    if not os.path.exists(JSON_PATH):
        print(f"[!] Error: No se encontro el archivo {JSON_PATH}")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    publicaciones = data.get("publicaciones", [])
    
    with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Red Social", "Tipo", "Texto Publicacion", "Hashtags", "Imagen Sugerida"])
        
        for pub in publicaciones:
            hashtags_str = " ".join(pub.get("hashtags", []))
            writer.writerow([
                pub.get("red_social", ""),
                pub.get("tipo", ""),
                pub.get("copy", ""),
                hashtags_str,
                pub.get("asset_sugerido", "")
            ])
            
    print(f"[OK] Exportacion exitosa a CSV: {CSV_PATH}")

if __name__ == "__main__":
    exportar_csv()