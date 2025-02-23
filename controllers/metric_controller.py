from flask import Blueprint, jsonify

from services.metric_service import get_current_metrics

metric_bp = Blueprint("metric_bp", __name__)


@metric_bp.route("/metrics", methods=["GET"])
def get_metrics():
    """
    Endpoint to fetch key processing metrics:
        - Total number of completed orders.
        - Average processing time for orders.
        - Count of orders in each status (Pending, Processing, Completed).
    """
    return jsonify(get_current_metrics()), 200
