from flask import Flask
from config import Config
from models import db
from routes import subcat_bp


def create_app():

    app = Flask(__name__)

    # Load base config
    app.config.from_object(Config)

    # ✅ SET AWS DATABASE (ims_db)
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.get_db_uri("ims_db")

    # Init DB (AFTER setting URI)
    db.init_app(app)

    # Register routes
    app.register_blueprint(subcat_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5002, debug=True)
