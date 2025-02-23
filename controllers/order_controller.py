from flask import Blueprint, jsonify, request

from error import CustomError
from services.order_service import create_order, enqueue_order, get_order

order_bp = Blueprint("order_bp", __name__)


@order_bp.route("/orders", methods=["POST"])
def create_new_order():
    """
    Endpoint to create a new order.
    Accepts JSON payload with: user_id, item_ids, total_amount.
    Generates a unique order_id if not provided.
    The new order is added to the database with status 'Pending' and enqueued for processing.
    """

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input, JSON expected"}), 400

    try:
        create_order(data)
        enqueue_order(data["order_id"])
        return jsonify({"message": "Order received", "order_id": data["order_id"]}), 201
    except CustomError as e:
        return jsonify({"error": str(e)}), e.status_code


@order_bp.route("/orders/<string:order_id>", methods=["GET"])
def get_order_status(order_id):
    """
    Endpoint to fetch the current status and details of an order.
    """

    try:
        order = get_order(order_id)
        return jsonify(order), 200
    except CustomError as e:
        return jsonify({"error": str(e)}), e.status_code
