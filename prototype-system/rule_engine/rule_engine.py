"""Rule Engine module.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""
import logging
import time

from database.database import Database
from definitions.definitions import Definitions
from definitions.rule.rule_action import (
    RuleAction,
    RuleActionActuate,
    RuleActionNotify,
    RuleActionSend,
    RuleActionSense,
)
from definitions.rule.rule_condition import ArgumentType, RuleArgument, RuleCondition
from definitions.rule.rule_condition_comparison_operator import RuleConditionComparisonOperator
from network_interface.network_interface import NetworkInterface
from scheduler.scheduler import Scheduler
from sensor_actor_interace.sensor_actor_interface import SensorActorInterface

logger = logging.getLogger(__name__)


class RuleEngine:
    """Rule Engine for the system."""

    scheduler: Scheduler
    definitions: Definitions
    sensor_actor_interface: SensorActorInterface
    database: Database
    network_interface: NetworkInterface

    def setup(self, scheduler: Scheduler,
              definitions: Definitions,
              sensor_actor_interface: SensorActorInterface,
              database: Database,
              network_interface: NetworkInterface) -> None:
        """Set up the rule engine."""
        self.scheduler = scheduler
        self.definitions = definitions
        self.sensor_actor_interface = sensor_actor_interface
        self.database = database
        self.network_interface = network_interface
        logger.info("Rule Engine set up")

    def execute_rule(self, rule_id: str) -> None:
        """Execute a rule."""
        try:
            rule = self.definitions.get_rule(rule_id)
            self.execute_elements(rule.rule_elements)
        except Exception:
            logger.error("Rule execution for rule %s failed", rule_id)

    def execute_elements(self, rule_elements: list[RuleCondition | RuleAction]) -> None:
        """Execute a list of rule elements."""
        for rule_element in rule_elements:
            if isinstance(rule_element, RuleCondition):
                self.execute_condition(rule_element)
            elif isinstance(rule_element, RuleAction):
                self.execute_action(rule_element)

    def execute_condition(self, condition: RuleCondition) -> None:
        """Execute the condition of a rule."""
        first_argument = self.evaluate_condition_argument(condition.first_argument)
        second_argument = self.evaluate_condition_argument(condition.second_argument)
        is_true: bool
        match condition.comparison_operator:
            case RuleConditionComparisonOperator.EQUAL:
                is_true = first_argument == second_argument
            case RuleConditionComparisonOperator.NOT_EQUAL:
                is_true = first_argument != second_argument
            case RuleConditionComparisonOperator.GREATER_THAN:
                is_true = first_argument > second_argument
            case RuleConditionComparisonOperator.LESS_THAN:
                is_true = first_argument < second_argument
            case RuleConditionComparisonOperator.GREATER_THAN_OR_EQUAL:
                is_true = first_argument >= second_argument
            case RuleConditionComparisonOperator.LESS_THAN_OR_EQUAL:
                is_true = first_argument <= second_argument
            case _:
                msg = "Invalid comparison operator"
                raise ValueError(msg)
        if is_true:
            self.execute_elements(condition.then_rule_elements)
        else:
            self.execute_elements(condition.else_rule_elements)

    def evaluate_condition_argument(self, argument: RuleArgument) -> float:
        """Evaluate a condition argument."""
        match argument.argument_type:
            case ArgumentType.CONSTANT:
                return float(argument.argument)
            case ArgumentType.SENSOR:
                return self.sensor_actor_interface.get_sensor_value(argument.argument)
            case ArgumentType.RANGE_MIN:
                raise NotImplementedError
            case ArgumentType.RANGE_MAX:
                raise NotImplementedError
            case ArgumentType.RANGE_AVERAGE:
                raise NotImplementedError

    def execute_action(self, action: RuleAction) -> None:
        """Execute the action of a rule."""
        match action:
            case RuleActionSense():
                self.execute_sense_action(action)
            case RuleActionActuate():
                self.execute_actuate_action(action)
            case RuleActionNotify():
                self.execute_notify_action(action)
            case RuleActionSend():
                self.execute_send_action(action)

    def execute_sense_action(self, action: RuleAction | RuleActionSense) -> None:
        """Execute a sense action."""
        self.sensor_actor_interface.get_sensor_value(action.sensor_id)

    def execute_actuate_action(self, action: RuleAction | RuleActionActuate) -> None:
        """Execute an actuate action."""
        self.sensor_actor_interface.trigger_actor(action.actor_id)

    def execute_notify_action(self, action: RuleAction | RuleActionNotify) -> None:
        """Execute a notify action."""
        self.network_interface.notify(action.text, action.priority)

    def execute_send_action(self, action: RuleAction | RuleActionSend) -> None:
        """Execute a send action."""
        type_id_values = {}
        for type_id in action.values_to_send:
            now = time.time()
            start_time = now - action.negative_time_offset_start
            end_time = now - action.negative_time_offset_end
            curr_value = self.database.retrieve_time_interval(type_id,
                                                              start_time,
                                                              end_time)
            type_id_values.update({type_id: curr_value})
        self.network_interface.send_data(type_id_values)
