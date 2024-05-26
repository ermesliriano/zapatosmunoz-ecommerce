import sqlite3

conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE inventario (
    producto_id TEXT PRIMARY KEY,
    cantidad INTEGER NOT NULL
)
''')
cursor.execute("INSERT INTO inventario (producto_id, cantidad) VALUES ('P001', 10)")
cursor.execute("INSERT INTO inventario (producto_id, cantidad) VALUES ('P002', 10)")
conn.commit()
conn.close()
