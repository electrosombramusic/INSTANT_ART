#!/usr/bin/env python3
"""
Script que monitorea la carpeta 'fotos' cada 15 segundos y copia
archivos nuevos a la carpeta 'proceso' basándose en timestamps.
"""
import os
import shutil
import time
from pathlib import Path
from datetime import datetime

# Directorios
FOTOS_DIR = Path(__file__).parent / "fotos"
PROCESO_DIR = Path(__file__).parent / "proceso"

# Timestamp de inicio
ultimo_check = datetime.now().timestamp()

print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando monitoreo de carpeta 'fotos'...")
print(f"Carpeta origen: {FOTOS_DIR}")
print(f"Carpeta destino: {PROCESO_DIR}")
print(f"Intervalo: 15 segundos\n")

while True:
    try:
        # Verificar que las carpetas existan
        if not FOTOS_DIR.exists():
            print(f"[ERROR] La carpeta {FOTOS_DIR} no existe")
            time.sleep(15)
            continue

        if not PROCESO_DIR.exists():
            print(f"[ERROR] La carpeta {PROCESO_DIR} no existe")
            time.sleep(15)
            continue

        # Buscar archivos nuevos
        archivos_nuevos = []
        for archivo in FOTOS_DIR.iterdir():
            if archivo.is_file():
                # Obtener timestamp de creación (o modificación si no está disponible)
                try:
                    timestamp_creacion = archivo.stat().st_birthtime
                except AttributeError:
                    # En Linux, st_birthtime no está disponible, usar st_ctime
                    timestamp_creacion = archivo.stat().st_ctime

                # Si el archivo es más nuevo que nuestro último check
                if timestamp_creacion > ultimo_check:
                    archivos_nuevos.append(archivo)

        # Copiar archivos nuevos
        if archivos_nuevos:
            for archivo in archivos_nuevos:
                destino = PROCESO_DIR / archivo.name
                try:
                    shutil.copy2(archivo, destino)
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Copiado: {archivo.name}")
                except Exception as e:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✗ Error al copiar {archivo.name}: {e}")

        # Actualizar timestamp del último check
        ultimo_check = datetime.now().timestamp()

        # Esperar 15 segundos
        time.sleep(15)

    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Monitoreo detenido por el usuario")
        break
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error inesperado: {e}")
        time.sleep(15)
