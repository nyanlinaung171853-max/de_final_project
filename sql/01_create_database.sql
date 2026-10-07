CREATE TABLE IF NOT EXISTS dim_product (
    product_key SERIAL PRIMARY KEY,

    product_id INTEGER NOT NULL,

    product_name VARCHAR(255),

    category VARCHAR(100),

    brand VARCHAR(100),

    sku VARCHAR(100),

    price DECIMAL(12,2),

    discount_percentage DECIMAL(5,2),

    discounted_price DECIMAL(12,2),

    rating DECIMAL(4,2),

    stock INTEGER,

    stock_status VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);