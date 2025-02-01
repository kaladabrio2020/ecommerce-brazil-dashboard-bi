-- Active: 1738412203579@@127.0.0.1@5432@ecommerce@public

---
CREATE  TEMPORARY VIEW vendedores AS
    SELECT OS.seller_state, COUNT(OS.seller_state) AS quantidade_vendedores FROM olist_seller AS OS 
        GROUP BY OS.seller_state
    ORDER BY quantidade_vendedores DESC;
        
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
;
--- tipo de pagamento prefiro

SELECT count() FROM ;