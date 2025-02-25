CREATE TABLE metrics (
	id INTEGER NOT NULL, 
	order_id VARCHAR(50) NOT NULL, 
	processing_start_time DATETIME, 
	processing_end_time DATETIME, 
	created_at DATETIME, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_metrics_order_id ON metrics (order_id);

CREATE TABLE orders (
	id INTEGER NOT NULL, 
	order_id VARCHAR(50) NOT NULL, 
	user_id VARCHAR(50) NOT NULL, 
	item_ids VARCHAR(255) NOT NULL, 
	total_amount FLOAT NOT NULL, 
	status VARCHAR(10), 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_orders_status ON orders (status);
CREATE UNIQUE INDEX ix_orders_order_id ON orders (order_id);
