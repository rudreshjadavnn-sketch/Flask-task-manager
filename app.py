from flask import Flask
from config import Config

app = Flask(__name__)

app.config["SECRET_KEY"] = Config.SECRET_KEY

from routes.page_routes import page_bp
from routes.auth_routes import auth_bp
from routes.task_routes import task_bp

app.register_blueprint(page_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)