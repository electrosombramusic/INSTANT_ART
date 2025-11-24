#!/usr/bin/env python3
"""
Script que muestra un carrusel de imágenes de la carpeta 'carrusel'.
Lee las imágenes cada vez que hace una transición para detectar nuevas.
Orden cronológico por timestamp. Pausa de 5 segundos entre imágenes.
"""
import pygame
import sys
from pathlib import Path
from datetime import datetime
from PIL import Image
import time

# Directorios
CARRUSEL_DIR = Path(__file__).parent / "carrusel"

# Extensiones de imagen soportadas
EXTENSIONES_IMAGEN = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}

# Tiempo entre transiciones (segundos)
PAUSA_SEGUNDOS = 5

# Colores
COLOR_FONDO = (0, 0, 0)  # Negro
COLOR_TEXTO = (255, 255, 255)  # Blanco

class CarruselImagenes:
    def __init__(self, ancho=1280, alto=720, fullscreen=True):
        """
        Inicializa el carrusel de imágenes.

        Args:
            ancho: Ancho de la ventana
            alto: Alto de la ventana
            fullscreen: Si True, inicia en pantalla completa
        """
        pygame.init()

        # Configurar pantalla
        if fullscreen:
            self.pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            info = pygame.display.Info()
            self.ancho_pantalla = info.current_w
            self.alto_pantalla = info.current_h
        else:
            self.pantalla = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)
            self.ancho_pantalla = ancho
            self.alto_pantalla = alto

        pygame.display.set_caption("Carrusel de Imágenes - Instant Art")

        # Fuente para el texto
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_pequena = pygame.font.Font(None, 24)

        # Estado
        self.fullscreen = fullscreen
        self.corriendo = True
        self.indice_actual = 0
        self.imagenes = []
        self.ultimo_tiempo = time.time()

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando carrusel de imágenes...")
        print(f"Carpeta: {CARRUSEL_DIR}")
        print(f"Intervalo: {PAUSA_SEGUNDOS} segundos")
        print(f"Resolución: {self.ancho_pantalla}x{self.alto_pantalla}")
        print("\nControles:")
        print("  - ESC o Q: Salir")
        print("  - F: Alternar pantalla completa")
        print("  - ESPACIO: Siguiente imagen")
        print("  - FLECHA IZQUIERDA: Imagen anterior\n")

    def obtener_imagenes_ordenadas(self):
        """
        Lee todas las imágenes de la carpeta carrusel y las ordena cronológicamente.

        Returns:
            list: Lista de Path ordenados por timestamp de creación
        """
        if not CARRUSEL_DIR.exists():
            return []

        imagenes = []
        for archivo in CARRUSEL_DIR.iterdir():
            if archivo.is_file() and archivo.suffix.lower() in EXTENSIONES_IMAGEN:
                try:
                    # Obtener timestamp de creación
                    try:
                        timestamp = archivo.stat().st_birthtime
                    except AttributeError:
                        # En Linux, usar st_ctime
                        timestamp = archivo.stat().st_ctime

                    imagenes.append((timestamp, archivo))
                except Exception as e:
                    print(f"Error al obtener timestamp de {archivo.name}: {e}")

        # Ordenar por timestamp
        imagenes.sort(key=lambda x: x[0])

        # Devolver solo los paths
        return [img[1] for img in imagenes]

    def cargar_y_escalar_imagen(self, path_imagen):
        """
        Carga una imagen y la escala para ajustarla a la pantalla manteniendo aspect ratio.

        Args:
            path_imagen: Path al archivo de imagen

        Returns:
            pygame.Surface: Imagen escalada o None si hay error
        """
        try:
            # Cargar imagen con PIL (mejor soporte de formatos)
            img_pil = Image.open(path_imagen)

            # Convertir a RGB si es necesario
            if img_pil.mode != 'RGB':
                img_pil = img_pil.convert('RGB')

            # Calcular tamaño manteniendo aspect ratio
            img_ancho, img_alto = img_pil.size
            ratio = min(self.ancho_pantalla / img_ancho, self.alto_pantalla / img_alto)
            nuevo_ancho = int(img_ancho * ratio * 0.9)  # 90% para dejar margen
            nuevo_alto = int(img_alto * ratio * 0.9)

            # Redimensionar
            img_pil = img_pil.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)

            # Convertir a formato pygame
            mode = img_pil.mode
            size = img_pil.size
            data = img_pil.tobytes()

            img_pygame = pygame.image.fromstring(data, size, mode)

            return img_pygame

        except Exception as e:
            print(f"Error al cargar imagen {path_imagen.name}: {e}")
            return None

    def dibujar_imagen(self, superficie_imagen, path_imagen):
        """
        Dibuja la imagen en el centro de la pantalla con información.

        Args:
            superficie_imagen: pygame.Surface con la imagen
            path_imagen: Path al archivo de imagen
        """
        # Limpiar pantalla
        self.pantalla.fill(COLOR_FONDO)

        if superficie_imagen:
            # Centrar imagen
            rect_imagen = superficie_imagen.get_rect()
            rect_imagen.center = (self.ancho_pantalla // 2, self.alto_pantalla // 2)
            self.pantalla.blit(superficie_imagen, rect_imagen)

            # Información de la imagen
            timestamp = path_imagen.stat().st_ctime
            fecha_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

            # Texto principal (nombre del archivo)
            texto_nombre = self.fuente.render(path_imagen.name, True, COLOR_TEXTO)
            rect_nombre = texto_nombre.get_rect()
            rect_nombre.centerx = self.ancho_pantalla // 2
            rect_nombre.bottom = self.alto_pantalla - 60

            # Texto secundario (fecha y posición)
            info = f"{fecha_str} | {self.indice_actual + 1}/{len(self.imagenes)}"
            texto_info = self.fuente_pequena.render(info, True, COLOR_TEXTO)
            rect_info = texto_info.get_rect()
            rect_info.centerx = self.ancho_pantalla // 2
            rect_info.bottom = self.alto_pantalla - 20

            # Dibujar textos con fondo semi-transparente
            fondo_nombre = pygame.Surface((rect_nombre.width + 20, rect_nombre.height + 10))
            fondo_nombre.set_alpha(180)
            fondo_nombre.fill((0, 0, 0))
            self.pantalla.blit(fondo_nombre, (rect_nombre.x - 10, rect_nombre.y - 5))
            self.pantalla.blit(texto_nombre, rect_nombre)

            fondo_info = pygame.Surface((rect_info.width + 20, rect_info.height + 10))
            fondo_info.set_alpha(180)
            fondo_info.fill((0, 0, 0))
            self.pantalla.blit(fondo_info, (rect_info.x - 10, rect_info.y - 5))
            self.pantalla.blit(texto_info, rect_info)

        pygame.display.flip()

    def mostrar_mensaje(self, mensaje):
        """
        Muestra un mensaje en el centro de la pantalla.

        Args:
            mensaje: Texto a mostrar
        """
        self.pantalla.fill(COLOR_FONDO)
        texto = self.fuente.render(mensaje, True, COLOR_TEXTO)
        rect = texto.get_rect(center=(self.ancho_pantalla // 2, self.alto_pantalla // 2))
        self.pantalla.blit(texto, rect)
        pygame.display.flip()

    def alternar_fullscreen(self):
        """Alterna entre pantalla completa y modo ventana."""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            info = pygame.display.Info()
            self.ancho_pantalla = info.current_w
            self.alto_pantalla = info.current_h
        else:
            self.pantalla = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
            self.ancho_pantalla = 1280
            self.alto_pantalla = 720

    def ejecutar(self):
        """Loop principal del carrusel."""
        clock = pygame.time.Clock()

        while self.corriendo:
            # Procesar eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.corriendo = False

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_q:
                        self.corriendo = False
                    elif evento.key == pygame.K_f:
                        self.alternar_fullscreen()
                    elif evento.key == pygame.K_SPACE:
                        # Avanzar manualmente
                        self.ultimo_tiempo = 0
                    elif evento.key == pygame.K_LEFT:
                        # Retroceder
                        if self.imagenes:
                            self.indice_actual = (self.indice_actual - 2) % len(self.imagenes)
                            self.ultimo_tiempo = 0

                elif evento.type == pygame.VIDEORESIZE:
                    self.ancho_pantalla = evento.w
                    self.alto_pantalla = evento.h

            # Actualizar carrusel cada PAUSA_SEGUNDOS
            tiempo_actual = time.time()
            if tiempo_actual - self.ultimo_tiempo >= PAUSA_SEGUNDOS:
                # Leer imágenes (para detectar nuevas)
                imagenes_nuevas = self.obtener_imagenes_ordenadas()

                if not imagenes_nuevas:
                    self.mostrar_mensaje('Esperando imágenes en carpeta "carrusel"...')
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Esperando imágenes...")
                else:
                    # Detectar cambios en la lista
                    if len(imagenes_nuevas) != len(self.imagenes):
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Detectadas {len(imagenes_nuevas)} imágenes (antes: {len(self.imagenes)})")
                        if self.indice_actual >= len(imagenes_nuevas):
                            self.indice_actual = 0

                    self.imagenes = imagenes_nuevas

                    # Mostrar imagen actual
                    if self.indice_actual < len(self.imagenes):
                        path_imagen = self.imagenes[self.indice_actual]
                        superficie = self.cargar_y_escalar_imagen(path_imagen)
                        self.dibujar_imagen(superficie, path_imagen)
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Mostrando: {path_imagen.name}")

                        # Avanzar al siguiente (circular)
                        self.indice_actual = (self.indice_actual + 1) % len(self.imagenes)

                self.ultimo_tiempo = tiempo_actual

            clock.tick(30)  # 30 FPS

        pygame.quit()

def main():
    carrusel = CarruselImagenes(fullscreen=True)
    carrusel.ejecutar()

if __name__ == "__main__":
    main()
