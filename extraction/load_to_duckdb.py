import duckdb
from pathlib import Path

DB_PATH = "shopify_pipeline.duckdb"
RAW_DIR = Path("data/raw")

print("=== Cargando JSONs a DuckDB ===")
print()

con = duckdb.connect(DB_PATH)

# Crear schema raw
con.execute("CREATE SCHEMA IF NOT EXISTS raw")
print("✓ Schema 'raw' creado")

# Cargar orders
print("\nCargando orders...")
con.execute(f"""
    CREATE OR REPLACE TABLE raw.orders AS
    SELECT * FROM read_json_auto('{RAW_DIR}/orders.json')
""")
count = con.execute("SELECT COUNT(*) FROM raw.orders").fetchone()[0]
print(f"✓ {count} órdenes cargadas")

# Cargar products
print("Cargando products...")
con.execute(f"""
    CREATE OR REPLACE TABLE raw.products AS
    SELECT * FROM read_json_auto('{RAW_DIR}/products.json')
""")
count = con.execute("SELECT COUNT(*) FROM raw.products").fetchone()[0]
print(f"✓ {count} productos cargados")

# Cargar customers
print("Cargando customers...")
con.execute(f"""
    CREATE OR REPLACE TABLE raw.customers AS
    SELECT * FROM read_json_auto('{RAW_DIR}/customers.json')
""")
count = con.execute("SELECT COUNT(*) FROM raw.customers").fetchone()[0]
print(f"✓ {count} clientes cargados")

# Inspeccionar schema
print("\n=== Esquema de las tablas ===")
for table in ["orders", "products", "customers"]:
    print(f"\n{table}:")
    schema = con.execute(f"DESCRIBE raw.{table}").fetchall()
    for col_name, col_type, *_ in schema:
        print(f"  {col_name}: {col_type}")

con.close()
print("\n✓ DuckDB listo en:", DB_PATH)
