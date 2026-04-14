import requests
import urllib.parse
import json

headers = {"User-Agent": "Mozilla/5.0"}
terminos = ["Pan lactal", "Arroz"]

for t in terminos:
    url = f"https://www.carrefour.com.ar/api/catalog_system/pub/products/search/?ft={urllib.parse.quote(t)}"
    res = requests.get(url, headers=headers)
    print(url)
    if res.status_code in (200, 206):
        data = res.json()
        print(f"[{t}] {len(data)}")
        if len(data) > 0:
            print("  -> First item:", data[0].get("productName"))
    else:
        print("Error", res.status_code)
