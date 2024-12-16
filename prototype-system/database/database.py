"""Database module.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""
import logging
from copy import deepcopy

logger = logging.getLogger(__name__)


class Database:
    """Database for the system."""

    database: dict[str, list[tuple[float, float]]]

    def __init__(self) -> None:
        """Initialize the database."""
        self.database = {}

    def store(self, type_id: str, measure_time: float, value: float) -> None:
        """Store a value in the database."""
        if type_id not in self.database:
            self.database[type_id] = []
        self.database[type_id].append((measure_time, value))

    def retrieve_entry(self, type_id: str, measure_time: float) -> tuple[float, float]:
        """Retrieve a value from the database."""
        for entry in self.database.get(type_id, []):
            if entry[0] == measure_time:
                return deepcopy(entry)
        msg = (f"No entry found for type_id {type_id} "
               f"at measure_time {measure_time}")
        raise KeyError(msg)

    def retrieve_all_for_type(self, type_id: str) -> list[tuple[float, float]]:
        """Retrieve all values for a sensor from the database."""
        return deepcopy(self.database.get(type_id, []))

    def retrieve_time_interval(self, type_id: str, start_time: float, end_time: float) -> list[tuple[float, float]]:
        """Retrieve all values for a type from the database within a time interval."""
        return deepcopy([entry
                         for entry in self.database.get(type_id, [])
                         if start_time <= entry[0] <= end_time])

    def retrieve_all(self) -> dict[str, list[tuple[float, float]]]:
        """Retrieve all values from the database."""
        return deepcopy(self.database)
