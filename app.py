from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector
import logging

# Habilitar logging para revisar los errores
logging.basicConfig(level=logging.DEBUG)

# Función para crear conexión a la base de datos
def get_db_connection():
    try:
        con = mysql.connector.connect(
            host="185.232.14.52",
            database="u760464709_tst_sep",
            user="u760464709_tst_sep_usr",
            password="dJ0CIAFF="
        )
        return con
    except mysql.connector.Error as err:
        logging.error(f"Error al conectar a la base de datos: {err}")
        return None

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

    con = get_db_connection()
    if con is None:
        return "Error al conectar a la base de datos.", 500

    try:
        cursor = con.cursor()
        sql = "INSERT INTO tst0_reservas (Nombre_Apellido, Telefono, Fecha) VALUES (%s, %s, %s)"
        val = (nombre_apellido, telefono, fecha)
        
        cursor.execute(sql, val)
        con.commit()
        cursor.close()

        # Disparar un evento a través de Pusher
        pusher_client.trigger("canalRegistroEncuesta", "registroEventoEncuests", {
            "nombreapellido": nombre_apellido,
            "telefono": telefono,
            "fecha": fecha
        })

        return "Datos guardados correctamente.", 200

    except mysql.connector.Error as err:
        logging.error(f"Error en la base de datos: {err}")
        return f"Error en la base de datos: {err}", 500

    finally:
        con.close()

# Ruta para buscar y mostrar los registros
@app.route("/buscar")
def buscar():
    con = get_db_connection()
    if con is None:
        return "Error al conectar a la base de datos.", 500

    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM tst0_experiencias ORDER BY Id_Experiencia DESC")
        registros = cursor.fetchall()
        cursor.close()

        # Devolver los registros como un JSON
        return jsonify(registros), 200

    except mysql.connector.Error as err:
        logging.error(f"Error al buscar registros: {err}")
        return f"Error al buscar registros: {err}", 500

    finally:
        con.close()

if __name__ == "__main__":
    app.run(debug=True)
