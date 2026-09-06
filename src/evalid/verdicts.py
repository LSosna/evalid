"""The EVALID verdict lattice, frozen at protocol 0.3.2.

The lattice is closed: an audit may not emit a verdict string outside it.
This module is the single source of truth, and every writer path in the
package validates against it.
"""
from __future__ import annotations

PROTOCOL_VERSION = "0.3.2"

#: Per-prediction verdicts (protocol §3.1).
PREDICTION_VERDICTS = frozenset({
    "PASS",
    "FAIL",
    "INDETERMINATE",        # new in 0.3.2 -- inside the threshold uncertainty band
    "UNDERDETERMINED",      # new in 0.3.2 -- failed the numerical admissibility gate
    "REGISTERED_INVALID",   # registered, criterion unsound, superseded
    "NOT_RUN",
})

#: Terminal audit verdicts (protocol §3.2).
TERMINAL_VERDICTS = frozenset({
    "IDENTIFIED",
    "DETECTED-BUT-NOT-IDENTIFIED",
    "LOCALIZED",
    "NONE",
    "ARTIFACT",
})

#: Spellings retired in 0.3.2, mapped to their replacement.
DEPRECATED = {
    "CRITERION INVALID": "REGISTERED_INVALID",
    "CRITERION_INVALID": "REGISTERED_INVALID",
}


class VerdictError(ValueError):
    """Raised when a verdict string is outside the frozen lattice."""


def check_prediction(verdict: str) -> str:
    """Return `verdict` if it is a legal per-prediction verdict, else raise.

    Deprecated spellings raise with the replacement named, rather than being
    silently accepted -- vocabulary drift is how a standard stops being one.
    """
    if verdict in PREDICTION_VERDICTS:
        return verdict
    if verdict in DEPRECATED:
        raise VerdictError(
            f"{verdict!r} was retired in protocol {PROTOCOL_VERSION}; "
            f"use {DEPRECATED[verdict]!r}."
        )
    raise VerdictError(
        f"{verdict!r} is not in the EVALID {PROTOCOL_VERSION} prediction lattice. "
        f"Legal values: {sorted(PREDICTION_VERDICTS)}"
    )


def check_terminal(verdict: str) -> str:
    """Return `verdict` if it is a legal terminal audit verdict, else raise."""
    if verdict in TERMINAL_VERDICTS:
        return verdict
    raise VerdictError(
        f"{verdict!r} is not in the EVALID {PROTOCOL_VERSION} terminal lattice. "
        f"Legal values: {sorted(TERMINAL_VERDICTS)}"
    )
