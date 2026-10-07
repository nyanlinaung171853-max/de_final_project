-- ==========================================
-- DIM PRODUCT
-- ==========================================

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

    effective_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    effective_to TIMESTAMP,

    is_current BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================
-- DIM CUSTOMER
-- ==========================================

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key SERIAL PRIMARY KEY,

    customer_id INTEGER NOT NULL,

    customer_name VARCHAR(255),

    email VARCHAR(255),

    city VARCHAR(100),

    country VARCHAR(100),

    effective_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    effective_to TIMESTAMP,

    is_current BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================
-- DIM DATE
-- ==========================================

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,

    full_date DATE NOT NULL,

    year INTEGER,

    quarter INTEGER,

    month INTEGER,

    month_name VARCHAR(20),

    day INTEGER,

    day_name VARCHAR(20),

    week_of_year INTEGER
);