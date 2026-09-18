"""The shape of a verification pass, shared by every writer.

Nothing a writer produces reaches disk on the writer's own say-so: the bytes are read
back with an independent reader and checked against the plan that produced them. Both
formats do that, so the report they fill in lives here rather than in either of them.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class VerificationReport:
    """What verification found. ``ok`` is the only thing callers must check."""

    checks: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures

    def check(self, description: str, condition: bool, detail: str = "") -> None:
        self.checks.append(description)
        if not condition:
            self.failures.append(f"{description}: {detail}" if detail else description)
