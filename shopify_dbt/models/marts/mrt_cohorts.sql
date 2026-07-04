with first_orders as (

    select
        customer_id,
        date_trunc('month', min(order_created_at)) as cohort_month

    from {{ ref('int_customer_order_sequence') }}
    group by customer_id

),

order_months as (

    select
        o.customer_id,
        f.cohort_month,
        date_trunc('month', o.order_created_at) as order_month,
        {% if target.type == 'duckdb' %}
        datediff('month', f.cohort_month, date_trunc('month', o.order_created_at))
        {% else %}
        (date_part('year', date_trunc('month', o.order_created_at)) - date_part('year', f.cohort_month)) * 12 +
        date_part('month', date_trunc('month', o.order_created_at)) - date_part('month', f.cohort_month)
        {% endif %} as months_since_first_order

    from {{ ref('int_customer_order_sequence') }} as o
    left join first_orders as f
        on o.customer_id = f.customer_id

),

cohort_size as (

    select
        cohort_month,
        count(distinct customer_id) as cohort_customer_count

    from first_orders
    group by cohort_month

),

cohort_retention as (

    select
        om.cohort_month,
        om.months_since_first_order,
        count(distinct om.customer_id) as active_customers

    from order_months as om
    group by om.cohort_month, om.months_since_first_order

)

select
    cr.cohort_month,
    cs.cohort_customer_count,
    cr.months_since_first_order,
    cr.active_customers,
    round(
        cr.active_customers * 100.0 / cs.cohort_customer_count,
        1
    ) as retention_rate_pct

from cohort_retention as cr
left join cohort_size as cs
    on cr.cohort_month = cs.cohort_month

order by cr.cohort_month, cr.months_since_first_order
