from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="SENA",
    database="hoteles",
)
cursor = db.cursor()

# Función auxiliar para categorías
def obtener_id_categoria(nombre_categoria):
    cursor.execute("SELECT id FROM categorias WHERE nombre = %s", (nombre_categoria,))
    categoria = cursor.fetchone()
    if categoria:
        return categoria[0]
    else:
        cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre_categoria,))
        db.commit()
        return cursor.lastrowid

# Ruta index
@app.route('/')
def index():
    return render_template('index.html')

# Ruta login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        cursor.execute("SELECT * FROM usuarios WHERE correo=%s AND password=%s", (correo, password))
        user = cursor.fetchone()
        if user:
            return redirect(url_for('dashboard'))
    return render_template('login.html')

# Ruta registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['password']
        cursor.execute("INSERT INTO usuarios (nombre, correo, password) VALUES (%s, %s, %s)", (nombre, correo, password))
        db.commit()
        return redirect(url_for('login'))
    return render_template('registro.html')

# Ruta dashboard
@app.route('/dashboard')
def dashboard():
    cursor.execute("""
        SELECT h.id, h.nombre, c.nombre AS categoria, h.direccion, h.telefono, h.anio_apertura AS anio
        FROM hoteles h
        JOIN categorias c ON h.categoria_id = c.id
    """)
    hoteles = cursor.fetchall()

    hoteles_dict = []
    for h in hoteles:
        hoteles_dict.append({
            'id': h[0],
            'nombre': h[1],
            'categoria': h[2],
            'direccion': h[3],
            'telefono': h[4],
            'anio': h[5]
        })

    return render_template('hoteles.html', hoteles=hoteles_dict)

# Ruta para guardar hotel
@app.route('/guardar_hotel', methods=['POST'])
def guardar_hotel():
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    anio = request.form['anio']

    categoria_id = obtener_id_categoria(categoria)

    cursor.execute("""
        INSERT INTO hoteles (nombre, direccion, telefono, anio_apertura, categoria_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, direccion, telefono, anio, categoria_id))
    db.commit()

    return redirect(url_for('dashboard'))



# Ruta para mostrar el formulario de edición de un hotel
@app.route('/editar_hotel/<int:id>', methods=['GET'])
def editar_hotel(id):
    cursor.execute("""
        SELECT h.id, h.nombre, c.nombre AS categoria, h.direccion, h.telefono, h.anio_apertura
        FROM hoteles h
        JOIN categorias c ON h.categoria_id = c.id
        WHERE h.id = %s
    """, (id,))
    hotel = cursor.fetchone()

    if not hotel:
        return "Hotel no encontrado", 404

    hotel_dict = {
        'id': hotel[0],
        'nombre': hotel[1],
        'categoria': hotel[2],
        'direccion': hotel[3],
        'telefono': hotel[4],
        'anio': hotel[5]
    }

    return render_template('editar_hotel.html', hotel=hotel_dict)

@app.route('/actualizar_hotel/<int:id>', methods=['POST'])
def actualizar_hotel(id):
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    anio = request.form['anio']
    categoria_id = obtener_id_categoria(categoria)

    cursor.execute("""
        UPDATE hoteles
        SET nombre = %s, direccion = %s, telefono = %s, anio_apertura = %s, categoria_id = %s
        WHERE id = %s
    """, (nombre, direccion, telefono, anio, categoria_id, id))
    db.commit()

    return redirect(url_for('dashboard'))


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)