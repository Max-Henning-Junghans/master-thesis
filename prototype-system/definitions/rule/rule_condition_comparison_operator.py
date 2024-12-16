"""Rule condition comparison operator module.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""
from enum import StrEnum


class RuleConditionComparisonOperator(StrEnum):
    """Enumeration for rule condition comparison operators."""

    EQUAL = "equal"
    NOT_EQUAL = "not equal"
    GREATER_THAN = "greater than"
    GREATER_THAN_OR_EQUAL = "greater than or equal"
    LESS_THAN = "less than"
    LESS_THAN_OR_EQUAL = "less than or equal"
