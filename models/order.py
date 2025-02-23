from datetime import datetime, timezone

from models.db import db
from models.enums.order_status import OrderStatus


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.String(50), nullable=False)
    item_ids = db.Column(db.String(255), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    metrics = db.relationship("Metric", backref="order", uselist=False)

    def to_dict(self):
        """Helper method to serialize the order to a dictionary."""
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "item_ids": self.item_ids,
            "total_amount": self.total_amount,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.created_at.isoformat(),
        }
