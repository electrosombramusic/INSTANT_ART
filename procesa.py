#!/usr/bin/env python3
"""
Script que monitorea la carpeta 'fotos' cada 15 segundos, procesa imágenes
intercambiando aleatoriamente sus canales RGB y las guarda en 'carrusel'.
"""
import os
import time
import random
from pathlib import Path
from datetime import datetime
from PIL import Image
import numpy as np

# Directorios
FOTOS_DIR = Path(__file__).parent / "proceso"
CARRUSEL_DIR = Path(__file__).parent / "carrusel"

# Extensiones de imagen soportadas
EXTENSIONES_IMAGEN = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}

# Timestamp de inicio
ultimo_check = datetime.now().timestamp()

def intercambiar_canales_rgb(imagen_path):
    """
    Abre una imagen e intercambia aleatoriamente sus canales RGB.

    Args:
        imagen_path: Path al archivo de imagen

    Returns:
        PIL.Image: Imagen con canales intercambiados
    """
    # Abrir imagen
    img = Image.open(imagen_path)

    # Convertir a RGB si no lo es (por ejemplo, si es RGBA o escala de grises)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Convertir a array numpy para manipular canales
    img_array = np.array(img)

    # Crear una permutación aleatoria de los índices [0, 1, 2] (R, G, B)
    permutacion = list(range(3))
    random.shuffle(permutacion)

    # Aplicar la permutación a los canales
    img_procesada = img_array[:, :, permutacion]

    # Convertir de vuelta a imagen PIL
    return Image.fromarray(img_procesada.astype('uint8')), permutacion

print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando procesamiento de imágenes...")
print(f"Carpeta origen: {FOTOS_DIR}")
print(f"Carpeta destino: {CARRUSEL_DIR}")
print(f"Intervalo: 15 segundos")
print(f"Extensiones soportadas: {', '.join(EXTENSIONES_IMAGEN)}\n")

while True:
    try:
        # Verificar que las carpetas existan
        if not FOTOS_DIR.exists():
            print(f"[ERROR] La carpeta {FOTOS_DIR} no existe")
            time.sleep(15)
            continue

        if not CARRUSEL_DIR.exists():
            print(f"[ERROR] La carpeta {CARRUSEL_DIR} no existe")
            time.sleep(15)
            continue

        # Buscar imágenes nuevas
        imagenes_nuevas = []
        for archivo in FOTOS_DIR.iterdir():
            if archivo.is_file() and archivo.suffix.lower() in EXTENSIONES_IMAGEN:
                # Obtener timestamp de creación
                try:
                    timestamp_creacion = archivo.stat().st_birthtime
                except AttributeError:
                    # En Linux, usar st_ctime
                    timestamp_creacion = archivo.stat().st_ctime

                # Si el archivo es más nuevo que nuestro último check
                if timestamp_creacion > ultimo_check:
                    imagenes_nuevas.append(archivo)

        # Procesar imágenes nuevas
        if imagenes_nuevas:
            for imagen_path in imagenes_nuevas:
                try:
                    # Procesar imagen (intercambiar canales RGB)
                    img_procesada, permutacion = intercambiar_canales_rgb(imagen_path)

                    # Generar nombre de salida
                    nombre_base = imagen_path.stem
                    extension = imagen_path.suffix
                    nombre_salida = f"{nombre_base}_rgb{extension}"
                    ruta_salida = CARRUSEL_DIR / nombre_salida

                    # Guardar imagen procesada
                    img_procesada.save(ruta_salida, quality=95)

                    # Mapeo de permutación para mostrar
                    canales = ['R', 'G', 'B']
                    permutacion_str = f"[{canales[permutacion[0]]}, {canales[permutacion[1]]}, {canales[permutacion[2]]}]"

                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Procesada: {imagen_path.name} -> {nombre_salida}")
                    print(f"  Permutación RGB: {permutacion_str}")

                except Exception as e:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✗ Error al procesar {imagen_path.name}: {e}")

        # Actualizar timestamp del último check
        ultimo_check = datetime.now().timestamp()

        # Esperar 15 segundos
        time.sleep(15)

    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Procesamiento detenido por el usuario")
        break
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error inesperado: {e}")
        time.sleep(15)
