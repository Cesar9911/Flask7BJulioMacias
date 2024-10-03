from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector
import datetime
import pytz

# Configurar la conexión a MySQL
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

# Configurar Pusher
pusher_client = pusher.Pusher(
    app_id="1766032",
    key="e7b4efacf7381f83e05e",
    secret="134ff4754740b57ad585",
    cluster="us2",
    ssl=True
)

app = Flask(__name__)

@app.route("/")
def index():
    # Cerrar la conexión después de renderizar la página
    con.close()
    return render_template("app.html")

@app.route("/reservar", methods=["POST"])
def reservar():
    # Verificar si la conexión a la base de datos sigue activa, si no, reconectarla
    if not con.is_connected():
        con.reconnect()

    nombre = request.form["name"]
    telefono = request.form["telefono"]
    fecha = request.form["fecha"]

    # Insertar los datos en la base de datos
    cursor = con.cursor()
    sql = "INSERT INTO reservas (Nombre_Apellido, Telefono, Fecha) VALUES (%s, %s, %s)"
    val = (nombre, telefono, fecha)
    cursor.execute(sql, val)
    con.commit()

    # Obtener el ID de la reserva recién insertada
    id_reserva = cursor.lastrowid
    cursor.close()

    # Crear nueva reserva para enviarla a Pusher
    nueva_reserva = {
        "id_reserva": id_reserva,
        "nombre": nombre,
        "telefono": telefono,
        "fecha": fecha
    }

    # Enviar evento a través de Pusher
    pusher_client.trigger("canalReservaciones", "nueva-reserva", nueva_reserva)

    # Cerrar la conexión después de las operaciones
    con.close()

    return jsonify(nueva_reserva), 200

# Ruta para buscar todas las reservas desde la base de datos
@app.route("/buscar", methods=["GET"])
def buscar():
    # Verificar si la conexión a la base de datos sigue activa, si no, reconectarla
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT id_reserva, Nombre_Apellido, Telefono, Fecha FROM reservas")
    reservas = cursor.fetchall()
    cursor.close()

    # Transformar los datos en un formato adecuado para JSON
    resultado = []
    for reserva in reservas:
        resultado.append({
            "id_reserva": reserva[0],
            "nombre": reserva[1],
            "telefono": reserva[2],
            "fecha": reserva[3]
        })

    # Cerrar la conexión después de las operaciones
    con.close()

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
