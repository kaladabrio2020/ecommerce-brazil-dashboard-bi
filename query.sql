SELECT oo.order_purchase_timestamp, oi.price
    FROM olist_order AS oo
        INNER JOIN olist_order_items AS oi 
            ON oi.order_id = oo.order_id
    WHERE oo.status_ = 'ok';
