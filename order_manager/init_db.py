import sqlite3

conn = sqlite3.connect('orders.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id TEXT NOT NULL,
    cantidad INTEGER NOT NULL
)
''')
conn.commit()
conn.close()
