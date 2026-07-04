select
    o.order_id,
    o.order_number,
    o.order_name,
    o.customer_id,
    o.order_created_at,
    o.financial_status,
    o.fulfillment_status,
    o.is_test_order,
    o.currency,
    o.subtotal_price,
    o.total_discounts,
    o.total_tax,
    o.total_price,
    o.order_source,
    coalesce(li.item_count, 0) as item_count,
    coalesce(li.total_quantity, 0) as total_quantity

from {{ ref('stg_shopify__orders') }} as o

left join (
    select
        order_id,
        count(*) as item_count,
        sum(quantity) as total_quantity
    from {{ ref('int_order_items') }}
    group by order_id
) as li
    on o.order_id = li.order_id
