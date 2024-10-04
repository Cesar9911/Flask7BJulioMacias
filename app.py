from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector

# Conectar a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

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

    # Conectar a la base de datos y guardar los datos
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "INSERT INTO tst0_reservas (Nombre_Apellido, Telefono, Fecha) VALUES (%s, %s, %s)"
    val = (nombre_apellido, telefono, fecha)
    
    cursor.execute(sql, val)
    con.commit()
    cursor.close()

    # Conexión con Pusher
    pusher_client = pusher.Pusher(
    app_id = "1875540"
key = "73801e00502db5454777"
secret = "01c9f9b70103cf9e823a"
cluster = "us2"
    )
    
    # Disparando un evento a través de Pusher
    pusher_client.trigger("canalRegistroEncuesta", "registroEventoEncuests", {
        "nombreapellido": nombre_apellido,
        "telefono": telefono,
        "fecha": fecha
    })

    return "Datos guardados correctamente.", 200  # Devuelve un código 200 para indicar éxito

# Ruta para buscar y mostrar los registros
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
        
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_experiencias ORDER BY Id_Experiencia DESC")
    registros = cursor.fetchall()
    cursor.close()  # Cierra el cursor aquí
    
    # Devuelve los registros como un JSON
    return jsonify(registros)

if __name__ == "__main__":
    app.run(debug=True)
