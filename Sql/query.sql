-- Active: 1738412203579@@127.0.0.1@5432@ecommerce@public

---
CREATE TEMPORARY VIEW vendedores AS
    SELECT OS.seller_state, COUNT(OS.seller_state) AS quantidade_vendedores FROM olist_seller AS OS 
        GROUP BY OS.seller_state
    ORDER BY quantidade_vendedores DESC;

SELECT * FROM vendedores;
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
                SELECT string_agg( seller_state , ', ') FROM vendedores
                    WHERE quantidade_vendedores < 20 )
            ELSE v.seller_state
    END AS todos_estados,
    CASE
        WHEN CAST(
            CASE 
                WHEN v.quantidade_vendedores < 20 THEN s.total
                    ELSE v.quantidade_vendedores
                END AS INTEGER) = 70  THEN 'Outros estados'
        ELSE v.seller_state
        END AS estados
FROM vendedores v
CROSS JOIN soma s;

-- 

---
select date_part('year', DATE(oli.shipping_limit_date)) AS ano , SUM(oop.payment_value) AS receita from olist_order AS olo
    INNER JOIN olist_order_items AS oli
        ON oli.order_id = olo.order_id
    INNER JOIN olist_order_payments AS oop 
        ON oop.order_id = olo.order_id
    WHERE olo.status_ = 'ok'
        GROUP BY ano LIMIT 3;

---Receita total 
select SUM(oop.payment_value) AS receita from olist_order AS olo
    INNER JOIN olist_order_items AS oli
        ON oli.order_id = olo.order_id
    INNER JOIN olist_order_payments AS oop 
        ON oop.order_id = olo.order_id
    WHERE olo.status_ = 'ok';

--- Produto mais vendido
SELECT op.product_category_name FROM olist_order AS olo 
    INNER JOIN olist_order_items AS oli
        ON oli.order_id = olo.order_id
    INNER JOIN olist_products AS op
        ON op.product_id = oli.product_id
    WHERE olo.status_ = 'ok'
        GROUP BY product_category_name
            ORDER BY  count(op.product_category_name) DESC LIMIT 1;

--- Meior estado de vendendores
SELECT ols.seller_state, count(ols.seller_state) 
    FROM olist_seller AS ols 
    GROUP BY ols.seller_state
        ORDER BY count DESC LIMIT 1;

-- cliente 
SELECT olc.customer_state, count(olc.customer_state) 
    FROM olist_customers AS olc
        GROUP BY olc.customer_state
    ORDER BY count DESC LIMIT 1; 

SELECT data_, count(data_) FROM(
    SELECT DATE(olo.order_purchase_timestamp) AS data_ FROM olist_order olo
        WHERE olo.status_='ok' 
    )
    GROUP BY data_ 
    ORDER BY data_ ASC;


SELECT date_part('year', DATE(olo.order_purchase_timestamp)) AS data_, SUM(olp.payment_value) FROM olist_order AS olo 
    INNER JOIN olist_order_payments AS olp 
        ON olp.order_id = olo.order_id
        WHERE olo.status_ = 'ok'
    GROUP BY data_;

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