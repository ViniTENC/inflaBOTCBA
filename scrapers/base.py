class BaseScraper:
    def __init__(self):
        self.supermercado = "Base"

    def scrape_product(self, product_id, termino_busqueda, playwright_context=None):
        """
        Debe devolver un dict con:
        {
            "supermercado": self.supermercado,
            "producto_id": product_id,
            "precio": float | None,
            "descripcion": str,
            "url": str
        }
        """
        raise NotImplementedError()
