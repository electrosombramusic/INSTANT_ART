# Instant Art - Sistema de Procesamiento de Imágenes

Sistema automatizado que monitorea, procesa y muestra imágenes en un carrusel interactivo.

## Descripción

Este proyecto consta de tres scripts de Python que trabajan en conjunto:

1. **monitor_fotos.py** - Monitorea la carpeta `fotos/` y copia archivos nuevos a `proceso/`
2. **procesa.py** - Procesa imágenes de `proceso/` intercambiando canales RGB y las guarda en `carrusel/`
3. **carrusel.py** - Muestra las imágenes procesadas en un slideshow interactivo

## Estructura de Carpetas

```
instant-art/
├── fotos/          # Carpeta de entrada (coloca aquí las imágenes originales) *
├── proceso/        # Carpeta intermedia (imágenes copiadas) *
├── carrusel/       # Carpeta de salida (imágenes procesadas) *
├── venv/           # Entorno virtual de Python
├── monitor_fotos.py
├── procesa.py
├── carrusel.py
├── requirements.txt
└── README.md
```

**Nota**: Las carpetas marcadas con `*` deben ser creadas manualmente la primera vez (ver sección de Instalación).

## Requisitos Previos

- **Sistema Operativo**: Windows 10 o Windows 11
- **Python**: 3.10 o superior
- **pip**: Gestor de paquetes de Python (incluido con Python)

### Verificar instalación de Python

Abre **PowerShell** o **CMD** y ejecuta:

```cmd
python --version
```

Si no tienes Python instalado:

