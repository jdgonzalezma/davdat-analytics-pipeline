import json
from pathlib import Path
from faker import Faker
import random

fake = Faker("es_CO")
random.seed(42)

RAW_DIR = Path("data/raw")
SAMPLE_DIR = Path("data/sample")
SAMPLE_DIR.mkdir(exist_ok=True)

print("=== Anonimizando datos ===\n")

# Mapeo consistente: customer_id real → datos fake
customer_mapping = {}

def fake_customer(real_id):
    if real_id not in customer_mapping:
        customer_mapping[real_id] = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
        }
    return customer_mapping[real_id]

# Anonimizar clientes
print("Anonimizando clientes...")
with open(RAW_DIR / "customers.json") as f:
    customers = json.load(f)

anon_customers = []
for c in customers:
    fake_data = fake_customer(c["id"])
    anon_customers.append({
        "id": c["id"],
        "email": fake_data["email"],
        "first_name": fake_data["first_name"],
        "last_name": fake_data["last_name"],
        "orders_count": c["orders_count"],
        "total_spent": str(float(c["total_spent"]) * random.uniform(0.85, 1.15)),
        "created_at": c["created_at"],
        "updated_at": c["updated_at"],
    })

with open(SAMPLE_DIR / "customers.json", "w") as f:
    json.dump(anon_customers, f, indent=2)
print(f"✓ {len(anon_customers)} clientes anonimizados\n")

# Anonimizar productos
print("Anonimizando productos...")
with open(RAW_DIR / "products.json") as f:
    products = json.load(f)

product_titles = [f"Producto {i:03d}" for i in range(1, len(products) + 1)]
vendors = ["Marca A", "Marca B", "Marca C"]

anon_products = []
for idx, p in enumerate(products):
    anon_products.append({
        "id": p["id"],
        "title": product_titles[idx],
        "vendor": random.choice(vendors),
        "product_type": f"Categoría {random.choice(['A', 'B', 'C'])}",
        "status": p["status"],
        "created_at": p["created_at"],
        "updated_at": p["updated_at"],
    })

with open(SAMPLE_DIR / "products.json", "w") as f:
    json.dump(anon_products, f, indent=2)
print(f"✓ {len(anon_products)} productos anonimizados\n")

# Anonimizar órdenes
print("Anonimizando órdenes...")
with open(RAW_DIR / "orders.json") as f:
    orders = json.load(f)

anon_orders = []
for o in orders:
    fake_data = fake_customer(o["customer"]["id"]) if o.get("customer") else None
    
    # Anonimizar line_items
    anon_line_items = []
    for li in o.get("line_items", []):
        # Encontrar el producto anonimizado
        anon_prod = next((p for p in anon_products if p["id"] == li["product_id"]), None)
        anon_line_items.append({
            "id": li["id"],
            "product_id": li["product_id"],
            "title": anon_prod["title"] if anon_prod else "Producto Desconocido",
            "quantity": li["quantity"],
            "price": str(float(li["price"]) * random.uniform(0.85, 1.15)),
            "total_discount": li.get("total_discount", "0"),
        })
    
    anon_orders.append({
        "id": o["id"],
        "customer": {
            "id": o["customer"]["id"],
            "email": fake_data["email"] if fake_data else "unknown@example.com",
            "first_name": fake_data["first_name"] if fake_data else "Cliente",
            "last_name": fake_data["last_name"] if fake_data else "Anonimizado",
        } if o.get("customer") else None,
        "created_at": o["created_at"],
        "updated_at": o["updated_at"],
        "financial_status": o["financial_status"],
        "fulfillment_status": o["fulfillment_status"],
        "total_price": str(float(o["total_price"]) * random.uniform(0.85, 1.15)),
        "subtotal_price": str(float(o.get("subtotal_price", 0)) * random.uniform(0.85, 1.15)),
        "total_tax": str(float(o.get("total_tax", 0)) * random.uniform(0.85, 1.15)),
        "currency": o["currency"],
        "source_name": o.get("source_name"),
        "referring_site": o.get("referring_site"),
        "line_items": anon_line_items,
        "billing_address": o.get("billing_address"),
        "shipping_address": o.get("shipping_address"),
    })

with open(SAMPLE_DIR / "orders.json", "w") as f:
    json.dump(anon_orders, f, indent=2)
print(f"✓ {len(anon_orders)} órdenes anonimizadas\n")

print("=== Anonimización completada ===")
print(f"Datos en: {SAMPLE_DIR}/")
