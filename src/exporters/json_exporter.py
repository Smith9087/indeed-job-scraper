from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Any

class JsonExporter:
    def __init__(self, path: Path):
        self.path = Path(path)

    def write(self, rows: List[Dict[str, Any]]) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)