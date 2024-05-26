from flask import Flask, request, jsonify
from shared.kafka_utils import create_producer

app = Flask(__name__)
producer = create_producer()

@app.route('/pedido', methods=['POST'])
def crear_pedido():
    pedido = request.json
    producer.send('PedidoCreado', pedido)
    return jsonify({"message": "Pedido recibido"}), 201

@app.route('/notificacion', methods=['POST'])
def recibir_notificacion():
    notificacion = request.json
    # Aquí puedes manejar la notificación como sea necesario
    return jsonify({"message": "Notificación recibida"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
