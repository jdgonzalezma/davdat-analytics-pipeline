{% if target.type == 'duckdb' %}

select
    o.id as order_id,
    o.order_number,
    li.id as line_item_id,
    li.product_id,
    li.variant_id,
    li.title as product_title,
    li.variant_title,
    li.vendor,
    li.quantity,
    cast(li.price as decimal(12, 2)) as unit_price,
    cast(li.total_discount as decimal(12, 2)) as total_discount,
    li.requires_shipping,
    li.taxable,
    li.gift_card,
    li.fulfillment_status as line_item_fulfillment_status

from {{ source('shopify_raw', 'orders') }} as o,
    unnest(o.line_items) as t(li)

{% else %}

select
    o.id as order_id,
    o.order_number,
    (li->>'id')::bigint as line_item_id,
    (li->>'product_id')::bigint as product_id,
    (li->>'variant_id')::bigint as variant_id,
    li->>'title' as product_title,
    li->>'variant_title' as variant_title,
    li->>'vendor' as vendor,
    (li->>'quantity')::integer as quantity,
    cast(li->>'price' as decimal(12, 2)) as unit_price,
    cast(li->>'total_discount' as decimal(12, 2)) as total_discount,
    (li->>'requires_shipping')::boolean as requires_shipping,
    (li->>'taxable')::boolean as taxable,
    (li->>'gift_card')::boolean as gift_card,
    li->>'fulfillment_status' as line_item_fulfillment_status

from {{ source('shopify_raw', 'orders') }} as o,
    jsonb_array_elements(o.line_items) as li

{% endif %}
