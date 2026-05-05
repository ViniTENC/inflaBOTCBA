import requests
from .base import BaseScraper
import urllib.parse

class JumboScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.supermercado = "Jumbo"
        self.api_url = "https://www.jumbo.com.ar/api/catalog_system/pub/products/search/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Origin": "https://www.jumbo.com.ar",
            "Referer": "https://www.jumbo.com.ar/"
        }

    def scrape_product(self, product_id, termino_busqueda, playwright_context=None):
        query = urllib.parse.quote(termino_busqueda)
        url = f"{self.api_url}?ft={query}"
        
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code in (200, 206):
                data = resp.json()
                if data and len(data) > 0:
                    item = data[0]
                    try:
                        nombre = item["productName"]
                        link = item["link"]
                        precio = item["items"][0]["sellers"][0]["commertialOffer"]["Price"]
                        
                        return {
                            "supermercado": self.supermercado,
                            "producto_id": product_id,
                            "precio": float(precio) if precio else None,
                            "descripcion": nombre,
                            "url": link
                        }
                    except (KeyError, IndexError) as e:
                        print(f"[JumboScraper] Estructura JSON no esperada: {e}")
                        
        except Exception as e:
            print(f"[JumboScraper] Error buscando {termino_busqueda}: {e}")
            
        return None
