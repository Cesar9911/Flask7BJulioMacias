from flask import Flask, render_template, request
import pusher
import mysql.connector
import pytz

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
@app.route("/reservar", methods=["POST"])
def reservar():
    nombre = request.form["name"]
    checkin = request.form["checkin"]
    checkout = request.form["checkout"]
    room_type = request.form["room_type"]
    comentario = request.form["comment"]

    # Insertar en la base de datos
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "INSERT INTO reservaciones (Nombre_Apellido, Fecha_Entrada, Fecha_Salida, Tipo_Habitacion, Comentario) VALUES (%s, %s, %s, %s, %s)"
    valores = (nombre, checkin, checkout, room_type, comentario)

    cursor.execute(sql, valores)
    con.commit()

    cursor.close()

    return f"Reservación realizada para {nombre}."

# Ruta para obtener y mostrar las reservaciones
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM reservaciones ORDER BY id_reservacion DESC")
    registros = cursor.fetchall()
    con.close()

    return registros

if __name__ == "__main__":
    app.run(debug=True)
