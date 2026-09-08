from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
for script in ("generate_management.py", "generate_types.py"):
    subprocess.run([sys.executable, str(ROOT / script)], check=True)
