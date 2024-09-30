from flask import Flask, render_template, request, jsonify
import mysql.connector
import pusher

# Configurar Pusher
pusher_client = pusher.Pusher(
    app_id='YOUR_APP_ID',
    key='YOUR_APP_KEY',
    secret='YOUR_APP_SECRET',
    cluster='YOUR_CLUSTER',
    ssl=True
)

# Conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

# Ruta principal para la página de reservación
@app.route("/")
def index():
    return render_template("app.html")

# Ruta para guardar los datos de la reservación enviados desde el formulario
@app.route("/reservar", methods=["GET"])
def reservar():
    nombre = request.args.get("name")
    telefono = request.args.get("telefono")
    fecha = request.args.get("fecha")

    # Insertar en la base de datos
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "INSERT INTO reservaciones (Nombre_Apellido, Telefono, Fecha) VALUES (%s, %s, %s)"
    valores = (nombre, telefono, fecha)

    cursor.execute(sql, valores)
    con.commit()
    cursor.close()

    # Enviar evento a Pusher
    pusher_client.trigger('reservaciones-channel', 'nueva-reservacion', {
        'name': nombre,
        'telefono': telefono,
        'fecha': fecha
    })

    return f"Reservación realizada para {nombre}."

# Ruta para obtener y mostrar las reservaciones
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT id_reservacion, Nombre_Apellido, Telefono, Fecha FROM reservaciones ORDER BY id_reservacion DESC")
    registros = cursor.fetchall()
    cursor.close()

    return jsonify(registros)

if __name__ == "__main__":
    app.run(debug=True)
