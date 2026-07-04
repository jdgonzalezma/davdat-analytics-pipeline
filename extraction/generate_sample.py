import json
import random
from pathlib import Path
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("es_CO")
random.seed(99)

SAMPLE_DIR = Path("data/sample")
SAMPLE_DIR.mkdir(exist_ok=True)

print("=== Generando datos sintéticos ===\n")

# ─────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────
NUM_CUSTOMERS   = 100
NUM_PRODUCTS    = 20
CHANNELS        = ["web", "instagram", "email", "facebook"]
PRICE_RANGES    = [
    (50000,  150000),   # productos baratos
    (150000, 300000),   # productos medios
    (300000, 600000),   # productos caros
]
# distribución de órdenes por cliente:
# 60% compra 1 vez, 25% compra 2 veces, 10% compra 3, 4% compra 4, 1% compra 5
ORDER_DIST = [1]*60 + [2]*25 + [3]*10 + [4]*4 + [5]*1

def random_date(months_back=12):
    """Fecha aleatoria dentro de los últimos N meses"""
    days_back = random.randint(1, months_back * 30)
    return datetime.now() - timedelta(days=days_back)

def fmt(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S%z") + "+00:00"

# ─────────────────────────────────────────
# PRODUCTOS SINTÉTICOS
# ─────────────────────────────────────────
print("Generando productos...")
categories   = ["Camisetas", "Pantalones", "Accesorios", "Zapatos", "Ropa exterior"]
vendors_list = ["Marca A", "Marca B", "Marca C"]

products = []
for i in range(1, NUM_PRODUCTS + 1):
    price_range = random.choice(PRICE_RANGES)
    price = random.randint(*price_range)
    cat   = random.choice(categories)
    products.append({
        "id":           i * 1000,
        "title":        f"Producto {i:03d} — {cat}",
        "vendor":       random.choice(vendors_list),
        "product_type": cat,
        "status":       "active",
	"status":       "active",
        "tags":         "",    
        "handle":         f"producto-{i:03d}",              
        "published_scope": "global",                        
        "published_at":   fmt(random_date(6)),              
        "price":        price,
        "created_at":   fmt(random_date(24)),
        "updated_at":   fmt(random_date(6)),
    })

with open(SAMPLE_DIR / "products.json", "w") as f:
    json.dump(products, f, indent=2, ensure_ascii=False)
print(f"✓ {len(products)} productos generados\n")

# ─────────────────────────────────────────
# CLIENTES SINTÉTICOS
# ─────────────────────────────────────────
print("Generando clientes...")
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    created = random_date(18)
    customers.append({
        "id":           i * 10000,
        "email":        fake.email(),
        "first_name":   fake.first_name(),
        "last_name":    fake.last_name(),
        "orders_count": 0,           # se actualiza abajo
        "total_spent":  "0",         # se actualiza abajo
        "created_at":   fmt(created),
        "updated_at":   fmt(created),
    })

print(f"✓ {len(customers)} clientes generados\n")

# ─────────────────────────────────────────
# ÓRDENES SINTÉTICAS
# ─────────────────────────────────────────
print("Generando órdenes...")
orders       = []
order_id_seq = 1
totals_by_customer = {c["id"]: 0.0 for c in customers}
counts_by_customer = {c["id"]: 0    for c in customers}

for customer in customers:
    num_orders = random.choice(ORDER_DIST)
    # primera fecha de compra: random dentro de últimos 12 meses
    first_order_date = random_date(12)

    for order_seq in range(num_orders):
        # cada orden siguiente ocurre entre 15 y 120 días después
        if order_seq == 0:
            order_date = first_order_date
        else:
            order_date = order_date + timedelta(days=random.randint(15, 120))
            # si la fecha resultante es futura, la fijamos a hoy
            if order_date > datetime.now():
                break

        # líneas de producto: 1 a 3 productos por orden
        num_items  = random.randint(1, 3)
        line_items = []
        order_total = 0.0

        for _ in range(num_items):
            prod     = random.choice(products)
            qty      = random.randint(1, 2)
            price    = prod["price"] * random.uniform(0.9, 1.1)
            discount = price * random.uniform(0, 0.1)  # descuento de 0-10%
            subtotal = (price * qty) - discount
            order_total += subtotal

            line_items.append({
                "id":             order_id_seq * 100 + len(line_items),
                "product_id":     prod["id"],
                "variant_id":     prod["id"] + 1,
                "title":          prod["title"],
                "variant_title":  random.choice(["S", "M", "L", "XL", "Único"]),
                "quantity":       qty,
                "price":          str(round(price, 2)),
                "total_discount": str(round(discount, 2)),
                "fulfillment_status": random.choice(["fulfilled", None]),
                "vendor":         prod["vendor"],
                "requires_shipping": True,
                "taxable":        True,
                "gift_card":      False,
            })

        # estado financiero: 85% pagado, 10% pendiente, 5% reembolsado
        fin_status = random.choices(
            ["paid", "pending", "refunded"],
            weights=[85, 10, 5]
        )[0]

        orders.append({
            "id":                 order_id_seq,
            "order_number":       1000 + order_id_seq,
            "name":               f"#{ 1000 + order_id_seq }",
            "customer": {
                "id":         customer["id"],
                "email":      customer["email"],
                "first_name": customer["first_name"],
                "last_name":  customer["last_name"],
            },
            "created_at":         fmt(order_date),
            "updated_at":         fmt(order_date),
            "processed_at":       fmt(order_date),
            "financial_status":   fin_status,
            "fulfillment_status": random.choice(["fulfilled", None]),
            "total_price":        str(round(order_total, 2)),
            "subtotal_price":     str(round(order_total * 0.85, 2)),
            "total_tax":          str(round(order_total * 0.15, 2)),
            "total_discounts":    str(round(sum(
                float(li["total_discount"]) for li in line_items
            ), 2)),
            "total_line_items_price": str(round(order_total, 2)),
            "currency":           "COP",
            "email":              customer["email"], 
            "source_name":        random.choice(CHANNELS),
            "tags":               "",
            "test":               False,
            "line_items":         line_items,
        })

        totals_by_customer[customer["id"]] += order_total
        counts_by_customer[customer["id"]] += 1
        order_id_seq += 1

# actualizar totales en clientes
for c in customers:
    c["orders_count"] = counts_by_customer[c["id"]]
    c["total_spent"]  = str(round(totals_by_customer[c["id"]], 2))

with open(SAMPLE_DIR / "customers.json", "w") as f:
    json.dump(customers, f, indent=2, ensure_ascii=False)

with open(SAMPLE_DIR / "orders.json", "w") as f:
    json.dump(orders, f, indent=2, ensure_ascii=False)

print(f"✓ {len(orders)} órdenes generadas")
print(f"✓ {len(customers)} clientes actualizados\n")
print("=== Generación completada ===")
print(f"Datos en: {SAMPLE_DIR}/")
