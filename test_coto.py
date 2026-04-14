from playwright.sync_api import sync_playwright

def find_coto():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()
        url = "https://www.cotodigital.com.ar/sitios/cdigi/productos/pan-lactal-blanco"
        page.goto(url, timeout=20000)
        page.wait_for_timeout(5000)
        
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
                            const priceEl = card.querySelector('.atg_store_newPrice, h4.card-title, h4');
                            let price = null;
                            if (priceEl) {
                                let priceText_raw = priceEl.textContent;
                                let priceText = priceEl.textContent.trim().replace('$', '').replaceAll(' ', '');
                                priceText = priceText.replaceAll('.', '').replace(',', '.');
                                price = parseFloat(priceText);
                                return { nombre: name, price: price, txt_raw: priceText_raw, parsed_txt: priceText };
                            }
                        }
                    }
                    return null;
                }
        """)
        print("Resultado devuelto Coto:", producto)
        browser.close()

if __name__ == '__main__':
    find_coto()
