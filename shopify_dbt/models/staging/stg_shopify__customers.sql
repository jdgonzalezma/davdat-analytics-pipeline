select
    id as customer_id,
    email,
    first_name,
    last_name,
    orders_count,
    cast(total_spent as decimal(12, 2)) as total_spent,
    created_at,
    updated_at
from {{ source('shopify_raw', 'customers') }}
