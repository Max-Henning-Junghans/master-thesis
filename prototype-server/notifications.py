"""Main module for the notifications of the server.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""

from enum import Enum, StrEnum


class Priority(StrEnum):
    """An enum to represent the different notification priorities."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class NotificationTarget(Enum):
    """An enum to represent the different notification targets."""

    CONSOLE = 0
    EMAIL = 1
    SMS = 2
    PUSH = 3


notification_target_mapping: dict[Priority, NotificationTarget] = {
    Priority.INFO: NotificationTarget.CONSOLE,
    Priority.LOW: NotificationTarget.EMAIL,
    Priority.MEDIUM: NotificationTarget.SMS,
    Priority.HIGH: NotificationTarget.PUSH,
}


notification_target_mapping: dict[Priority: NotificationTarget]


def send_console(message: str, priority: Priority) -> None:
    """Send a notification to the console."""
    print(f"Sending console notification of priority {priority}:\n{message}")


def send_email(message: str, priority: Priority) -> None:  # noqa: ARG001
    """Send a notification via email."""
    raise NotImplementedError


def send_sms(message: str, priority: Priority) -> None:  # noqa: ARG001
    """Send a notification via SMS."""
    raise NotImplementedError


def send_push(message: str, priority: Priority) -> None:  # noqa: ARG001
    """Send a notification via push notification."""
    raise NotImplementedError


def send(message: str, priority: Priority) -> None:
    """Send a notification based on the priority."""
    match notification_target_mapping[priority]:
        case NotificationTarget.CONSOLE:
            send_console(message, priority)
        case NotificationTarget.EMAIL:
            send_email(message, priority)
        case NotificationTarget.SMS:
            send_sms(message, priority)
        case NotificationTarget.PUSH:
            send_push(message, priority)
        case _:
            raise NotImplementedError
