import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src'))

exec(open(project_root / 'src' / 'app' / 'app.py').read())

