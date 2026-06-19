"""
HebiKata - Exercise Data Loader

Loads exercise definitions from individual YAML files via the index registry.
Each exercise is stored as data/exercises/{ref}.yaml and referenced in
data/index.yaml.
"""

from pathlib import Path
from typing import Any

import yaml


def _data_dir() -> Path:
    return Path(__file__).parent.parent / "data"


def load_exercises() -> list[dict[str, Any]]:
    """
    Load exercises from individual YAML files via index.yaml registry.

    Returns:
        List[Dict[str, Any]]: Ordered list of exercise dictionaries.
    """
    data = _data_dir()
    index_path = data / "index.yaml"
    with open(index_path, encoding="utf-8") as f:
        index = yaml.safe_load(f)
    exercises = []
    for entry in index["exercises"]:
        ref = entry["ref"]
        ex_path = data / "exercises" / f"{ref}.yaml"
        with open(ex_path, encoding="utf-8") as f:
            exercises.append(yaml.safe_load(f))
    return exercises
