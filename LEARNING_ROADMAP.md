## Fase 1: Fundamentos y Autenticación
- [x] Entender OAuth 2.0 con Shopify
- [x] Generar credenciales (Client ID + Secret)
- [x] Obtener access token
- [x] Documentar flujo de autenticación

## Fase 2: Extracción de Datos
- [x] Implementar paginación con cursores
- [x] Extraer orders (23), products (38), customers (433)
- [x] Guardar como JSONs en data/raw/

## Fase 3: Almacenamiento Local
- [x] Configurar DuckDB
- [x] Cargar JSONs a shopify_pipeline.duckdb (real)
- [x] Cargar JSONs a shopify_pipeline_sample.duckdb (anonimizado)

## Fase 4: Anonimización para Portafolio
- [x] Generar datos sintéticos con Faker
- [x] Crear data/sample/ con 433 clientes, 38 productos, 23 órdenes

## Fase 5: Transformación con dbt
- [x] Instalar dbt-core + dbt-duckdb
- [x] Inicializar proyecto shopify_dbt
- [x] Crear _shopify__sources.yml
- [x] Crear primer modelo: stg_shopify__customers
- [ ] Crear stg_shopify__orders
- [ ] Crear stg_shopify__products
- [ ] Crear intermediate models
- [ ] Crear marts (dim, fct, mrt)

## Fase 6-9: Pendiente
- [ ] Análisis de negocio
- [ ] Cloud (Supabase)
- [ ] Looker Studio
- [ ] Documentación y portafolio

