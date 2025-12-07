# INSTANT_ART

Sistema para captura y procesamiento de fotos en eventos: móvil → PC → IA → carrusel / Instagram / mailing / impresión.

## Estructura

instant-art/
├── src/ # Código principal
│ ├── monitor_fotos.py
│ ├── procesa.py
│ └── carrusel.py
├── data/
│ ├── input/ # Fotos originales
│ └── output/ # Fotos procesadas
├── docs/
│ ├── arquitectura.md
│ └── flujo_QA.md
├── tests/ # Pruebas futuras
├── requirements.txt
└── README.md

bash
Copiar código

## Requisitos

- Python 3.10+
- Windows / Linux (WSL recomendado)
- Dependencias: Pillow, NumPy, Pygame

## Instalación

```bash
# Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux / WSL
.venv\Scripts\Activate.ps1 # Windows PowerShell

# Instalar dependencias
pip install -r requirements.txt
Flujo
css
Copiar código
data/input → [monitor_fotos] → data/output → [carrusel / publicación]
Uso
Ejecutar cada script en terminal separada:

bash
Copiar código
python src/monitor_fotos.py
python src/procesa.py
python src/carrusel.py
Controles del Carrusel
ESC / Q → Salir

F → Pantalla completa

SPACE → Siguiente imagen

LEFT ARROW → Imagen anterior

Notas
Detección de nuevas fotos por timestamps

procesa.py integra IA para efectos artísticos

Escalable: nuevas fuentes de entrada, backends de IA, integración social

Contribuir
Documentar bugs / sugerencias en docs/

Mantener estructura y comentarios claros
Configurable para CI/CD sin modificaciones mayores.

