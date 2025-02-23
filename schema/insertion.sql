INSERT INTO orders (id, order_id, user_id, item_ids, total_amount, status, created_at, updated_at) VALUES
(1, 'ORD12345', 'USR001', '[\"ITM001\",\"ITM002\"]', 299.99, 'Completed', '2025-02-01 10:15:10', '2025-02-01 10:15:14'),
(2, 'ORD12346', 'USR002', '[\"ITM003\"]', 159.49, 'Completed', '2025-02-01 10:20:10', '2025-02-01 10:20:14'),
(3, 'ORD12347', 'USR003', '[\"ITM004\",\"ITM005\",\"ITM006\"]', 499.99, 'Completed', '2025-02-01 10:25:30', '2025-02-01 10:25:34');

INSERT INTO metrics (id, order_id, processing_start_time, processing_end_time, created_at) VALUES
(1, 'ORD12345', '2025-02-01 10:15:12', '2025-02-01 10:15:14', '2025-02-01 10:15:10'),
(2, 'ORD12346', '2025-02-01 10:20:11', '2025-02-01 10:20:14', '2025-02-01 10:20:10'),
(3, 'ORD12347', '2025-02-01 10:25:33', '2025-02-01 10:25:34', '2025-02-01 10:25:30');
