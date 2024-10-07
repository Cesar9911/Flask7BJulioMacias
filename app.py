from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
import pusher
import datetime
import pytz

# Conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

# Configuración de Pusher
pusher_client = pusher.Pusher(
    app_id="1875540",
    key="73801e00502db5454777",
    secret="01c9f9b70103cf9e823a",
    cluster="us2",
    ssl=True
)

# Página principal que carga el CRUD de reservaciones
@app.route("/")
def index():
    con.close()
    return render_template("app.html")

# Crear o actualizar una reservación
@app.route("/reservas/guardar", methods=["POST"])
def guardar_reserva():
    if not con.is_connected():
        con.reconnect()

    id_reserva = request.form.get("id_reserva")
    nombre_completo = request.form["nombre_completo"]
    telefono = request.form["telefono"]
    fecha = request.form["fecha"]

    cursor = con.cursor()
    if id_reserva:  # Actualizar
        sql = """
        UPDATE tst0_reservas SET Nombre_Completo = %s, Telefono = %s, Fecha = %s WHERE Id_Reserva = %s
        """
        val = (nombre_completo, telefono, fecha, id_reserva)
    else:  # Crear nueva reservación
        sql = """
        INSERT INTO tst0_reservas (Nombre_Completo, Telefono, Fecha) VALUES (%s, %s, %s)
        """
        val = (nombre_completo, telefono, fecha)

    cursor.execute(sql, val)
    con.commit()
    cursor.close()
    con.close()

    notificar_actualizacion_reservas()

    return make_response(jsonify({"message": "Reserva guardada exitosamente"}))

# Obtener todas las reservas
@app.route("/reservas", methods=["GET"])
def obtener_reservas():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tst0_reservas")
    reservas = cursor.fetchall()
    cursor.close()
    con.close()

    return make_response(jsonify(reservas))

# Obtener una reserva por su ID
@app.route("/reservas/editar", methods=["GET"])
def editar_reserva():
    if not con.is_connected():
        con.reconnect()

    id_reserva = request.args.get("id")
    cursor = con.cursor(dictionary=True)
    sql = "SELECT * FROM tst0_reservas WHERE Id_Reserva = %s"
    val = (id_reserva,)
    cursor.execute(sql, val)
    reserva = cursor.fetchone()
    cursor.close()
    con.close()

    return make_response(jsonify(reserva))

# Eliminar una reserva
@app.route("/reservas/eliminar", methods=["POST"])
def eliminar_reserva():
    if not con.is_connected():
        con.reconnect()

    id_reserva = request.form["id"]
    cursor = con.cursor()
    sql = "DELETE FROM tst0_reservas WHERE Id_Reserva = %s"
    val = (id_reserva,)
    cursor.execute(sql, val)
    con.commit()
    cursor.close()
    con.close()

    notificar_actualizacion_reservas()

    return make_response(jsonify({"message": "Reserva eliminada exitosamente"}))

# Notificar a través de Pusher sobre actualizaciones en la tabla de reservaciones
def notificar_actualizacion_reservas():
    pusher_client.trigger("canalReservas", "actualizacion", {})

if __name__ == "__main__":
    app.run(debug=True)
