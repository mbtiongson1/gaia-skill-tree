import os
import sys

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, os.path.join(_REPO_ROOT, "src"))
sys.path.insert(0, _REPO_ROOT)

from gaia_cli.main import *  # noqa: F401,F403
from gaia_cli.main import main


if __name__ == "__main__":
    main()
