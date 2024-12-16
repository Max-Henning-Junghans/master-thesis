"""Main module for the backend of the application.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""

from flask import Flask
from flask_cors import CORS

from api import api_bp


def create_app() -> Flask:
    """Create the Flask app."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.register_blueprint(api_bp)
    CORS(app)
    return app


def main() -> None:
    """Start the backend."""
    app = create_app()
    app.run(host="0.0.0.0")  # noqa: S104


if __name__ == "__main__":
    main()
