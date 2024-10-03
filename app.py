from flask import Flask, render_template, request
import pusher
import mysql.connector

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
    nombre_apellido = request.form["nombreapellido"]
    telefono = request.form["telefono"]
    fecha = request.form["fecha"]

    # Conectar a la base de datos y guardar los datos
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "INSERT INTO tst0_experiencias (Nombre_Apellido, Telefono, Fecha) VALUES (%s, %s, %s)"
    val = (nombre_apellido, telefono, fecha)
    
    cursor.execute(sql, val)
    con.commit()
    cursor.close()

    # Conexión con Pusher
    pusher_client = pusher.Pusher(
        app_id="1766032",
        key="e7b4efacf7381f83e05e",
        secret="134ff4754740b57ad585",
        cluster="us2",
        ssl=True
    )
    
    # Disparando un evento a través de Pusher
    pusher_client.trigger("canalRegistroEncuesta", "registroEventoEncuests", {
        "nombreapellido": nombre_apellido,
        "telefono": telefono,
        "fecha": fecha
    })

    return "Datos guardados correctamente."

# Ruta para buscar y mostrar los registros
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_experiencias ORDER BY Id_Experiencia DESC")
    registros = cursor.fetchall()
    con.close()
    
    return registros

if __name__ == "__main__":
    app.run(debug=True)
