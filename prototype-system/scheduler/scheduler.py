"""Scheduler for the system.

TODO: Add more information about the module.
:author: Max Henning Junghans
"""
import logging
import time
from dataclasses import dataclass
from queue import PriorityQueue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rule_engine.rule_engine import RuleEngine

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Job:
    """Job for the scheduler."""

    rule_id: str
    schedule: float
    repeat_interval: float | None
    repeating: bool

    def __lt__(self, other: "Job") -> bool:
        """Compare jobs based on their schedule time."""
        return self.schedule < other.schedule


class Scheduler:
    """Scheduler for the system."""

    rule_queue = PriorityQueue()
    rule_engine: "RuleEngine"

    def setup(self, rule_engine: "RuleEngine") -> None:
        """TODO: Add more information about the method."""
        logger.info("Setting up the scheduler.")
        self.rule_engine = rule_engine

    def run(self) -> None:
        """TODO: Add more information about the method."""
        # TODO @Junghans: Add a thread to run the scheduler
        while True:
            if not self.rule_queue.empty():
                current_rule: Job = self.rule_queue.get()
                if current_rule.schedule <= time.time():
                    self._start_rule_execution(current_rule)
                else:
                    self.rule_queue.put(current_rule)

    def _start_rule_execution(self, current_rule: Job) -> None:
        """TODO: Add more information about the method."""
        if current_rule.repeating:
            logger.info(
                "Create repeating job for rule %s",
                current_rule.rule_id
            )
            self.create_job(
                current_rule.rule_id,
                current_rule.repeat_interval,
                current_rule.repeating,
            )
        logger.info("Executing rule %s", current_rule.rule_id)
        self.rule_engine.execute_rule(current_rule.rule_id)

    def create_job(
            self,
            rule_id: str,
            repeat_interval: float,
            repeating: bool,  # noqa: FBT001
    ) -> None:
        """Create a job for the scheduler.

        @param rule_id: The id of the rule to execute.
        @param repeat_interval: The interval to repeat the job.
        Only repeats if repeating is True.
        Is used to determine the first execution time.
        @param repeating: Whether the job should repeat.
        """
        logger.info(
            "Create job for rule %s with repeat_interval %s",
            rule_id,
            repeat_interval,
        )
        job = Job(
            rule_id,
            time.time() + repeat_interval,
            repeat_interval,
            repeating,
        )
        self.rule_queue.put(job)
