import httpx
import json
from pathlib import Path
from dotenv import load_dotenv
import os
import time

load_dotenv()

SHOP = os.getenv("SHOPIFY_SHOP_NAME")
TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
BASE_URL = f"https://{SHOP}/admin/api/2024-01"
HEADERS = {"X-Shopify-Access-Token": TOKEN}
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

print("=== Shopify Extractor ===")
print(f"Conectando a: {SHOP}")
print()

# Extraer órdenes
print("[1/3] Extrayendo órdenes...")
url = f"{BASE_URL}/orders.json?limit=250"
orders = []
while url:
    print(f"  → Pidiendo: {url[:80]}...")
    resp = httpx.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json().get("orders", [])
    orders.extend(data)
    print(f"     Obtenidas {len(data)} órdenes. Total: {len(orders)}")
    
    # Paginación: buscar link "next" en el header Link
    link = resp.headers.get("Link", "")
    url = None
    for part in link.split(","):
        if 'rel="next"' in part:
            url = part.split(";")[0].strip().strip("<> ")
    time.sleep(0.5)

out = RAW_DIR / "orders.json"
out.write_text(json.dumps(orders, indent=2))
print(f"✓ {len(orders)} órdenes guardadas en {out}\n")

# Extraer productos
print("[2/3] Extrayendo productos...")
url = f"{BASE_URL}/products.json?limit=250"
products = []
while url:
    print(f"  → Pidiendo: {url[:80]}...")
    resp = httpx.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json().get("products", [])
    products.extend(data)
    print(f"     Obtenidos {len(data)} productos. Total: {len(products)}")
    
    link = resp.headers.get("Link", "")
    url = None
    for part in link.split(","):
        if 'rel="next"' in part:
            url = part.split(";")[0].strip().strip("<> ")
    time.sleep(0.5)

out = RAW_DIR / "products.json"
out.write_text(json.dumps(products, indent=2))
print(f"✓ {len(products)} productos guardados en {out}\n")

# Extraer clientes
print("[3/3] Extrayendo clientes...")
url = f"{BASE_URL}/customers.json?limit=250"
customers = []
while url:
    print(f"  → Pidiendo: {url[:80]}...")
    resp = httpx.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json().get("customers", [])
    customers.extend(data)
    print(f"     Obtenidos {len(data)} clientes. Total: {len(customers)}")
    
    link = resp.headers.get("Link", "")
    url = None
    for part in link.split(","):
        if 'rel="next"' in part:
            url = part.split(";")[0].strip().strip("<> ")
    time.sleep(0.5)

out = RAW_DIR / "customers.json"
out.write_text(json.dumps(customers, indent=2))
print(f"✓ {len(customers)} clientes guardados en {out}\n")

print("=== Extracción completada ===")
