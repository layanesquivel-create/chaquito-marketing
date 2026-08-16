import subprocess
import sys

def ejecutar_script(nombre):
    print(f"\n[+] Ejecutando {nombre}...")
    resultado = subprocess.run([sys.executable, f"scripts/{nombre}"], capture_output=False)
    if resultado.returncode != 0:
        print(f"[!] Error al ejecutar {nombre}")
    else:
        print(f"[OK] {nombre} finalizado con exito.")

def main():
    print("=== INICIANDO PIPELINE DE MARKETING CHAQUITO ===")
    ejecutar_script("optimizar_imagenes.py")
    ejecutar_script("generador_contenido.py")
    ejecutar_script("exportar_csv.py")
    print("\n=== PIPELINE COMPLETADO EXITOSAMENTE ===")

if __name__ == "__main__":
    main()