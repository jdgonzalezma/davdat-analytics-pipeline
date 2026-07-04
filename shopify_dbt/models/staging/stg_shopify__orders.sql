select
    id as order_id,
    order_number,
    name as order_name,

    {% if target.type == 'duckdb' %}
    customer.id as customer_id,
    {% else %}
    (customer->>'id')::bigint as customer_id,
    {% endif %}

    email,
    financial_status,
    fulfillment_status,
    test as is_test_order,
    currency,
    cast(subtotal_price as decimal(12, 2)) as subtotal_price,
    cast(total_discounts as decimal(12, 2)) as total_discounts,
    cast(total_tax as decimal(12, 2)) as total_tax,
    cast(total_line_items_price as decimal(12, 2)) as total_line_items_price,
    cast(total_price as decimal(12, 2)) as total_price,
    source_name as order_source,
    tags,
    created_at as order_created_at,
    processed_at as order_processed_at,
    updated_at as order_updated_at

from {{ source('shopify_raw', 'orders') }}
