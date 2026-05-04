import os
import threading
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

from canasta import cargar_productos_canasta, guardar_snapshot, obtener_historial_mensual, obtener_ultimo_snapshot
from scrapers import CarrefourScraper, JumboScraper

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "inflacion-cba-secret-2024")
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template("canasta.html")

@app.route("/api/canasta/productos")
def api_canasta_productos():
    return jsonify(cargar_productos_canasta())

@app.route("/api/canasta/ultimo")
def api_canasta_ultimo():
    return jsonify(obtener_ultimo_snapshot() or {})

@app.route("/api/canasta/historial")
def api_canasta_historial():
    return jsonify(obtener_historial_mensual())

def run_scraping_canasta(sid):
    def log(msg, level="info"):
        socketio.emit("canasta_log", {"msg": msg, "level": level}, to=sid)

    productos = cargar_productos_canasta()
    carrefour = CarrefourScraper()
    jumbo = JumboScraper()

    resultados = []

    for i, prod in enumerate(productos):
        nombre = prod["nombre"]
        term = prod["termino_busqueda"]
        mult = prod.get("multiplicador", 1.0)

        log(f"[{i+1}/{len(productos)}] Buscando {nombre}...")

        # Carrefour
        res_carrefour = carrefour.scrape_product(prod["id"], term)
        if res_carrefour and res_carrefour["precio"]:
            res_carrefour["precio"] = res_carrefour["precio"] * mult
            resultados.append(res_carrefour)

        # Jumbo
        res_jumbo = jumbo.scrape_product(prod["id"], term)
        if res_jumbo and res_jumbo["precio"]:
            res_jumbo["precio"] = res_jumbo["precio"] * mult
            resultados.append(res_jumbo)

    # Guardar en DB
    if resultados:
        guardar_snapshot(resultados)
        log("✅ Scraping finalizado y guardado en historial.", "success")
    else:
        log("⚠️ No se encontraron resultados.", "warn")

    socketio.emit("canasta_done", to=sid)

@app.route("/api/canasta/scrape", methods=["POST"])
def api_canasta_scrape():
    data = request.json
    sid = data.get("sid", "")
    t = threading.Thread(
        target=run_scraping_canasta,
        args=(sid,),
        daemon=True,
    )
    t.start()
    return jsonify({"ok": True})

if __name__ == "__main__":
    socketio.run(app, debug=True, host="127.0.0.1", port=8080)
