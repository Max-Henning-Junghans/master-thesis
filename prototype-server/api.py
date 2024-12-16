"""Main module for the api of the server.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""

from flask import Blueprint, request

import database
import external
import notifications

api_bp = Blueprint("/", __name__)


@api_bp.route("/notifications", methods=["POST"])
def notifications_api() -> str:
    """Trigger the notifications."""
    message = request.json["message"]
    priority = request.json["priority"]
    notifications.send(message, priority)
    return "OK"


@api_bp.route("/external/<sensor_id>", methods=["GET"])
def external_get(sensor_id: str) -> str:
    """Return the external data."""
    return external.get_data(sensor_id)


@api_bp.route("/measurements", methods=["GET"])
def measurements_get() -> dict[str, list[tuple[float, float]]]:
    """Return the measurements."""
    return database.measurements

@api_bp.route("/measurements", methods=["POST"])
def measurements_post() -> str:
    """Trigger the notifications."""
    data = request.json
    database.merge_database(data)
    return "OK"


@api_bp.route("/definitions", methods=["GET"])
def definitions_get() -> None | dict | str:
    """Return the definitions."""
    return database.definitions


@api_bp.route("/definitions", methods=["POST"])
def definitions_post() -> None | dict | str:
    """Return the definitions."""
    database.definitions = request.json
    return "OK"

