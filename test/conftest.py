import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cli import CliInterface
from storage import StorageManager


@pytest.fixture
def tmp_json_path(tmp_path: Path) -> Path:
    return tmp_path / "data" / "projects.json"


@pytest.fixture
def app(tmp_json_path: Path) -> CliInterface:
    a = CliInterface()
    a.storage = StorageManager(tmp_json_path)
    a.limpiar_pantalla = lambda: None
    return a