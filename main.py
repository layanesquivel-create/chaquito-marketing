import subprocess
import sys

def ejecutar_script(nombre):
    print(f"\n[+] Ejecutando {nombre}...")
    resultado = subprocess.run([sys.executable, f"scripts/{nombre}"])
    if resultado.returncode != 0:
        print(f"[!] Error al ejecutar {nombre}")
        sys.exit(1)
    else:
        print(f"[OK] {nombre} finalizado con exito.")

def main():
    print("=== INICIANDO PIPELINE DE MARKETING CHAQUITO ===")
    ejecutar_script("validar_menu.py")
    ejecutar_script("optimizar_imagenes.py")
    ejecutar_script("generador_contenido.py")
    ejecutar_script("exportar_csv.py")
    ejecutar_script("generador_prompts_ia.py")
    ejecutar_script("exportar_prompts.py")
    ejecutar_script("agencia_autonoma.py")
    print("\n=== PIPELINE COMPLETADO EXITOSAMENTE ===")

if __name__ == "__main__":
    main()