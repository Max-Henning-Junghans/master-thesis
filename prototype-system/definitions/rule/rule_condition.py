"""Rule condition module.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""
from dataclasses import dataclass
from enum import StrEnum
from typing import Self

from definitions.rule.rule_action import RuleAction
from definitions.rule.rule_condition_comparison_operator import RuleConditionComparisonOperator


class ArgumentType(StrEnum):
    """Enumeration for argument types."""

    CONSTANT = "constant"
    SENSOR = "sensor"
    RANGE_MIN = "range_min"
    RANGE_MAX = "range_max"
    RANGE_AVERAGE = "range_average"

@dataclass
class RuleArgument:
    """Argument for a rule."""

    argument: str | int | float
    argument_type: ArgumentType
    start_time_difference: int | float | None
    end_time_difference: int | float | None


@dataclass(frozen=True)
class RuleCondition:
    """Condition for a rule."""

    name: str
    first_argument: RuleArgument
    comparison_operator: RuleConditionComparisonOperator
    second_argument: RuleArgument
    then_rule_elements: list[Self | RuleAction] | None
    else_rule_elements: list[Self | RuleAction] | None
