import re
import unicodedata
from .base import BaseScraper

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", " ", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text

class CotoScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.supermercado = "Coto"

    def scrape_product(self, product_id, termino_busqueda, page=None):
        if not page:
            raise ValueError("CotoScraper requiere una 'page' de Playwright")
            
        try:
            # Filtrar palabras que sean unidades musculares (500g, 1kg, etc) antes del slug
            palabras = [w for w in termino_busqueda.split() if not re.match(r"^(\d+\w*|x|kg|gr|g|ml|l|lt|un|paq|bsa|cja)$", w, re.I)][:4]
            term_corto = " ".join(palabras)
            slug = slugify(term_corto)
            search_url = f"https://www.cotodigital.com.ar/sitios/cdigi/productos/{slug}"
            
            page.goto(search_url, timeout=15000)
            try:
                page.wait_for_load_state("networkidle", timeout=8000)
                page.wait_for_selector("h3, .nombre-producto", timeout=5000)
            except Exception:
                pass
            
            producto = page.evaluate("""
                () => {
                    const h3s = document.querySelectorAll('h3.nombre-producto, h3');
                    for (const h3 of h3s) {
                        const name = h3.textContent.trim();
                        if (name.length < 3) continue;
                        
                        let el = h3;
                        let card = null;
                        for (let i = 0; i < 6; i++) {
                            el = el.parentElement;
                            if (!el) break;
                            if (el.classList.contains('centro-precios') || el.classList.contains('product_info_container') || el.querySelector('button')) {
                                card = el;
                                break;
                            }
                        }
                        
                        if (card) {
                            const priceEl = card.querySelector('.atg_store_newPrice, h4.card-title');
                            let price = null;
                            if (priceEl && priceEl.textContent.includes('$')) {
                                let priceText = priceEl.textContent.trim().split('$')[1];
                                priceText = priceText.trim().split(' ')[0];
                                priceText = priceText.replaceAll('.', '').replace(',', '.');
                                price = parseFloat(priceText);
                            }
                            
                            let linkEl = card.querySelector('a[href*="/productos/"]');
                            let href = linkEl ? linkEl.href : window.location.href;
                            // En la nueva SPA a veces el a tag está arriba
                            if (!linkEl && card.parentElement && card.parentElement.querySelector('a')) {
                                href = card.parentElement.querySelector('a').href;
                            }
                            
                            if (price && !isNaN(price)) {
                                return { nombre: name, price: price, href: href };
                            }
                        }
                    }
                    return null;
                }
            """)
            
            if producto:
                return {
                    "supermercado": self.supermercado,
                    "producto_id": product_id,
                    "precio": producto["price"],
                    "descripcion": producto["nombre"],
                    "url": producto["href"]
                }
            
            return None
            
        except Exception as e:
            print(f"[CotoScraper] Error buscando {termino_busqueda}: {e}")
            return None
