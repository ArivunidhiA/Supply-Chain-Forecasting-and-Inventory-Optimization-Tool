-- Create Sales History Table
CREATE TABLE sales_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    product_id VARCHAR(10) NOT NULL,
    sales INTEGER NOT NULL,
    inventory_level INTEGER NOT NULL,
    lead_time INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Products Table
CREATE TABLE products (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    unit_cost DECIMAL(10,2),
    reorder_point INTEGER,
    minimum_order_quantity INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Suppliers Table
CREATE TABLE suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name VARCHAR(100) NOT NULL,
    lead_time INTEGER,
    reliability_score DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Inventory Transactions Table
CREATE TABLE inventory_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id VARCHAR(10) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    quantity INTEGER NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_sales_date ON sales_history(date);
CREATE INDEX idx_sales_product ON sales_history(product_id);
CREATE INDEX idx_inventory_product ON inventory_transactions(product_id);
