import json
import sqlite3
import os
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(__file__), "precios.db")
JSON_FILE = os.path.join(os.path.dirname(__file__), "canasta_basica.json")

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = dict_factory
    return conn

def crear_tablas():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS precios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id INTEGER NOT NULL,
            supermercado TEXT NOT NULL,
            producto_id TEXT NOT NULL,
            precio REAL,
            descripcion TEXT,
            url TEXT,
            FOREIGN KEY (snapshot_id) REFERENCES snapshots(id)
        )
    ''')
    conn.commit()
    conn.close()

def cargar_productos_canasta():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_snapshot(resultados):
    conn = get_db()
    c = conn.cursor()
    hoy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute("INSERT INTO snapshots (fecha) VALUES (?)", (hoy,))
    snapshot_id = c.lastrowid
    
    for r in resultados:
        c.execute('''
            INSERT INTO precios (snapshot_id, supermercado, producto_id, precio, descripcion, url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (snapshot_id, r["supermercado"], r["producto_id"], r["precio"], r["descripcion"], r["url"]))
        
    conn.commit()
    conn.close()
    return snapshot_id

def obtener_ultimo_snapshot():
    conn = get_db()
    c = conn.cursor()
    
    c.execute("SELECT id, fecha FROM snapshots ORDER BY id DESC LIMIT 1")
    snap = c.fetchone()
    if not snap:
        conn.close()
        return None
        
    c.execute('''
        SELECT p.* 
        FROM precios p
        WHERE p.snapshot_id = ?
    ''', (snap["id"],))
    precios = c.fetchall()
    
    conn.close()
    return {"id": snap["id"], "fecha": snap["fecha"], "precios": precios}

def obtener_historial_mensual():
    """
    Obtiene todos los snapshots y sus precios para graficar en el tiempo.
    """
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''
        SELECT s.id, s.fecha, p.supermercado, sum(p.precio) as total
        FROM snapshots s
        JOIN precios p ON s.id = p.snapshot_id
        GROUP BY s.id, p.supermercado
        ORDER BY s.fecha ASC
    ''')
    historial = c.fetchall()
    conn.close()
    
    # Organizar por fecha -> supermercado -> total
    result = {}
    for r in historial:
        fecha = r["fecha"].split(" ")[0] # solo la fecha, sin la hora para agrupar simple
        if fecha not in result:
            result[fecha] = {}
        result[fecha][r["supermercado"]] = r["total"]
        
    return result

# Inicializar DB la primera vez que se importa
crear_tablas()
