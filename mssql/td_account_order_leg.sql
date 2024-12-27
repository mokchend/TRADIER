CREATE TABLE td_account_order_leg (
    id BIGINT PRIMARY KEY, -- Unique ID for the leg
    order_id BIGINT NOT NULL, -- Foreign key referencing td_account_order
    type VARCHAR(50),
    symbol VARCHAR(50),
    side VARCHAR(50),
    quantity DECIMAL(10, 2),
    status VARCHAR(50),
    duration VARCHAR(50),
    price DECIMAL(10, 2),
    avg_fill_price DECIMAL(10, 2),
    exec_quantity DECIMAL(10, 2),
    last_fill_price DECIMAL(10, 2),
    last_fill_quantity DECIMAL(10, 2),
    remaining_quantity DECIMAL(10, 2),
    create_date DATETIME,
    transaction_date DATETIME,
    class VARCHAR(50),
    option_symbol VARCHAR(100),
    FOREIGN KEY (order_id) REFERENCES td_account_order(id) ON DELETE CASCADE -- Ensures referential integrity
);
