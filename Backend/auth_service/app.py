from flask import Flask
from config import Config
from models import db
from routes import auth_bp


def create_app():

    app = Flask(__name__)

    print("DEBUG: Config class =", Config)
    print("DEBUG: get_db_uri =", hasattr(Config, "get_db_uri"))

    # Try to get URI
    try:
        uri = Config.get_db_uri("auth_db")
        print("DEBUG: DB URI =", uri)
    except Exception as e:
        print("DEBUG ERROR:", e)
        uri = None


    app.config["SQLALCHEMY_DATABASE_URI"] = uri

    print("DEBUG: App DB URI =", app.config.get("SQLALCHEMY_DATABASE_URI"))

    db.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
