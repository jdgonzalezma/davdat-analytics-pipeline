select
    order_id,
    customer_id,
    order_created_at,
    total_price,
    row_number() over (
        partition by customer_id
        order by order_created_at asc
    ) as order_sequence_number

from {{ ref('stg_shopify__orders') }}
where customer_id is not null
