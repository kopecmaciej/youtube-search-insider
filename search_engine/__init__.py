## Loads the shared directory into the path so that the shared modules can be imported
import sys

from pathlib import Path

current_dir = Path(__file__).resolve().parent
print(current_dir)
project_dir = current_dir.parent.parent
print(project_dir)

sys.path.append(str(project_dir))