1. Descarga Python desde [python.org/downloads](https://www.python.org/downloads/)
2. Ejecuta el instalador
3. **IMPORTANTE**: Marca la casilla "Add Python to PATH" durante la instalación
4. Reinicia la terminal después de instalar

## Instalación

### 1. Clonar o descargar el proyecto

Si estás clonando desde un repositorio:

```cmd
git clone <url-del-repositorio>
cd instant-art
```

Si ya tienes los archivos, navega a la carpeta:

```cmd
cd C:\ruta\a\instant-art
```

### 2. Crear las carpetas de trabajo

Las carpetas `fotos/`, `proceso/` y `carrusel/` no están incluidas en el repositorio (están en `.gitignore`). Créalas con:

**En PowerShell:**
```powershell
mkdir fotos, proceso, carrusel
```

**En CMD:**
```cmd
mkdir fotos
mkdir proceso
mkdir carrusel
```

Estas carpetas son necesarias para el flujo de trabajo del sistema:
- **fotos/**: Aquí colocarás las imágenes originales
- **proceso/**: Carpeta intermedia (el monitor copiará aquí las imágenes)
- **carrusel/**: Carpeta de salida con imágenes procesadas

### 3. Crear el entorno virtual

```cmd
python -m venv venv
```

### 4. Activar el entorno virtual

**En PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

**En CMD:**
```cmd
venv\Scripts\activate.bat
```

**Nota**: Verás `(venv)` al inicio de tu línea de comando cuando el entorno esté activo.

**Si obtienes error de permisos en PowerShell**, ejecuta esto como Administrador:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 5. Instalar dependencias

```cmd
pip install -r requirements.txt
```

Esto instalará:
- **Pillow** - Manipulación de imágenes
- **NumPy** - Operaciones con arrays
- **Pygame** - Visualización del carrusel

### 6. Verificar instalación

```cmd
python -c "import PIL, numpy, pygame; print('✓ Todas las dependencias instaladas correctamente')"
```

## Uso

### Ejecutar el sistema completo

Necesitarás **3 ventanas de terminal** abiertas (PowerShell o CMD).

#### Terminal 1: Monitor de Fotos

**En PowerShell:**
```powershell
cd C:\ruta\a\instant-art
venv\Scripts\Activate.ps1
python monitor_fotos.py
```

**En CMD:**
```cmd
cd C:\ruta\a\instant-art
venv\Scripts\activate.bat
python monitor_fotos.py
```

Este script monitorea cada 15 segundos la carpeta `fotos/` y copia archivos nuevos a `proceso/`.

#### Terminal 2: Procesador de Imágenes

**En PowerShell:**
```powershell
cd C:\ruta\a\instant-art
venv\Scripts\Activate.ps1
python procesa.py
```

**En CMD:**
```cmd
cd C:\ruta\a\instant-art
venv\Scripts\activate.bat
python procesa.py
```

Este script procesa cada 15 segundos las imágenes de `proceso/`, intercambia aleatoriamente sus canales RGB y las guarda en `carrusel/`.

#### Terminal 3: Carrusel de Imágenes

**En PowerShell:**
```powershell
cd C:\ruta\a\instant-art
venv\Scripts\Activate.ps1
python carrusel.py
```

**En CMD:**
```cmd
cd C:\ruta\a\instant-art
venv\Scripts\activate.bat
python carrusel.py
```

Este script muestra las imágenes procesadas en un carrusel con transiciones cada 5 segundos.

### Controles del Carrusel

Cuando el carrusel esté ejecutándose:

- **ESC o Q** - Salir del carrusel
- **F** - Alternar pantalla completa / modo ventana
- **ESPACIO** - Avanzar manualmente a la siguiente imagen
- **FLECHA IZQUIERDA** - Retroceder a la imagen anterior

### Flujo de Trabajo

1. **Añade imágenes** a la carpeta `fotos/`
2. El script `monitor_fotos.py` las copiará automáticamente a `proceso/`
3. El script `procesa.py` las procesará y guardará en `carrusel/`
4. El carrusel las mostrará automáticamente en orden cronológico

```
USUARIO → fotos/ → [monitor] → proceso/ → [procesa] → carrusel/ → [visualización]
```

## Detener los Scripts

Para detener cualquier script:

1. Ve a la ventana de terminal donde está corriendo
2. Presiona **Ctrl + C**

Para salir del entorno virtual:

```cmd
deactivate
```

## Formatos de Imagen Soportados

El sistema soporta los siguientes formatos:
- JPG / JPEG
- PNG
- BMP
- GIF
- TIFF
- WebP

## Troubleshooting

### Error: "La carpeta no existe"

Si ves errores como `[ERROR] La carpeta fotos no existe`, significa que olvidaste crear las carpetas de trabajo. Créalas con:

**En PowerShell:**
```powershell
mkdir fotos, proceso, carrusel
```

**En CMD:**
```cmd
mkdir fotos
mkdir proceso
mkdir carrusel
```

### Error: "ModuleNotFoundError"

Asegúrate de que:
1. El entorno virtual esté activado (deberías ver `(venv)` en tu terminal)
2. Hayas instalado las dependencias: `pip install -r requirements.txt`

### Error: "Python no se reconoce como comando"

Esto significa que Python no está en tu PATH:
1. Reinstala Python desde [python.org](https://www.python.org/downloads/)
2. **Marca la casilla "Add Python to PATH"** durante la instalación
3. Reinicia la terminal después de instalar

### Error de permisos en PowerShell

Si obtienes un error al activar el entorno virtual en PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### El carrusel no muestra imágenes

1. Verifica que haya imágenes en la carpeta `carrusel/`
2. Revisa que los otros dos scripts estén corriendo
3. Comprueba la consola para mensajes de error

### Las imágenes no se procesan

1. Asegúrate de que `monitor_fotos.py` esté copiando archivos a `proceso/`
2. Verifica que las imágenes tengan un formato soportado
3. Revisa que las carpetas existan y tengan permisos de escritura

### Pygame no funciona en Windows

Si tienes problemas con pygame:

1. Actualiza pip primero:
```cmd
python -m pip install --upgrade pip
```

2. Reinstala pygame:
```cmd
pip uninstall pygame
pip install pygame
```

3. Si persiste el error, instala Visual C++ Redistributable desde:
https://aka.ms/vs/17/release/vc_redist.x64.exe

## Configuración Avanzada

### Cambiar intervalos de tiempo

Edita las constantes al inicio de cada script:

**monitor_fotos.py** y **procesa.py**:
```python
time.sleep(15)  # Cambiar a los segundos deseados
```

**carrusel.py**:
```python
PAUSA_SEGUNDOS = 5  # Cambiar a los segundos deseados
```

### Cambiar carpetas de origen/destino

Edita las variables al inicio de cada script:

```python
FOTOS_DIR = Path(__file__).parent / "nombre_carpeta"
```

## Notas para el Desarrollador

- Los scripts usan **timestamps de creación** (`st_ctime`) para detectar archivos nuevos
- Las imágenes se ordenan cronológicamente en el carrusel
- El procesamiento RGB intercambia canales aleatoriamente, creando efectos visuales únicos
- Todos los scripts muestran logs con timestamps para facilitar el debugging

## Contribuir

Si encuentras bugs o tienes sugerencias:

1. Documenta el problema con capturas de pantalla si es posible
2. Incluye el mensaje de error completo
3. Especifica tu versión de Windows y Python

## Licencia

[Especificar licencia aquí]

## Contacto

[Especificar información de contacto]

---

**¡Listo para usar!** Coloca algunas imágenes en la carpeta `fotos/` y observa cómo el sistema las procesa y muestra automáticamente.
