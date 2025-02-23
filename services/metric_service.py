import threading
from sqlalchemy.sql import func

from error import CustomError
from models.db import db
from models.metric import Metric
from models.order import Order
from models.enums.order_status import OrderStatus

metrics = {
    "avg_processing_time": 0.0,
    "total_orders": 0,
    "order_status_counts": {
        OrderStatus.PENDING: 0,
        OrderStatus.PROCESSING: 0,
        OrderStatus.COMPLETED: 0,
    },
}

metrics_lock = threading.Lock()


def initialise_metrics_dict(app):
    """
    Return the initial metrics dictionary.
    """
    with app.app_context():
        pending_order_count = get_status_count(OrderStatus.PENDING)
        processing_order_count = get_status_count(OrderStatus.PROCESSING)
        processed_order_count = get_status_count(OrderStatus.COMPLETED)
        avg_processing_time = get_average_processing_time()
    total_orders = pending_order_count + processing_order_count + processed_order_count

    global metrics
    metrics = {
        "avg_processing_time": avg_processing_time,
        "total_orders": total_orders,
        "order_status_counts": {
            OrderStatus.PENDING: pending_order_count,
            OrderStatus.PROCESSING: processing_order_count,
            OrderStatus.COMPLETED: processed_order_count,
        },
    }


def get_status_count(status):
    return Order.query.filter(Order.status == status).count()


def get_average_processing_time():
    """
    Return the average processing time for completed orders.
    """
    avg_time = (
        db.session.query(
            func.avg(
                (
                    func.julianday(Metric.processing_end_time)
                    - func.julianday(Metric.processing_start_time)
                )
                * 86400
            )
        )
        .filter(Metric.processing_end_time != None)
        .scalar()
    )
    return round(avg_time, 2) if avg_time else 0.0


def get_current_metrics():
    """
    Return the current metrics.
    """
    return metrics


def get_new_avg_processing_time(new_processing_time):
    """
    Return the new average processing time after processing a new order.
    """
    n = metrics["order_status_counts"][OrderStatus.COMPLETED]
    if n < 2:
        return new_processing_time

    new_avg_processing_time = (
        metrics["avg_processing_time"] * (n - 1) + new_processing_time
    ) / n
    return round(new_avg_processing_time, 2)


def update_metrics_on_order_submission():
    """
    Update metrics when a new order is submitted.
    """
    with metrics_lock:
        metrics["order_status_counts"][OrderStatus.PENDING] += 1
        metrics["total_orders"] += 1


def update_metrics_on_order_processing():
    """
    Update metrics when an order is being processed.
    """
    with metrics_lock:
        db.session.commit()
        metrics["order_status_counts"][OrderStatus.PENDING] -= 1
        metrics["order_status_counts"][OrderStatus.PROCESSING] += 1


def update_metrics_on_order_completion(processing_time):
    """
    Update metrics when an order is completed.
    """
    with metrics_lock:
        db.session.commit()
        metrics["order_status_counts"][OrderStatus.PROCESSING] -= 1
        metrics["order_status_counts"][OrderStatus.COMPLETED] += 1
        metrics["avg_processing_time"] = get_new_avg_processing_time(processing_time)
