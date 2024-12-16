"""Sensor definition module.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""
from dataclasses import dataclass

from definitions.sensor.sensor_type import SensorType


@dataclass(frozen=True)
class SensorDefinition:
    """Definition for a sensor."""

    name: str
    sensor_type: SensorType


@dataclass(frozen=True)
class I2CAction:
    """Action for an I2C sensor."""

    i2c_type: str
    message: list[int | float]
    length: int


@dataclass(frozen=True)
class SensorDefinitionI2C(SensorDefinition):
    """Definition for an I2C sensor."""

    i2c_address: int
    actions: list[I2CAction]
    factor: float
    offset: float
    msb_first: bool
