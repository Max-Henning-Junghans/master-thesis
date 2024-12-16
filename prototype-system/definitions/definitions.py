"""Definitions module.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""
import logging

from definitions.actor.actor_definition import ActorDefinition
from definitions.rule.rule_definition import RuleDefinition
from definitions.sensor.sensor_definition import SensorDefinition

logger = logging.getLogger(__name__)


class Definitions:
    """Definitions for the system."""

    rules: dict[str, RuleDefinition]
    sensors: dict[str, SensorDefinition]
    actors: dict[str, ActorDefinition]

    def __init__(self) -> None:
        """Initialize the definitions."""
        # TODO @Junghans: Add load from file
        logger.info("Setups empty definitions")
        self.rules = {}
        self.sensors = {}
        self.actors = {}

    def configure_definitions(self,
                              rules: dict[str, RuleDefinition],
                              sensors: dict[str, SensorDefinition],
                              actors: dict[str, ActorDefinition]) -> None:
        """Configure the definitions."""
        logger.info("Configuring definitions")
        self.rules = rules
        self.sensors = sensors
        self.actors = actors

    def get_rule(self, rule_id: str) -> RuleDefinition:
        """Get a rule by its ID."""
        logger.info("Getting rule with ID %s", rule_id)
        return self.rules[rule_id]

    def get_sensor(self, sensor_id: str) -> SensorDefinition:
        """Get a sensor by its ID."""
        logger.info("Getting sensor with ID %s", sensor_id)
        return self.sensors[sensor_id]

    def get_actor(self, actor_id: str) -> ActorDefinition:
        """Get an actor by its ID."""
        logger.info("Getting actor with ID %s", actor_id)
        return self.actors[actor_id]
