"""Main module for the external data sources.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""
import ast

import requests

mapping: dict[str: dict]
# This mapping is only an example for the prototype.
mapping = {
    "s_weather": {
        "type": "url",
        "url": r"https://api.open-meteo.com/v1/forecast?latitude=52.8342444419322&longitude=10.704168884802847&daily=precipitation_probability_max&timezone=Europe%2FBerlin&forecast_days=3",
        "keys": ["daily", "precipitation_probability_max"],
        "function": "max",
    }
}


def _get_data_url(mapping_data: dict) -> float:
    """Get the external data from a URL."""
    data = requests.get(mapping_data.get("url"),
                        headers={"Accept": "application/json"},
                        timeout=10)
    value = ast.literal_eval(data.content.decode("utf-8"))
    for key in mapping_data.get("keys"):
        value = value[key]
    match mapping_data.get("function"):
        case "max":
            return max(value)
        case _:
            raise NotImplementedError


def get_data(sensor_id: str) -> str:
    """Get the external data."""
    match mapping.get(sensor_id).get("type"):
        case "url":
            return str(_get_data_url(mapping.get(sensor_id)))
        case _:
            raise NotImplementedError
