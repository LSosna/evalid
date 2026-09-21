"""Import guards. A missing dependency should name itself and its fix."""
from __future__ import annotations

_MSG = ("EVALID needs {pkg}. Install the pinned set with:\n"
        "    pip install -r requirements.txt\n"
        "or just this one with:\n"
        "    pip install '{spec}'")

try:
    import numpy as np
except ImportError as exc:                                  # pragma: no cover
    raise ImportError(_MSG.format(pkg="numpy >= 2.0 (np.trapezoid is used)",
                                  spec="numpy>=2.0")) from exc

if tuple(int(p) for p in np.__version__.split(".")[:2]) < (2, 0):  # pragma: no cover
    raise ImportError(
        f"EVALID needs numpy >= 2.0 (found {np.__version__}); np.trapezoid was "
        "added in 2.0. Install with: pip install 'numpy>=2.0'")


def require(name: str, spec: str | None = None):
    """Import `name`, or raise an ImportError that names the install command."""
    import importlib
    try:
        return importlib.import_module(name)
    except ImportError as exc:
        raise ImportError(_MSG.format(pkg=name, spec=spec or name)) from exc


__all__ = ["np", "require"]
