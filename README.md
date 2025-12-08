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