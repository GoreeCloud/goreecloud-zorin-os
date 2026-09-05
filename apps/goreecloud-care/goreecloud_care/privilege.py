from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PrivilegedOutcome:
    completed: bool
    cancelled: bool
    message: str


def interpret_pkexec_result(returncode: int, stderr: str, action_label: str) -> PrivilegedOutcome:
    """Translate pkexec/helper completion into explicit user-facing state.

    pkexec reserves exit code 126 for a dismissed authentication dialog and 127
    for authorization/error cases where authorization was not obtained. Other
    non-zero values are treated as helper/action failures and never as success.
    """
    if returncode == 0:
        return PrivilegedOutcome(
            completed=True,
            cancelled=False,
            message=f"{action_label} completed successfully.",
        )

    if returncode == 126:
        return PrivilegedOutcome(
            completed=False,
            cancelled=True,
            message=(
                f"{action_label} was cancelled. The privileged maintenance command "
                "was not run, so GoreeCloud Care made no privileged changes."
            ),
        )

    detail = (stderr or "").strip()
    if returncode == 127:
        message = (
            f"{action_label} did not run because administrator authorization was not obtained "
            "or PolicyKit reported an error. No successful privileged change is claimed."
        )
    else:
        message = (
            f"{action_label} did not complete (exit status {returncode}). "
            "No successful privileged change is claimed."
        )

    if detail:
        message = f"{message} Details: {detail}"

    return PrivilegedOutcome(completed=False, cancelled=False, message=message)
