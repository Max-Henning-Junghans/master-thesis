"""Sensor type module.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""
from enum import StrEnum


class SensorType(StrEnum):
    """Enumeration for sensor types."""

    I2C = "I2C"
    SPI = "SPI"
    UART = "UART"
    NETWORK = "network"
    OTHER = "other"
