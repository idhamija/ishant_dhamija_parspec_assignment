# E-Commerce Order Processing Backend

## Overview

This backend service manages and processes orders for an e-commerce platform. It provides:

- A RESTful API for order creation and status checking.
- An asynchronous order processing mechanism using an in-memory queue.
- A metrics endpoint to monitor total orders processed, average processing time, and order statuses.

## Components

- **API**: Built using Flask.
- **Database**: SQLite via SQLAlchemy (easily replaceable with PostgreSQL/MySQL).
- **Queue Processing**: A Python in-memory queue with a background worker thread.
- **Metrics Reporting**: Fetched on app initialization and then handled in-memory.

## Setup and Running Instructions

1. **Clone the Repository**
   - `git clone https://github.com/your-repo/order-processing-backend.git`
   - `cd ecommerce-backend`
2. **Install Dependencies**
   - Set up a virtual environment
   - Run `pip install -r requirements.txt`
3. **Start the Application**
   - Run `python app.py`

## Example API Requests and Responses

### Create Order

**Request:**

```
curl -X POST http://127.0.0.1:5000/orders \
-H "Content-Type: application/json" \
-d '{"user_id": "user1", "order_id": "A0001", "item_ids": ["item1", "item2"], "total_amount": 199.99}'
```

**Response:**

```
{
    "message": "Order received",
    "order_id": "A0001"
}
```

### Get Order Details

**Request:**

```
curl http://localhost:3000/orders/A0001
```

**Response:**

```
{
  "order_id": "A0001",
  "user_id": "user1",
  "item_ids": "[\"item1\", \"item2\"]",
  "status": "pending",
  "total_amount": 199.99,
  "created_at": "2025-02-23T12:12:23.017204",
  "updated_at": "2025-02-23T12:12:23.017204"
}
```

### Get Metrics

**Request:**

```
curl http://localhost:3000/metrics
```

**Response:**

```
{
  "avg_processing_time": 2.26,
  "total_orders": 1000
  "order_status_counts": {
    "completed": 879,
    "pending": 111,
    "processing": 10
  },
}
```

## Design Decisions and Trade-offs

- **RESTful Design:** Chosen for its simplicity and compatibility with various clients.
- **Lightweight Framework:** Ensures minimal performance overhead but requires additional work for more advanced features.
- **In-Memory Metrics:** Loads initial metrics from the database and then uses an in-memory metrics object to store and fetch metrics. For better scalability, consider using a dedicated in-memory datastore like Redis.
- **In-Memory Queue for Asynchronous Processing:** The current implementation uses an in-memory queue for simplicity. For production-level scalability, you should consider using distributed queue solutions such as Kafka, Redis, etc.
- **SQLite Database:** SQLite is used for ease-of-use and development. For a scalable production service, a more robust SQL database such as MySQL or PostgreSQL should be used.
- **Security and Error Handling:** The service currently implements no authentication and basic error handling. For production, consider integrating more robust, secure mechanisms (e.g., OAuth for authentication).
- **Items List Storage:** The items list is stored as a stringified JSON in the orders table instead of using a separate table. This simplifies the data model but can be a limitation if you need to perform complex queries on the items data.

## Assumptions

- **Order Processing Load:** The system is designed for a low-to-moderate order processing load only. As such, it is not optimized for handling very high volumes of concurrent orders. For production deployment at a large scale, optimizations (e.g., distributed queuing, database scaling) would be necessary.
- **Network and Database Connectivity:** The system assumes a stable and reliable network and database connectivity. In production environments, network failures and intermittent connectivity issues should be handled with appropriate retries, timeouts, and error handling to maintain robustness.
- **Order Processing Simulation:** The system uses a random sleep time as a proxy to simulate the duration of order processing in a real-world scenario.
