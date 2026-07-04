select
    li.order_id,
    li.line_item_id,
    li.product_id,
    li.variant_id,
    li.product_title,
    li.variant_title,
    p.vendor,
    p.product_type,
    li.quantity,
    li.unit_price,
    li.total_discount,
    (li.unit_price * li.quantity) - li.total_discount as line_item_total,
    li.requires_shipping,
    li.taxable,
    li.gift_card,
    li.line_item_fulfillment_status

from {{ ref('int_order_items') }} as li

left join {{ ref('stg_shopify__products') }} as p
    on li.product_id = p.product_id

