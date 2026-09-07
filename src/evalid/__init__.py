"""EVALID -- a pre-registered identifiability protocol.

Protocol spec: protocol/EVALID_v0.3.4.md
"""
from .verdicts import (PROTOCOL_VERSION, PREDICTION_VERDICTS, TERMINAL_VERDICTS,
                       check_prediction, check_terminal, VerdictError)
from .stats import (threshold_verdict, uncertainty_from_spread,
                    implementation_spread, condition_gate, safe_inverse,
                    benjamini_hochberg, cluster_bootstrap_ci, detection_limit,
                    DEFAULT_COND_CEILING, UNCERTAINTY_METHODS)
from . import anchors, manifest, corrections

__version__ = "0.3.6"
__all__ = [
    "PROTOCOL_VERSION", "PREDICTION_VERDICTS", "TERMINAL_VERDICTS",
    "check_prediction", "check_terminal", "VerdictError",
    "threshold_verdict", "uncertainty_from_spread", "implementation_spread",
    "condition_gate", "safe_inverse", "benjamini_hochberg",
    "cluster_bootstrap_ci", "detection_limit",
    "DEFAULT_COND_CEILING", "UNCERTAINTY_METHODS",
    "anchors", "manifest", "corrections", "__version__",
]
