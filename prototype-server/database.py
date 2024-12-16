"""Main module for the database of the server.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""


measurements: dict[str, list[tuple[float, float]]]
definitions: str

definitions = ""

measurements = {}


def merge_database(
        database: dict[str, list[tuple[float, float]]]
) -> None:
    """Merge the database with the given data."""
    for type_id, measurement_list in database.items():
        for measure_time, value in measurement_list:
            if measure_time not in [entry[0]
                                    for entry
                                    in measurements.get(type_id, [])
                                    ]:
                if type_id not in measurements:
                    measurements[type_id] = []
                measurements.get(type_id).append((measure_time, value))
