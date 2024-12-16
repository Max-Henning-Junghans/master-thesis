"""Main module for the system prototype."""
import argparse
import json
import logging
from pathlib import Path

from database.database import Database
from definitions.definitions import Definitions
from network_interface.network_interface import NetworkInterface
from rule_engine.rule_engine import RuleEngine
from scheduler.scheduler import Scheduler
from sensor_actor_interace.sensor_actor_interface import SensorActorInterface

logger = logging.getLogger(__name__)

def main() -> None:
    """Run the system prototype."""
    logging.basicConfig(encoding="utf-8", level=logging.INFO)
    args = parse_args()
    server_address = args.server_address
    config = args.config

    scheduler = Scheduler()
    rule_engine = RuleEngine()
    definitions = Definitions()
    network_interface = NetworkInterface()
    database = Database()
    sensor_actor_interface = SensorActorInterface()

    scheduler.setup(rule_engine)
    rule_engine.setup(
        scheduler,
        definitions,
        sensor_actor_interface,
        database,
        network_interface,
    )
    sensor_actor_interface.setup(database, definitions, network_interface)
    network_interface.setup(server_address, definitions, scheduler)
    if config:
        network_interface.configure_definitions(parse_json_file(config))
    else:
        success: bool = False
        while not success:
            try:
                network_interface.get_definitions()
                success = True
            except Exception as e:
                logger.error("Failed to get definitions")
        network_interface.get_definitions()
    scheduler.run()


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the system prototype.")
    parser.add_argument(
        "--server_address",
        type=str,
        required=True,
        help="Server address for the network interface."
    )
    parser.add_argument(
        "--config",
        type=str,
        required=False,
        help="Path to the configuration JSON file."
    )
    return parser.parse_args()


def parse_json_file(file_path: str) -> dict:
    """Parse a JSON file and return the data as a dictionary."""
    with Path(file_path).open(encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":
    main()
