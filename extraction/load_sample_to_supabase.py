import json
import psycopg2
from pathlib import Path

# Credenciales Supabase — mismas del profiles.yml
DB_CONFIG = {
    "host":     "aws-1-us-east-2.pooler.supabase.com",
    "port":     6543,
    "dbname":   "postgres",
    "user":     "postgres.adevrfzhdumldybnvcqc",
    "password": input("Supabase password: "),
}

SAMPLE_DIR = Path("data/sample")

print("=== Cargando datos a Supabase ===\n")

con = psycopg2.connect(**DB_CONFIG)
cur = con.cursor()

# Crear schema raw
cur.execute("CREATE SCHEMA IF NOT EXISTS raw")
con.commit()
print("✓ Schema 'raw' creado")

# Cargar orders
print("Cargando orders...")
with open(SAMPLE_DIR / "orders.json") as f:
    orders = json.load(f)

cur.execute("DROP TABLE IF EXISTS raw.orders CASCADE")
cur.execute("""
    CREATE TABLE raw.orders (
        id BIGINT,
        order_number INTEGER,
        name VARCHAR,
        customer JSONB,
        created_at TIMESTAMP,
        updated_at TIMESTAMP,
        processed_at TIMESTAMP,
        financial_status VARCHAR,
        fulfillment_status VARCHAR,
        total_price VARCHAR,
        subtotal_price VARCHAR,
        total_tax VARCHAR,
        total_discounts VARCHAR,
        total_line_items_price VARCHAR,
        currency VARCHAR,
        source_name VARCHAR,
        email VARCHAR,
        tags VARCHAR,
        test BOOLEAN,
        line_items JSONB
    )
""")
for o in orders:
    cur.execute("""
        INSERT INTO raw.orders VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
    """, (
        o["id"], o["order_number"], o["name"],
        json.dumps(o["customer"]),
        o["created_at"], o["updated_at"], o["processed_at"],
        o["financial_status"], o.get("fulfillment_status"),
        o["total_price"], o["subtotal_price"], o["total_tax"],
        o["total_discounts"], o["total_line_items_price"],
        o["currency"], o["source_name"], o.get("email"),
        o.get("tags", ""), o.get("test", False),
        json.dumps(o["line_items"])
    ))
con.commit()
print(f"✓ {len(orders)} órdenes cargadas")

# Cargar products
print("Cargando products...")
with open(SAMPLE_DIR / "products.json") as f:
    products = json.load(f)

cur.execute("DROP TABLE IF EXISTS raw.products CASCADE")
cur.execute("""
    CREATE TABLE raw.products (
        id BIGINT,
        title VARCHAR,
        vendor VARCHAR,
        product_type VARCHAR,
        status VARCHAR,
        tags VARCHAR,
        handle VARCHAR,
        published_scope VARCHAR,
        created_at TIMESTAMP,
        updated_at TIMESTAMP,
        published_at TIMESTAMP
    )
""")
for p in products:
    cur.execute("""
        INSERT INTO raw.products VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
    """, (
        p["id"], p["title"], p["vendor"], p["product_type"],
        p["status"], p.get("tags", ""), p["handle"],
        p["published_scope"], p["created_at"],
        p["updated_at"], p["published_at"]
    ))
con.commit()
print(f"✓ {len(products)} productos cargados")

# Cargar customers
print("Cargando customers...")
with open(SAMPLE_DIR / "customers.json") as f:
    customers = json.load(f)

cur.execute("DROP TABLE IF EXISTS raw.customers CASCADE")
cur.execute("""
    CREATE TABLE raw.customers (
        id BIGINT,
        email VARCHAR,
        first_name VARCHAR,
        last_name VARCHAR,
        orders_count INTEGER,
        total_spent VARCHAR,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
""")
for c in customers:
    cur.execute("""
        INSERT INTO raw.customers VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s
        )
    """, (
        c["id"], c["email"], c["first_name"], c["last_name"],
        c["orders_count"], c["total_spent"],
        c["created_at"], c["updated_at"]
    ))
con.commit()
print(f"✓ {len(customers)} clientes cargados")

cur.close()
con.close()
print("\n=== Carga completada ===")
