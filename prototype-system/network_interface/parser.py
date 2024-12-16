"""Parser module.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""
import logging

from definitions.rule.rule_action import (
    RuleAction,
    RuleActionActuate,
    RuleActionNotify,
    RuleActionSend,
    RuleActionSense,
)
from definitions.rule.rule_condition import ArgumentType, RuleArgument, RuleCondition
from definitions.rule.rule_definition import RuleDefinition
from definitions.sensor.sensor_definition import I2CAction, SensorDefinition, SensorDefinitionI2C
from definitions.sensor.sensor_type import SensorType

logger = logging.getLogger(__name__)


def parse_definitions(definitions: dict) -> tuple[dict, dict, dict]:
    """Parse the definitions."""
    logger.info("Parsing the definitions.")
    unparsed_rules = definitions.get("rules", {})
    unparsed_sensors = definitions.get("sensors", {})
    unparsed_actors = definitions.get("actors", {})
    rules = _parse_rules(unparsed_rules)
    sensors = _parse_sensors(unparsed_sensors)
    actors = _parse_actors(unparsed_actors)
    return rules, sensors, actors

########################################################################
# Parse the rules                                                      #
########################################################################


def _parse_rules(unparsed_rules: dict) -> dict:
    """Parse the rules."""
    rules = {}
    for rule_id, unparsed_rule in unparsed_rules.items():
        x = [_parse_rule(rule) for rule in unparsed_rule["elements"]]
        rules[rule_id] = RuleDefinition(
            unparsed_rule["name"],
            rule_id,
            x,
            unparsed_rule.get("repeat_interval"),
            unparsed_rule.get("repeating")
        )
    return rules


def _parse_rule(unparsed_rule: dict) -> RuleCondition | RuleAction:
    """Parse a rule."""
    match unparsed_rule["type"]:
        case "condition":
            return _parse_condition(unparsed_rule)
        case "action":
            return _parse_action(unparsed_rule)
        case _:
            raise NotImplementedError


def _parse_condition(unparsed_condition: dict) -> RuleCondition:
    """Parse the condition."""
    first_argument = _parse_condition_argument(unparsed_condition["first_argument"])
    second_argument = _parse_condition_argument(unparsed_condition["second_argument"])
    then_ele = unparsed_condition.get("then")
    then_rule_elements = [_parse_rule(rule)
                          for rule in then_ele] if then_ele else None
    else_ele = unparsed_condition.get("else")
    else_rule_elements = [_parse_rule(rule)
                          for rule in else_ele] if else_ele else None
    return RuleCondition(unparsed_condition["name"],
                         first_argument,
                         unparsed_condition["comparison_operator"],
                         second_argument,
                         then_rule_elements,
                         else_rule_elements)


def _parse_action(unparsed_action: dict) -> RuleAction:
    """Parse the action."""
    match unparsed_action["action_type"]:
        case "sense":
            return RuleActionSense(unparsed_action["name"],
                                   unparsed_action["sensor_id"])
        case "actuate":
            return RuleActionActuate(unparsed_action["name"],
                                     unparsed_action["actor_id"])
        case "notify":
            return RuleActionNotify(unparsed_action["name"],
                                    unparsed_action["text"],
                                    unparsed_action["priority"])
        case "send":
            return RuleActionSend(unparsed_action["name"],
                                  unparsed_action["values_to_send"],
                                  unparsed_action["negative_time_offset_start"],
                                  unparsed_action["negative_time_offset_end"])
        case _:
            raise NotImplementedError


def _parse_condition_argument(unparsed_argument: dict) -> RuleArgument:
    """Parse the condition argument."""
    match unparsed_argument["type"]:
        case ArgumentType.CONSTANT | ArgumentType.SENSOR:
            return RuleArgument(unparsed_argument["argument"],
                                unparsed_argument["type"],
                                None,
                                None)
        case (ArgumentType.RANGE_MIN |
              ArgumentType.RANGE_MAX |
              ArgumentType.RANGE_AVERAGE):
            start = unparsed_argument.get("start_time_difference")
            end = unparsed_argument.get("end_time_difference")
            return RuleArgument(unparsed_argument["argument"],
                                unparsed_argument["type"],
                                start,
                                end)
        case _:
            raise NotImplementedError

########################################################################
# Parse the sensors                                                    #
########################################################################


def _parse_sensors(unparsed_sensors: dict) -> dict:
    """Parse the sensors."""
    parsed_sensors = {}
    for sensor_id, sensor in unparsed_sensors.items():
        match sensor.get("type"):
            case SensorType.I2C:
                parsed_sensor = _parse_sensor_i2c(sensor)
            case SensorType.SPI:
                parsed_sensor = _parse_sensor_spi(sensor)
            case SensorType.UART:
                parsed_sensor = _parse_sensor_uart(sensor)
            case SensorType.NETWORK:
                parsed_sensor = _parse_sensor_network(sensor)
            case SensorType.OTHER:
                parsed_sensor = _parse_sensor_other(sensor)
            case _:
                raise NotImplementedError
        parsed_sensors[sensor_id] = parsed_sensor
    return parsed_sensors


def _parse_sensor_i2c(sensor: dict) -> SensorDefinitionI2C:
    """Parse an I2C sensor."""
    parsed_actions = [
        I2CAction(action["type"],
                  [parse_string_to_int(i) for i in action["data"]],
                  action["length"])
        for action in sensor["actions"]
    ]
    return SensorDefinitionI2C(sensor["name"],
                               sensor["type"],
                               parse_string_to_int(sensor["i2c_address"]),
                               parsed_actions,
                               sensor["factor"],
                               sensor["offset"],
                               sensor["msb_first"])


def parse_string_to_int(s: str) -> int:
    """Parse a string to an integer.

    The method considers base 2, base 10, or base 16.
    """
    if s.startswith("0b"):
        return int(s, 2)
    if s.startswith("0x"):
        return int(s, 16)
    return int(s, 10)


def _parse_sensor_spi(sensor: dict):
    """Parse an SPI sensor."""
    raise NotImplementedError


def _parse_sensor_uart(sensor: dict):
    """Parse a UART sensor."""
    raise NotImplementedError


def _parse_sensor_network(sensor: dict):
    """Parse a network sensor."""
    return SensorDefinition(sensor["name"], sensor["type"])


def _parse_sensor_other(sensor: dict):
    """Parse an other sensor."""
    raise NotImplementedError

########################################################################
# Parse the actors                                                     #
########################################################################


def _parse_actors(unparsed_actors: dict) -> dict:
    """Parse the actors."""
    actors = {}
    return actors

