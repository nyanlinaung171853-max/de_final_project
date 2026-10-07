-- ==========================================
-- FACT SALES
-- Grain:
-- One row = One product sale within one order
-- ==========================================

CREATE TABLE IF NOT EXISTS fact_sales (

    sales_key BIGSERIAL PRIMARY KEY,

    order_id INTEGER NOT NULL,

    product_key INTEGER NOT NULL,

    customer_key INTEGER,

    date_key INTEGER NOT NULL,

    quantity INTEGER NOT NULL,

    unit_price DECIMAL(12,2),

    sales_amount DECIMAL(12,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_product
        FOREIGN KEY (product_key)
        REFERENCES dim_product(product_key),

    CONSTRAINT fk_customer
        FOREIGN KEY (customer_key)
        REFERENCES dim_customer(customer_key),

    CONSTRAINT fk_date
        FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);