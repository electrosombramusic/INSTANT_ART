import os
import socket
import qrcode
import uuid
from flask import Flask, request, render_template_string, redirect, url_for
from werkzeug.utils import secure_filename
import miniupnpc  # Para UPnP

# --- HTMLs DEFINIDOS PRIMERO (arregla Pylance) ---
HTML_DENIED = """
<!doctype html>
<html lang="es">
<body>
    <h1>🚫 Acceso Denegado</h1>
    <p>Token inválido, expirado o sesión completa (máx 10 fotos).</p>
    <p><a href="/">Vuelve a generar un QR nuevo.</a></p>
</body>
</html>
"""

HTML_SUCCESS = """
<!doctype html>
<html lang="es">
<body>
    <h1>✅ ¡Foto Enviada!</h1>
    <p>Se guardó en la carpeta input. Puedes tomar otra.</p>
</body>
</html>
"""

HTML_PAGE = """
<!doctype html>
<html lang="es">
<body>
    <h1>📸 INSTANT_ART - Photomaton Virtual</h1>
    <p>Token: {{ token }} | Fotos: {{ count }} / 10</p>
    
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="hidden" name="session_token" value="{{ token }}">
        <label for="file-upload">📸 Captura y Envía Foto (automático)</label><br><br>
        
        <input id="file-upload" type="file" name="file" accept="image/*" capture="camera" onchange="this.form.submit()">
    </form>
    <p><small>Solo imágenes. Máx 10 por sesión.</small></p>
</body>
</html>
"""

# --- CONFIGURACIÓN Y ESTRUCTURA ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'data', 'input')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
ACTIVE_TOKENS = {}  # token: count_of_uploads
SESSION_TOKEN = None

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = str(uuid.uuid4())

# --- FUNCIONES DE VALIDACIÓN ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- RUTAS ---
@app.route('/')
def index():
    return render_template_string(HTML_DENIED), 403

@app.route('/session/<token>')
def session_page(token):
    if token in ACTIVE_TOKENS:
        count = ACTIVE_TOKENS[token]
        return render_template_string(HTML_PAGE, token=token, count=count)
    else:
        print(f"🚨 Acceso denegado a /session/{token}")
        return render_template_string(HTML_DENIED), 403

@app.route('/upload', methods=['POST'])
def upload_file():
    token = request.form.get('session_token')
    print(f"📤 Upload intentado con token: {token}")
    
    if not token or token not in ACTIVE_TOKENS:
        print(f"🚨 SUBIDA RECHAZADA: Token inválido o expirado: {token}")
        return render_template_string(HTML_DENIED), 403
    
    if 'file' not in request.files:
        print("🚨 No se encontró archivo")
        return 'No se encontró archivo', 400
    
    file = request.files['file']
    if file.filename == '':
        print("🚨 Nombre de archivo vacío")
        return 'Nombre de archivo vacío', 400
        
    if not allowed_file(file.filename):
        print(f"🚨 Tipo no permitido: {file.filename}")
        return 'Tipo de archivo no permitido. Solo JPG, PNG, WEBP.', 400
        
    if file:
        original_ext = file.filename.rsplit('.', 1)[1].lower()
        safe_filename = f"{uuid.uuid4()}.{original_ext}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        file.save(save_path)
        
        # Actualizar contador
        ACTIVE_TOKENS[token] += 1
        count = ACTIVE_TOKENS[token]
        print(f"✅ FOTO #{count} RECIBIDA: {safe_filename} | Token: {token}")
        
        if count >= 10:
            del ACTIVE_TOKENS[token]
            print(f"🎉 SESIÓN COMPLETA: Token {token} invalidado (10/10 fotos).")
            # Generar nuevo token y QR automáticamente
            global SESSION_TOKEN
            SESSION_TOKEN = generate_new_session_token()
            global local_ip, port  # Para reutilizar
            new_url = f"http://{local_ip}:{port}/session/{SESSION_TOKEN}"
            generate_qr(new_url)
            return render_template_string(HTML_DENIED), 403
        
        # Redirigir para otra foto
        return redirect(url_for('session_page', token=token))

# --- FUNCIONES DE RED Y TOKENS ---
def get_ip():
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
    new_token = str(uuid.uuid4())
    ACTIVE_TOKENS[new_token] = 0
    return new_token

def generate_qr(url):
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)
    print("\n" * 2)
    print("--------------------------------------------------")
    print(f"🔗 NUEVA SESIÓN: http://{local_ip}:{port}/session/{SESSION_TOKEN}")
    print(f"📱 Escanea este QR con tu móvil (misma WiFi).")
    print("--------------------------------------------------")
    qr.print_ascii(invert=True)
    print("\n" * 2)

# --- FUNCIÓN UPnP (con try-except para no crashear) ---
def open_upnp_port(port):
    try:
        upnp = miniupnpc.UPnP()
        upnp.discoverdelay = 200
        ndiscover = upnp.discover()
        if ndiscover > 0:
            upnp.selectigd()
            result = upnp.addportmapping(port, 'TCP', upnp.lanaddr, port, 'InstantArt Server', '')
            if result == 0:  # 0 = éxito
                print(f"✅ Puerto {port} abierto vía UPnP (router).")
            else:
                print(f"⚠️ UPnP falló al mapear puerto (código {result}). Sigue sin él.")
        else:
            print("⚠️ No se detectó router UPnP. Usa firewall local.")
    except ImportError:
        print("⚠️ miniupnpc no instalado correctamente. Instala con: pip install miniupnpc")
        print("   En Windows, si falla, usa: pip install --only-binary=all miniupnpc")
    except Exception as e:
        print(f"⚠️ Error UPnP: {e}. Continuando sin él (normal en algunos setups).")

if __name__ == '__main__':
    # 1. Config puerto (cambiado a 8080 para menos bloqueos)
    port = 8080
    local_ip = get_ip()
    print(f"🌐 IP detectada: {local_ip} (verifica con ipconfig si no es 192.168.x.x)")
    
    # 2. Intentar UPnP
    open_upnp_port(port)
    
    # 3. Primer token
    SESSION_TOKEN = generate_new_session_token()
    
    # 4. URL y QR
    url = f"http://{local_ip}:{port}/session/{SESSION_TOKEN}"
    generate_qr(url)
    
    print(f"🚀 Servidor en http://{local_ip}:{port} | Máx 10 fotos por QR | Presiona Ctrl+C para parar.")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)  # Threaded para manejar múltiples requests