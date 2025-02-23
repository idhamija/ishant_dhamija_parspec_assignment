from datetime import datetime, timezone

from models.db import db


class Metric(db.Model):
    __tablename__ = "metrics"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), db.ForeignKey("orders.order_id"))
    processing_start_time = db.Column(db.DateTime, nullable=True)
    processing_end_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def to_dict(self):
        """Helper method to serialize the order to a dictionary."""
        return {
            "order_id": self.order_id,
            "processing_start_time": (
                self.processing_start_time.isoformat()
                if self.processing_start_time
                else None
            ),
            "processing_end_time": (
                self.processing_end_time.isoformat()
                if self.processing_end_time
                else None
            ),
            "created_at": self.created_at.isoformat(),
        }
