from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Aquí iría la lógica de autenticación
        return redirect(url_for('dashboard'))  # Simulación
    return render_template('login.html')

# Ruta de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Aquí iría la lógica para registrar usuarios
        return redirect(url_for('login'))  # Simulación
    return render_template('registro.html')

# Ruta del dashboard simulado
@app.route('/dashboard')
def dashboard():
    return "<h2>Bienvenido al Dashboard (simulado)</h2><a href='/'>Volver al inicio</a>"

if __name__ == '__main__':
    app.run(debug=True)
