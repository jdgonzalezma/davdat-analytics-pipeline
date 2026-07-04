select
    c.customer_id,
    c.email,
    c.first_name,
    c.last_name,
    c.created_at as customer_created_at,

    coalesce(o.total_orders, 0) as total_orders,
    coalesce(o.lifetime_value, 0) as lifetime_value,
    o.first_order_date,
    o.last_order_date

from {{ ref('stg_shopify__customers') }} as c

left join (
    select
        customer_id,
        count(*) as total_orders,
        sum(total_price) as lifetime_value,
        min(order_created_at) as first_order_date,
        max(order_created_at) as last_order_date
    from {{ ref('int_customer_order_sequence') }}
    group by customer_id
) as o
    on c.customer_id = o.customer_id

