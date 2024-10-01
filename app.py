from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Lista para almacenar reservaciones en memoria
reservaciones = []
contador_id = 1  # Contador para generar ID de reserva

# Ruta principal para la página de reservación
@app.route("/")
def index():
    return render_template("app.html")

# Ruta para guardar los datos de la reservación enviados desde el formulario
@app.route("/reservar", methods=["POST"])
def reservar():
    global contador_id
    nombre = request.form["name"]
    telefono = request.form["telefono"]
    fecha = request.form["fecha"]

    # Crear una nueva reservación con ID autoincremental
    nueva_reserva = {
        "id_reserva": contador_id,
        "nombre": nombre,
        "telefono": telefono,
        "fecha": fecha
    }
    reservaciones.append(nueva_reserva)  # Añadir reservación a la lista
    contador_id += 1  # Incrementar el contador de ID

    return f"Reservación realizada para {nombre}."

# Ruta para obtener y mostrar las reservaciones
@app.route("/buscar")
def buscar():
    return jsonify(reservaciones)  # Retornar las reservaciones como JSON

if __name__ == "__main__":
    app.run(debug=True)
