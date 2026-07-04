with orders_with_customer as (

    select
        o.order_id,
        o.customer_id,
        o.order_source,
        o.total_price,
        o.order_created_at

    from {{ ref('stg_shopify__orders') }} as o
    where o.customer_id is not null

),

ltv_by_channel as (

    select
        order_source,
        count(distinct customer_id)     as unique_customers,
        count(order_id)                 as total_orders,
        sum(total_price)                as total_revenue,
        avg(total_price)                as avg_order_value,
        sum(total_price)
            / count(distinct customer_id) as ltv_per_customer

    from orders_with_customer
    group by order_source

)

select * from ltv_by_channel
order by ltv_per_customer desc
