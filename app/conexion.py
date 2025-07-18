import pymysql

def obtener_conexion():
    return pymysql.connect(
        host='localhost',
        port=3307,  # Asegúrate de que este puerto sea el correcto
        user='root',               # o el usuario que uses
        password='SENA',               # tu contraseña de MySQL
        db='hoteles',         # nombre de tu base de datos
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
