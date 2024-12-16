"""Network Interface for the system.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""
import json
import logging
from typing import TYPE_CHECKING

import requests

from definitions.definitions import Definitions
from network_interface import parser
from scheduler.scheduler import Scheduler

if TYPE_CHECKING:
    from definitions.rule.rule_definition import RuleDefinition

logger = logging.getLogger(__name__)


class NetworkInterface:
    """Network Interface for the system."""

    server: str
    definitions: Definitions
    scheduler: Scheduler

    def setup(self,
              server: str,
              definitions: Definitions,
              scheduler: Scheduler) -> None:
        """Set up the network interface."""
        self.server = server
        self.definitions = definitions
        self.scheduler = scheduler
        logger.info("Network Interface setup")

    def send_data(self, data: dict) -> None:
        """Send data."""
        logger.info("Sending data")
        url = f"{self.server}/measurements"
        requests.post(url, json=data, timeout=10)

    def request_data(self, sensor_id: str) -> float:
        """Request data from external data source."""
        logger.info("Requesting data")
        url = f"{self.server}/external/{sensor_id}"
        value = requests.request("GET", url, timeout=10).text
        return float(value)

    def notify(self, text: str, priority: str) -> None:
        """Notify the user."""
        logger.info("Notifying user of %s with %s", text, priority)
        url = f"{self.server}/notifications"
        payload = {
            "message": text,
            "priority": priority
        }
        requests.post(url, json=payload, timeout=10)

    def configure_definitions(self, definitions: dict) -> None:
        """Configure the definitions."""
        logger.info("Configuring definitions")
        rules, sensors, actors = parser.parse_definitions(definitions)
        rule_id: str
        rule_values: RuleDefinition
        for rule_id, rule_values in rules.items():
            self.scheduler.create_job(
                rule_id,
                rule_values.repeat_interval,
                rule_values.repeating,
            )
        self.definitions.configure_definitions(rules,
                                               sensors,
                                               actors)

    def get_definitions(self) -> None:
        """Get the definitions."""
        logger.info("Getting definitions from server")
        url = f"{self.server}/definitions"
        definitions = requests.request("GET", url, timeout=10).text
        self.configure_definitions(json.loads(definitions))
