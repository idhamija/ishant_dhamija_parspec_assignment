from flask import Flask

from config import Config
from controllers.metric_controller import metric_bp
from controllers.order_controller import order_bp
from models.db import db
from services.metric_service import initialise_metrics_dict
from services.order_service import start_order_processing


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    initialise_metrics_dict(app)
    start_order_processing(app)

    app.register_blueprint(order_bp)
    app.register_blueprint(metric_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(threaded=True, port=5000)
