from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key-change-me"  # needed for flash messages

    from .game.routes import bp as game_bp
    app.register_blueprint(game_bp)

    return app
