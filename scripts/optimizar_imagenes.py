import os
from PIL import Image

ASSETS_DIR = r"D:\chaquito-marketing\assets\imagenes"
OUTPUT_DIR = r"D:\chaquito-marketing\assets\imagenes\optimizadas"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def optimizar():
    valid_exts = ('.jpg', '.jpeg', '.png')
    archivos = [f for f in os.listdir(ASSETS_DIR) if f.lower().endswith(valid_exts)]
    
    if not archivos:
        print("[!] No hay imagenes en " + ASSETS_DIR)
        return
        
    for archivo in archivos:
        ruta_in = os.path.join(ASSETS_DIR, archivo)
        nombre_base = os.path.splitext(archivo)[0]
        ruta_out = os.path.join(OUTPUT_DIR, nombre_base + ".webp")
        
        with Image.open(ruta_in) as img:
            img = img.convert("RGB")
            img.save(ruta_out, "WEBP", quality=85, optimize=True)
            print(f"[+] Convertido: {archivo} -> {nombre_base}.webp")
            
    print("[OK] Proceso finalizado.")

if __name__ == "__main__":
    optimizar()