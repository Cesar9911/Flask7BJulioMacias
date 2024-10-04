from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector

# Conectar a la base de datos
def connect_db():
    return mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )

con = connect_db()

app = Flask(__name__)

# Conexión con Pusher
pusher_client = pusher.Pusher(
    app_id="1875540",
    key="73801e00502db5454777",
    secret="01c9f9b70103cf9e823a",
    cluster="us2",
    ssl=True  # Activar SSL para conexión segura
)

# Ruta principal que sirve una página de inicio
@app.route("/")
def index():
    return render_template("app.html")

# Ruta para guardar los datos enviados desde el formulario
@app.route("/app/guardar", methods=["POST"])
def guardar():
    nombre_apellido = request.form.get("nombreapellido")
    telefono = request.form.get("telefono")
    fecha = request.form.get("fecha")

    if not nombre_apellido or not telefono or not fecha:
        return "Faltan datos requeridos.", 400  # Devuelve un error 400 si faltan datos

    # Verificar si la conexión sigue activa
    if not con.is_connected():
        con.reconnect()

    try:
        cursor = con.cursor()
        sql = "INSERT INTO tst0_reservas (Nombre_Apellido, Telefono, Fecha) VALUES (%s, %s, %s)"
        val = (nombre_apellido, telefono, fecha)
        
        cursor.execute(sql, val)
        con.commit()
        cursor.close()

        # Disparar un evento a través de Pusher
        try:
            pusher_client.trigger("canalRegistroEncuesta", "registroEventoEncuests", {
                "nombreapellido": nombre_apellido,
                "telefono": telefono,
                "fecha": fecha
            })
        except Exception as pusher_error:
            return f"Error al enviar el evento a Pusher: {pusher_error}", 500

        return "Datos guardados correctamente.", 200

    except mysql.connector.Error as err:
        return f"Error en la base de datos: {err}", 500  # Devuelve un error 500 si hay un problema en la BD

# Ruta para buscar y mostrar los registros
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM tst0_experiencias ORDER BY Id_Experiencia DESC")
        registros = cursor.fetchall()
        cursor.close()

        # Devolver los registros como un JSON
        return jsonify(registros), 200

    except mysql.connector.Error as err:
        return f"Error al buscar registros: {err}", 500  # Devuelve un error 500 si hay un problema

if __name__ == "__main__":
    app.run(debug=True)
