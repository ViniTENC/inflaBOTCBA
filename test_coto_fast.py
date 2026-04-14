import requests

def test_coto_requests():
    url = "https://www.cotodigital.com.ar/sitios/cdigi/productos/pan-lactal-blanco"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"
    }
    
    # Optional disable verify though usually not needed
    res = requests.get(url, headers=headers, timeout=10)
    print("Status:", res.status_code)
    
    html = res.text
    print("Length:", len(html))
    
    if "card-title" in html or "atg_store_newPrice" in html:
        print("Success! Price container found in raw HTML!")
    else:
        print("Price container not found in raw HTML.")
        if "Incapsula" in html or "Cloudflare" in html:
            print("WAF Blocked it.")

if __name__ == "__main__":
    test_coto_requests()
