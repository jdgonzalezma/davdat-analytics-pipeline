import duckdb
from pathlib import Path

DB_PATH = "shopify_pipeline_sample.duckdb"
SAMPLE_DIR = Path("data/sample")

print("=== Cargando datos anonimizados a DuckDB ===")
print()

con = duckdb.connect(DB_PATH)

# Crear schema raw
con.execute("CREATE SCHEMA IF NOT EXISTS raw")
print("✓ Schema 'raw' creado")

# Cargar orders
print("Cargando orders...")
con.execute(f"""
    CREATE OR REPLACE TABLE raw.orders AS
    SELECT * FROM read_json_auto('{SAMPLE_DIR}/orders.json')
""")
count = con.execute("SELECT COUNT(*) FROM raw.orders").fetchone()[0]
print(f"✓ {count} órdenes cargadas")

# Cargar products
print("Cargando products...")
con.execute(f"""
    CREATE OR REPLACE TABLE raw.products AS
    SELECT * FROM read_json_auto('{SAMPLE_DIR}/products.json')
""")
count = con.execute("SELECT COUNT(*) FROM raw.products").fetchone()[0]
print(f"✓ {count} productos cargados")

# Cargar customers
print("Cargando customers...")
con.execute(f"""
    CREATE OR REPLACE TABLE raw.customers AS
    SELECT * FROM read_json_auto('{SAMPLE_DIR}/customers.json')
""")
count = con.execute("SELECT COUNT(*) FROM raw.customers").fetchone()[0]
print(f"✓ {count} clientes cargados")

con.close()
print("\n✓ DuckDB anonimizado listo en:", DB_PATH)
