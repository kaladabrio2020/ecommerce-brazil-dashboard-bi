import json

data = {
    "queries": {

        "SomaTotalVendendores": """
CREATE TEMPORARY VIEW vendedores AS
    SELECT OS.seller_state, COUNT(OS.seller_state) AS quantidade_vendedores 
    FROM olist_seller AS OS 
    GROUP BY OS.seller_state
    ORDER BY quantidade_vendedores DESC
""",

        "SomaTotalVendendoresAgrupamendo": """
WITH soma AS (
    SELECT CAST(SUM(ve.quantidade_vendedores) AS INTEGER) AS total
    FROM vendedores AS ve
    WHERE ve.quantidade_vendedores < 20
)
SELECT DISTINCT
    CASE 
        WHEN v.quantidade_vendedores < 20 THEN s.total
        ELSE v.quantidade_vendedores
    END AS quantidade_vendedores,
    CASE
        WHEN CAST(
            CASE 
                WHEN v.quantidade_vendedores < 20 THEN s.total
                ELSE v.quantidade_vendedores
            END AS INTEGER) = 70 THEN (
                SELECT string_agg(seller_state, ', ') 
                FROM vendedores
                WHERE quantidade_vendedores < 20 
            )
        ELSE v.seller_state
    END AS todos_estados,
    CASE
        WHEN CAST(
            CASE 
                WHEN v.quantidade_vendedores < 20 THEN s.total
                ELSE v.quantidade_vendedores
            END AS INTEGER) = 70 THEN 'Outros estados'
        ELSE v.seller_state
    END AS estados
FROM vendedores v
CROSS JOIN soma s
""",
        "receitaTotalNosAnos":"""
select date_part('year', DATE(oli.shipping_limit_date)) AS ano , SUM(oop.payment_value) AS receita from olist_order AS olo
    INNER JOIN olist_order_items AS oli
        ON oli.order_id = olo.order_id
    INNER JOIN olist_order_payments AS oop 
        ON oop.order_id = olo.order_id
    WHERE olo.status_ = 'ok'
        GROUP BY ano LIMIT 3;
""",
        "receitaTotal":"""
select SUM(oop.payment_value) AS receita from olist_order AS olo
    INNER JOIN olist_order_items AS oli
        ON oli.order_id = olo.order_id
    INNER JOIN olist_order_payments AS oop 
        ON oop.order_id = olo.order_id
    WHERE olo.status_ = 'ok';
""",
    "produtoMaisVendido":"""
SELECT op.product_category_name FROM olist_order AS olo 
    INNER JOIN olist_order_items AS oli
        ON oli.order_id = olo.order_id
    INNER JOIN olist_products AS op
        ON op.product_id = oli.product_id
    WHERE olo.status_ = 'ok'
        GROUP BY product_category_name
            ORDER BY  count(op.product_category_name) DESC LIMIT 1;
""",
    "estadoComMaisVendedores":"""
SELECT ols.seller_state, count(ols.seller_state) 
    FROM olist_seller AS ols 
    GROUP BY ols.seller_state
        ORDER BY count DESC LIMIT 1;
""",
    "estadoComMaisCliente":"""
SELECT olc.customer_state, count(olc.customer_state) 
    FROM olist_customers AS olc
        GROUP BY olc.customer_state
    ORDER BY count DESC LIMIT 1;
""",
    "seriesHistoricaPedidos":"""
SELECT data_, count(data_) FROM(
    SELECT DATE(olo.order_purchase_timestamp) AS data_ FROM olist_order olo
        WHERE olo.status_='ok' 
    )
    GROUP BY data_ 
    ORDER BY data_ ASC;
""",
    "receitaCategoria":"""
WITH receita AS(
    SELECT order_id, sum(payment_value) AS result_ FROM olist_order_payments
    GROUP BY order_id
)
SELECT opp.product_category_name, SUM(result_) AS tota_receita FROM olist_order AS olo 
    INNER JOIN receita AS olp 
        ON olo.order_id = olp.order_id
    INNER JOIN olist_order_items AS oli 
        ON oli.order_id = olp.order_id
    INNER JOIN olist_products AS opp 
        ON oli.product_id = opp.product_id
    WHERE olo.status_='ok' AND
        date_part('year', olo.order_purchase_timestamp) >= 2016 AND
        date_part('year', olo.order_purchase_timestamp) <= 2018
    GROUP BY opp.product_category_name  
    ORDER BY tota_receita DESC LIMIT 10;
""",
    "serieHistoricaVendas":"""
select DATE(olo.order_purchase_timestamp) AS ano , SUM(oop.payment_value) AS receita from olist_order AS olo
    INNER JOIN olist_order_items AS oli
        ON oli.order_id = olo.order_id
    INNER JOIN olist_order_payments AS oop 
        ON oop.order_id = olo.order_id
    WHERE olo.status_ = 'ok' AND date_part('year', DATE(oli.shipping_limit_date)) < 2020
        GROUP BY ano
        ORDER BY ano ASC;
""",
    "distribuicaoClientes":"""
SELECT geolocation_state, COUNT(ols.customer_id) FROM olist_customers AS ols
    INNER JOIN olist_geolocation AS olg
        ON ols.customer_zip_code_prefix = olg.geolocation_zip_code_prefix
    GROUP BY geolocation_state;
""",
    "Semanas": """
select DATE(olo.order_purchase_timestamp) AS ano , COUNT(oop.payment_value) AS quantidade_vendas from olist_order AS olo
    INNER JOIN olist_order_items AS oli
        ON oli.order_id = olo.order_id
    INNER JOIN olist_order_payments AS oop 
        ON oop.order_id = olo.order_id
    WHERE olo.status_ = 'ok' AND date_part('year', DATE(oli.shipping_limit_date)) < 2020
        GROUP BY ano
        ORDER BY ano ASC;
"""
    }
}
estados = {
    "SP": "São Paulo",
    "RJ": "Rio de Janeiro",
    "MG": "Minas Gerais",
    "BA": "Bahia",
    "RS": "Rio Grande do Sul",
    "PR": "Paraná",
    "SC": "Santa Catarina",
    "PE": "Pernambuco",
    "CE": "Ceará",
    "GO": "Goiás",
    "PA": "Pará",
    "AM": "Amazonas",
    "ES": "Espírito Santo",
    "PB": "Paraíba",
    "RN": "Rio Grande do Norte",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "AL": "Alagoas",
    "PI": "Piauí",
    "SE": "Sergipe",
    "RO": "Rondônia",
    "TO": "Tocantins",
    "AC": "Acre",
    "AP": "Amapá",
    "RR": "Roraima",
    "DF": "Distrito Federal"
}



with open("backend\\queries-states.json", "w", encoding="utf-8") as f:
    json.dump(estados, f, indent=4, ensure_ascii=False)


with open("backend\\queries.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
