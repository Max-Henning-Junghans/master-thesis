"""Actor definition module.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""
from definitions.actor.actor_type import ActorType


class ActorDefinition:
    """Definition for a sensor."""

    name: str
    actor_type: ActorType

    def __init__(self, name: str, actor_type: ActorType) -> None:
        """Initialize the sensor definition."""
        self.name = name
        self.actor_type = actor_type
