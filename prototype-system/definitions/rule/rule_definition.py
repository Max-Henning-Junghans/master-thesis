"""Rule definition module.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""
from dataclasses import dataclass

from definitions.rule.rule_action import RuleAction
from definitions.rule.rule_condition import RuleCondition


@dataclass(frozen=True)
class RuleDefinition:
    """Definition for a rule."""

    name: str
    rule_id: str
    rule_elements: list[RuleCondition | RuleAction]
    repeat_interval: float | None
    repeating: bool
