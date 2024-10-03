from flask import Flask, request, jsonify
import pusher

app = Flask(__name__)

# Configura Pusher con tus credenciales
pusher_client = pusher.Pusher(
    app_id='YOUR_APP_ID',
    key='YOUR_KEY',
    secret='YOUR_SECRET',
    cluster='YOUR_CLUSTER',
    ssl=True
)

# Datos en memoria para reservas (puedes usar una base de datos si prefieres)
reservas = []
id_counter = 1

@app.route('/reservar', methods=['POST'])
def reservar():
    global id_counter
    nombre = request.form['name']
    telefono = request.form['telefono']
    fecha = request.form['fecha']
    
    # Crear nueva reserva
    nueva_reserva = {
        'id_reserva': id_counter,
        'nombre': nombre,
        'telefono': telefono,
        'fecha': fecha
    }
    id_counter += 1
    reservas.append(nueva_reserva)

    # Enviar evento a Pusher para notificar a los clientes
    pusher_client.trigger('reservaciones-channel', 'nueva-reserva', nueva_reserva)

    return 'Reservación registrada correctamente', 200

@app.route('/buscar', methods=['GET'])
def buscar():
    return jsonify(reservas)

if __name__ == '__main__':
    app.run(debug=True)
