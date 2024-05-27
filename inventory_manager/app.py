from flask import Flask, jsonify
import sqlite3
from shared.kafka_utils import create_consumer
from shared.event_schema import InventarioActualizado
import jsonschema
import threading

app = Flask(__name__)

consumer = create_consumer('InventarioActualizado')

def handle_inventario_actualizado(inventario):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    productos = inventario['productosActualizados']
    for producto in productos:
        producto_id = producto['productoId']
        cantidad = producto['cantidadActual']  # Verifica que esta clave sea correcta
        cursor.execute("UPDATE inventario SET cantidad = ? WHERE producto_id = ?", (cantidad, producto_id))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return "Inventory Manager"

@app.route('/inventario', methods=['GET'])
def get_inventario():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventario")
    inventario = cursor.fetchall()
    conn.close()
    return jsonify(inventario)

def consume_inventarios():
    for message in consumer:
        inventario = message.value
        jsonschema.validate(instance=inventario, schema=InventarioActualizado)
        handle_inventario_actualizado(inventario)

if __name__ == '__main__':
    threading.Thread(target=consume_inventarios).start()
    app.run(host='0.0.0.0', port=5002)
