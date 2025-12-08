<<<<<<< HEAD
Proyecto de Automatización con Python y Selenium

Este repositorio contiene un entorno básico de automatización pensado para pruebas funcionales y de regresión. La estructura está organizada para trabajar cómodamente desde WSL + VS Code, con instalación sencilla y comandos directos desde terminal.

Estructura

src/: Código principal del proyecto.

tests/: Casos de prueba y suites.

requirements.txt: Dependencias.

venv/: Entorno virtual (no se sube al repo).

Requisitos

Python 3.10+

WSL o Linux

Navegador compatible + WebDriver

Instalación rápida

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Ejecución

pytest -v

Notas

Estructura pensada para escalar a Page Object Model.

Configurable para CI/CD sin modificaciones mayores.
=======
INSTANT_ART es un sistema pensado para eventos (bodas, fiestas, ferias, empresas) que captura fotos desde móviles u ordenadores, las procesa con IA en tiempo real, las etiqueta automáticamente para redes sociales, las muestra en pantallas y permite imprimirlas o enviarlas por email.

La idea mejora radicalmente a los “photomatones con IA” actuales, que son caros, rígidos y dan resultados pobres. INSTANT_ART es moderno, portátil, rápido y funciona en cualquier dispositivo.

Objetivo del sistema

Crear una plataforma que:

Detecta nuevas fotos en un directorio o desde un móvil.

Procesa la imagen con IA (ajustes, efectos, estilo, branding del evento).

Genera versiones optimizadas para Instagram, pantallas y correo.

Publica automáticamente en redes o sistemas de pantalla.

Envía email automático con la foto al usuario.

Permite impresión local si el cliente lo desea.

Puede ser vendido o alquilado:

como servicio para eventos,

o como software autosuficiente “pago por uso/foto”.

Ventaja competitiva

No es un aparato físico antiguo: es software portable.

Se ejecuta en un portátil, tablet o móvil.

Totalmente personalizable por evento (marco, colores, hashtag).

El cliente puede gestionarlo sin técnico.

El flujo es rápido y completamente automático.

Situación actual del repositorio

Repositorio ordenado, con estructura clara:

src/
data/input
data/output
docs/
tests/
>>>>>>> e13d7572632a2d9b334d9d920fbbcd7aca8adf55
