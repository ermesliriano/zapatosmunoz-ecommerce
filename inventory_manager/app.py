from flask import Flask
import sqlite3
from shared.kafka_utils import create_consumer
from shared.event_schema import InventarioActualizado
import jsonschema

app = Flask(__name__)

consumer = create_consumer('InventarioActualizado')

def handle_inventario_actualizado(inventario):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    productos = inventario['productosActualizados']
    for producto in productos:
        producto_id = producto['productoId']
        cantidad = producto['cantidadActual']
        cursor.execute("UPDATE inventario SET cantidad = ? WHERE producto_id = ?", (cantidad, producto_id))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return "Inventory Manager"

if __name__ == '__main__':
    for message in consumer:
        inventario = message.value
        jsonschema.validate(instance=inventario, schema=InventarioActualizado)
        handle_inventario_actualizado(inventario)
    app.run(host='0.0.0.0', port=5002)
