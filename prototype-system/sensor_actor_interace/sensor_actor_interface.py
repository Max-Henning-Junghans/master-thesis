"""Interface for connected sensors and actors.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""
import logging
import time

from smbus2 import SMBus, i2c_msg

from database.database import Database
from definitions.definitions import Definitions
from definitions.sensor.sensor_definition import SensorDefinitionI2C
from definitions.sensor.sensor_type import SensorType
from network_interface.network_interface import NetworkInterface

logger = logging.getLogger(__name__)


class SensorActorInterface:
    """Interface for connected sensors and actors."""

    database: Database
    definitions: Definitions
    network_interface: NetworkInterface

    def setup(self,
              database: Database,
              definitions: Definitions,
              network_interface: NetworkInterface) -> None:
        """Set up the interface."""
        self.database = database
        self.definitions = definitions
        self.network_interface = network_interface
        logger.info("SensorActorInterface setup")

    def trigger_actor(self, actor_id: str) -> None:
        """Trigger an actor."""
        actor = self.definitions.get_actor(actor_id)
        match actor.actor_type:
            case _:  # TODO @Junghans: Implement the actor triggering
                pass

    def get_sensor_value(self, sensor_id: str) -> float:
        """Get the value of a sensor."""
        sensor = self.definitions.get_sensor(sensor_id)
        logger.info(
            "Getting sensor value for %s of type %s",
            sensor_id,
            sensor.sensor_type
        )
        measurement: float
        match sensor.sensor_type:
            case SensorType.NETWORK:
                measurement = self._handle_network_sensor(sensor_id)
            case SensorType.I2C:
                measurement = self._handle_i2c(sensor)
            case _:
                logger.error("Sensor type not implemented")
                raise NotImplementedError
        now = time.time()
        self.database.store(sensor_id, now, measurement)
        return measurement

    def _handle_network_sensor(self, sensor_id: str) -> float:
        """Handle a network sensor."""
        return self.network_interface.request_data(sensor_id)

    def _handle_i2c(self, sensor: SensorDefinitionI2C) -> float:
        """Handle an I2C sensor."""
        logger.info("Handling I2C sensor %s", sensor.name)
        result: list = [0]
        with SMBus(1) as bus:
            for action in sensor.actions:
                match action.i2c_type:
                    case "read":
                        result = bus.read_i2c_block_data(sensor.i2c_address,
                                                          action.message[0],
                                                          action.length)
                    case "write":
                        msg1 = i2c_msg.write(sensor.i2c_address,
                                             action.message)
                        bus.i2c_rdwr(msg1)
                    case "sleep":
                        time.sleep(action.message[0])
        return (self._concatenate_binary(result, sensor.msb_first)
                * sensor.factor
                + sensor.offset)

    @staticmethod
    def _concatenate_binary(int_list: list[int], msb_first: bool) -> int:
        binary_strings = [format(x, "08b") for x in int_list]
        if not msb_first:
            binary_strings.reverse()
        concatenated_binary = "".join(binary_strings)
        return int(concatenated_binary, 2)

