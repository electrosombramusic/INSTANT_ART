import os
import socket
import qrcode
import uuid
from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename # Útil para limpiar el nombre del archivo si fuera necesario

# --- CONFIGURACIÓN Y ESTRUCTURA ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'data', 'input')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'} # Solo permitimos formatos de imagen
# Almacén de tokens activos (Sólo se permite usar una vez por token)
# Usaremos un set para búsquedas rápidas
ACTIVE_TOKENS = set() 
SESSION_TOKEN = None # El token que se genera al inicio y se espera escanear

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# La clave secreta es necesaria para manejar sesiones en Flask (aunque aquí usamos tokens simples)
app.secret_key = str(uuid.uuid4()) 

# --- FUNCIONES DE VALIDACIÓN ---

def allowed_file(filename):
    """Verifica si la extensión del archivo está permitida (parte A de la mejora)."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- HTML SÚPER SIMPLE PARA EL MÓVIL ---
# Modificamos la página para enviar el token en un campo oculto (hidden input)
HTML_PAGE = """
<!doctype html>
<html lang="es">
<body>
    <h1>📸 INSTANT_ART</h1>
    <p>Token de Sesión: {{ token }}</p>
    
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="hidden" name="session_token" value="{{ token }}">
        <label for="file-upload">📸 Capturar y Enviar Foto</label>
        
        <input id="file-upload" type="file" name="file" accept="image/*" capture="camera" onchange="this.form.submit()">
    </form>
</body>
</html>
"""

# --- RUTAS ---
@app.route('/')
def index():
    # Si alguien navega a la raíz sin un token, lo redirigimos a usar el QR
    return HTML_DENIED, 403

@app.route('/session/<token>')
def session_page(token):
    # Verificamos si el token existe y es válido
    if token in ACTIVE_TOKENS:
        # Aquí se usa el token por primera vez al abrir la página.
        # Podríamos invalidarlo justo antes de la subida, pero para una seguridad estricta,
        # nos aseguramos de que solo la página con el token válido se muestre.
        return render_template_string(HTML_PAGE, token=token)
    else:
        return render_template_string(HTML_DENIED), 403

@app.route('/upload', methods=['POST'])
def upload_file():
    # 1. VERIFICACIÓN DE TOKEN
    token = request.form.get('session_token')
    if not token or token not in ACTIVE_TOKENS:
        print(f"🚨 SUBIDA RECHAZADA: Token inválido o expirado.")
        return render_template_string(HTML_DENIED), 403
    
    # 2. PROCESAMIENTO DE ARCHIVO
    if 'file' not in request.files:
        return 'No se encontró archivo', 400
    file = request.files['file']
    
    if file.filename == '':
        return 'Nombre de archivo vacío', 400
        
    # 3. VERIFICACIÓN DE SEGURIDAD DEL ARCHIVO (Parte A)
    if not allowed_file(file.filename):
        print(f"🚨 SUBIDA RECHAZADA: Tipo de archivo no permitido: {file.filename}")
        return 'Tipo de archivo no permitido. Solo JPG, PNG, WEBP.', 400
        
    # 4. GUARDAR Y ASIGNAR NOMBRE SEGURO (Parte B)
    if file:
        # Generar nombre de archivo único
        original_ext = file.filename.rsplit('.', 1)[1].lower()
        safe_filename = f"{uuid.uuid4()}.{original_ext}"
        
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        file.save(save_path)
        
        # 5. INACTIVAR TOKEN (¡El paso de seguridad crítico!)
        ACTIVE_TOKENS.remove(token)
        print(f"✅ FOTO RECIBIDA: {save_path} | Token {token} invalidado.")
        
        # 6. GENERAR NUEVO TOKEN PARA EL SIGUIENTE USUARIO
        global SESSION_TOKEN
        SESSION_TOKEN = generate_new_session_token()
        
        return render_template_string(HTML_SUCCESS)

# --- FUNCIONES DE RED Y TOKENS ---
def get_ip():
    """Obtiene la IP local de tu ordenador para generar el link."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def generate_new_session_token():
    """Genera un nuevo token único y lo añade a la lista de activos."""
    new_token = str(uuid.uuid4())
    ACTIVE_TOKENS.add(new_token)
    return new_token

def generate_qr(url):
    """Genera y muestra el QR en la terminal."""
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)
    print("\n" * 2)
    print("--------------------------------------------------")
    print(f"--- NUEVA SESIÓN LISTA: ESCANEA ESTE QR CON MÓVIL ---")
    print(f"Dirección: {url}")
    print("--------------------------------------------------")
    qr.print_ascii(invert=True)
    print("\n" * 2)

if __name__ == '__main__':
    # 1. GENERAR EL PRIMER TOKEN
    SESSION_TOKEN = generate_new_session_token() 
    
    # 2. PREPARAR LA DIRECCIÓN DE RED
    local_ip = get_ip()
    port = 5000
    # La URL ahora incluye el token de sesión
    url = f"http://{local_ip}:{port}/session/{SESSION_TOKEN}"
    
    # 3. MOSTRAR QR E INICIAR SERVIDOR
    generate_qr(url)
    
    print("Servidor listo. ¡Solo se permitirá una subida por token!")
    app.run(host='0.0.0.0', port=port, debug=False)