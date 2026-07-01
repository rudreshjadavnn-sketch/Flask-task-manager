from flask import Flask
from config import Config
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = Config.SECRET_KEY

from routes.page_routes import page_bp
from routes.auth_routes import auth_bp
from routes.task_routes import task_bp

app.register_blueprint(page_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)