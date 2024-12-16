"""Rule Action module.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class RuleAction:
    """Action for a rule."""

    name: str


@dataclass(frozen=True)
class RuleActionSense(RuleAction):
    """Sense action for a rule."""

    sensor_id: str


@dataclass(frozen=True)
class RuleActionActuate(RuleAction):
    """Actuate action for a rule."""

    actor_id: str


@dataclass(frozen=True)
class RuleActionNotify(RuleAction):
    """Notify action for a rule."""

    text: str
    priority: str


@dataclass(frozen=True)
class RuleActionSend(RuleAction):
    """Send action for a rule."""

    values_to_send: list[str] | None  # List of type ids
    negative_time_offset_start: int
    negative_time_offset_end: int
