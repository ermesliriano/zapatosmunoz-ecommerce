from flask import Flask
import sqlite3
from shared.kafka_utils import create_consumer, create_producer
from shared.event_schema import PedidoCreado, InventarioActualizado
import jsonschema
import threading
import datetime

app = Flask(__name__)

producer = create_producer()
consumer = create_consumer('PedidoCreado')

def handle_pedido_creado(pedido):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    productos = pedido['productos']
    for producto in productos:
        producto_id = producto['productoId']
        cantidad = producto['cantidad']
        cursor.execute("INSERT INTO pedidos (producto_id, cantidad) VALUES (?, ?)", (producto_id, cantidad))
    conn.commit()
    conn.close()
    actualizar_inventario(productos)

def actualizar_inventario(productos):
    productos_actualizados = []
    for producto in productos:
        productos_actualizados.append({
            "productoId": producto["productoId"],
            "cantidadActual": producto["cantidad"]  # Asegúrate de usar la clave correcta aquí
        })

    inventario_actualizado = {
        "fechaActualizacion": datetime.datetime.now().isoformat(),
        "productosActualizados": productos_actualizados
    }
    producer.send('InventarioActualizado', inventario_actualizado)

@app.route('/')
def index():
    return "Order Manager"

def consume_pedidos():
    for message in consumer:
        pedido = message.value
        jsonschema.validate(instance=pedido, schema=PedidoCreado)
        handle_pedido_creado(pedido)

if __name__ == '__main__':
    threading.Thread(target=consume_pedidos).start()
    app.run(host='0.0.0.0', port=5001)
