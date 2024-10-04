from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector

# Configuración de la conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

# Ruta para el index
@app.route("/")
def index():
    return render_template("app.html")

# Función para obtener todas las reservas
@app.route("/reservas")
def obtener_reservas():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tst0_reservas")
    reservas = cursor.fetchall()
    con.close()

    return make_response(jsonify(reservas))

# Función para agregar o editar reservas
@app.route("/reservas/guardar", methods=["POST"])
def guardar_reserva():
    if not con.is_connected():
        con.reconnect()

    id_reserva = request.form.get("id_reserva")
    nombre_apellido = request.form["nombre_apellido"]
    telefono = request.form["telefono"]
    fecha = request.form["fecha"]

    cursor = con.cursor()

    if id_reserva:
        # Si se proporciona id_reserva, entonces es una actualización
        sql = """
        UPDATE tst0_reservas SET
        Nombre_Apellido = %s,
        Telefono = %s,
        Fecha = %s
        WHERE Id_Reserva = %s
        """
        val = (nombre_apellido, telefono, fecha, id_reserva)
    else:
        # Si no hay id_reserva, entonces es una inserción
        sql = """
        INSERT INTO tst0_reservas (Nombre_Apellido, Telefono, Fecha)
        VALUES (%s, %s, %s)
        """
        val = (nombre_apellido, telefono, fecha)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({"status": "success"}))

# Función para obtener los datos de una reserva específica
@app.route("/reservas/editar", methods=["GET"])
def editar_reserva():
    if not con.is_connected():
        con.reconnect()

    id_reserva = request.args.get("id_reserva")
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tst0_reservas WHERE Id_Reserva = %s", (id_reserva,))
    reserva = cursor.fetchone()
    con.close()

    return make_response(jsonify(reserva))

# Función para eliminar una reserva
@app.route("/reservas/eliminar", methods=["POST"])
def eliminar_reserva():
    if not con.is_connected():
        con.reconnect()

    id_reserva = request.form["id_reserva"]
    cursor = con.cursor()
    cursor.execute("DELETE FROM tst0_reservas WHERE Id_Reserva = %s", (id_reserva,))
    con.commit()
    con.close()

    return make_response(jsonify({"status": "success"}))

if __name__ == "__main__":
    app.run(debug=True)
