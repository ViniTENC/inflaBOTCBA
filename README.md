# 🛒 Inflación CBA (Canasta Básica Alimentaria)

Este proyecto es un **Dashboard Comparador de Precios y Scraper** diseñado para monitorear mensualmente el costo exacto de la Canasta Básica Alimentaria (CBA) de Argentina, tal como la define el INDEC. 

Compara automáticamente los precios entre los principales supermercados del país (**Carrefour y Jumbo**) ajustando matemáticamente cada precio a las cantidades en gramos/litros requeridas por las normativas oficiales para medir el índice de inflación real en góndola.

---

## 🚀 Características Principales

* **Scraping Multi-Supermercado en Vivo:**
  - **Carrefour y Jumbo:** Escaneo instantáneo y silencioso mediante sus APIs internas (VTEX) paginadas.
* **Matemática INDEC Estricta:** Gracias al archivo `canasta_basica.json`, no suma "1 pan". Multiplica algorítmicamente el precio de mercado para cumplir la cuota mensual exacta de 6.75 kg de pan, y así con los 30 rubros de la lista oficial.
* **Dashboard Histórico:** Interfaz gráfica web estéticamente agradable con gráficos interactivos (`Chart.js`) para ver cómo evoluciona la inflación a lo largo de los meses.
* **Persistencia Local:** Los resultados de cada mes guardan un Snapshot histórico inmutable en una base de datos local rápida (`precios.db` vía SQLite).

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python + Flask (Servidor Web) + SQLite (Base de datos).
* **Concurrencia y Log en Vivo:** `Flask-SocketIO` y `Threading` para retransmitir los logs de scraping azules directamente al navegador en tiempo real.
* **Scraping:** `Requests` (Para VTEX público).
* **Frontend:** HTML5 + CSS Vanilla (Sleek UI) + Chart.js.

---

## ⚙️ Instalación y Uso

1. Cloná o descargá el repositorio a tu computadora.
2. Es sumamente recomendable usar un entorno virtual (`python -m venv venv` y `source venv/bin/activate`).
3. Instalá los requerimientos esenciales:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
4. Corré el servidor web:
   ```bash
   python app.py
   ```
5. Accedé desde tu navegador a `http://127.0.0.1:8080`.
6. Presioná **"Actualizar Precios Ahora"**, sentate a disfrutar viendo cómo se arma automáticamente la tabla.

---

## 📝 Personalización

Si en algún momento el INDEC cambia las proporciones, o se desea agregar un supermercado nuevo:
- **`canasta_basica.json`:** Se pueden ajustar los multiplicadores de cantidad, o modificar los "slugs" y términos de búsqueda si un supermercado deja de vender una marca específica.
- **Carpeta `scrapers/`:** Su arquitectura orientada a objetos (`BaseScraper`) permite agregar fácilmente un `DiaScraper.py` o similares copiando la plantilla.
