import os
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
TEST_DATABASE_PATH = ROOT_DIR / "test_client_management.db"

os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DATABASE_PATH.as_posix()}"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
