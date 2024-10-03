from flask import Flask, render_template, request, jsonify
import pusher
import pytz

# Configurar Pusher con las credenciales proporcionadas
pusher_client = pusher.Pusher(
    app_id="1766032",
    key="e7b4efacf7381f83e05e",
    secret="134ff4754740b57ad585",
    cluster="us2",
    ssl=True
)

app = Flask(__name__)

# Datos en memoria para reservas (en lugar de usar una base de datos)
reservas = []
id_counter = 1

@app.route("/")
def index():
    return render_template("app.html")

# Ruta para guardar los datos de las reservas enviadas desde el formulario
@app.route("/reservar", methods=["POST"])
def reservar():
    global id_counter
    nombre = request.form["name"]
    telefono = request.form["telefono"]
    fecha = request.form["fecha"]

    # Crear nueva reserva
    nueva_reserva = {
        "id_reserva": id_counter,
        "nombre": nombre,
        "telefono": telefono,
        "fecha": fecha
    }
    id_counter += 1
    reservas.append(nueva_reserva)

    # Enviar evento a través de Pusher
    pusher_client.trigger("canalReservaciones", "nueva-reserva", nueva_reserva)

    return jsonify(nueva_reserva), 200

# Ruta para buscar las reservas (si es necesario)
@app.route("/buscar", methods=["GET"])
def buscar():
    return jsonify(reservas)

if __name__ == "__main__":
    app.run(debug=True)
