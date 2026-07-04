select
    id as product_id,
    title as product_title,
    vendor,
    product_type,
    status as product_status,
    tags,
    handle as product_handle,
    published_scope,
    created_at as product_created_at,
    updated_at as product_updated_at,
    published_at as product_published_at

from {{ source('shopify_raw', 'products') }}
