from datetime import datetime, timezone
import json
import logging
import os
import queue
import random
import threading
import time

from error import CustomError
from models.db import db
from models.metric import Metric
from models.order import Order
from models.enums.order_status import OrderStatus
from services.metric_service import (
    update_metrics_on_order_completion,
    update_metrics_on_order_processing,
    update_metrics_on_order_submission,
)

order_queue = queue.Queue()


def enqueue_order(order_id):
    """
    Enqueue an order for processing.
    """
    order_queue.put(order_id)


def create_order(order_data):
    """
    Create a new order in the database.
    """
    order = (
        db.session.query(Order).filter(Order.order_id == order_data["order_id"]).first()
    )
    if order:
        raise CustomError(f"Order {order_data['order_id']} already exists", 400)

    required_fields = ("user_id", "order_id", "item_ids", "total_amount")
    if not all(field in order_data for field in required_fields):
        raise CustomError("Missing required fields", 400)

    order_id = order_data["order_id"]
    user_id = order_data["user_id"]

    try:
        item_ids = json.dumps(order_data["item_ids"])
    except Exception:
        raise CustomError("Invalid format for item_ids", 400)

    total_amount = order_data["total_amount"]

    new_order = Order(
        order_id=order_id,
        user_id=user_id,
        item_ids=item_ids,
        total_amount=total_amount,
        status=OrderStatus.PENDING,
    )
    db.session.add(new_order)

    metric = Metric(order_id=order_id)
    db.session.add(metric)

    db.session.commit()

    update_metrics_on_order_submission()


def get_order(order_id):
    """
    Retrieve an order by order_id.
    """
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        raise CustomError(f"Order {order_id} not found", 404)
    return order.to_dict()


def process_order(order):
    """
    Simulate processing of an order.
    Update the order's status from 'Pending' to 'Processing' to 'Completed',
    and record the processing time.
    """
    metric = order.metrics

    start_time = metric.processing_start_time = datetime.now(timezone.utc)
    order.status = OrderStatus.PROCESSING
    update_metrics_on_order_processing()

    # This is used as proxy for the time taken to process the order in real world scenarios
    time.sleep(random.uniform(1, 3))

    end_time = metric.processing_end_time = datetime.now(timezone.utc)
    order.status = OrderStatus.COMPLETED    
    processing_time = (end_time - start_time).total_seconds()
    update_metrics_on_order_completion(processing_time)


def process_orders(app):
    """
    Process orders from the queue.
    """

    while True:
        order_id = order_queue.get()
        with app.app_context():
            try:
                order = Order.query.filter_by(order_id=order_id).first()
                process_order(order)
            except Exception as e:
                logging.ERROR(f"Error processing order {order_id}: {e}")
                db.session.rollback()
            finally:
                order_queue.task_done()


def start_order_processing(app):
    """
    Start the order processing service.
    """
    for _ in range(min(32, os.cpu_count() + 4)):
        order_processing_thread = threading.Thread(
            target=process_orders, args=(app,), daemon=True
        )
        order_processing_thread.start()
