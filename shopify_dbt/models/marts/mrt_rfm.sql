with rfm_base as (

    select
        customer_id,
        count(order_id) as frequency,
        sum(total_price) as monetary,
        max(order_created_at) as last_order_date,
        {% if target.type == 'duckdb' %}
            datediff('day', max(order_created_at), current_date) as recency_days
        {% else %}
            date_part('day', current_date::timestamp - max(order_created_at))::integer as recency_days
        {% endif %}

    from {{ ref('int_customer_order_sequence') }}
    group by customer_id

),

rfm_scores as (

    select
        customer_id,
        recency_days,
        frequency,
        monetary,
        last_order_date,

        -- puntaje recency: menos días = mejor = puntaje más alto
        -- por eso invertimos: ntile ordena de menor a mayor, pero queremos
        -- que el cliente más reciente (menos días) tenga puntaje 3
        4 - ntile(3) over (order by recency_days asc) as r_score,

        -- puntaje frequency: más órdenes = mejor = puntaje más alto
        ntile(3) over (order by frequency asc) as f_score,

        -- puntaje monetary: más gasto = mejor = puntaje más alto
        ntile(3) over (order by monetary asc) as m_score

    from rfm_base

),

rfm_segments as (

    select
        customer_id,
        recency_days,
        frequency,
        monetary,
        last_order_date,
        r_score,
        f_score,
        m_score,
        r_score + f_score + m_score as rfm_total,

        case
            when r_score = 3 and f_score = 3 and m_score = 3
                then 'Champion'
            when r_score >= 2 and f_score >= 2
                then 'Leal'
            when r_score = 3 and f_score = 1
                then 'Cliente nuevo'
            when r_score <= 2 and f_score >= 2
                then 'En riesgo'
            when r_score = 1 and f_score = 1 and m_score >= 2
                then 'No puedo perderlos'
            when r_score = 1
                then 'Perdido'
            else 'Necesita atención'
        end as rfm_segment

    from rfm_scores

)

select * from rfm_segments
