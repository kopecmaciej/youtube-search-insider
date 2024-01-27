## Loads the shared directory into the path so that the shared modules can be imported
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
project_dir = current_dir.parent

sys.path.append(str(project_dir))
