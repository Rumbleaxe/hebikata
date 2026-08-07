"""
HebiKata - Exercise Data Loader

Loads exercise definitions from individual YAML files via the index registry.
Each exercise is stored as data/exercises/{ref}.yaml and referenced in
data/index.yaml.
"""

from pathlib import Path
from typing import Any

import streamlit as st
import yaml


def _data_dir() -> Path:
    return Path(__file__).parent.parent / "data"


@st.cache_data(show_spinner=False)
def load_exercises() -> list[dict[str, Any]]:
    """
    Load exercises from individual YAML files via index.yaml registry.

    Returns:
        Ordered list of exercise dictionaries. Invalid/missing files
        are logged and skipped so the app can degrade gracefully.

    Cached via ``@st.cache_data`` to avoid re-reading all YAML files
    on every Streamlit rerun.
    """
    data = _data_dir()
    index_path = data / "index.yaml"

    if not index_path.is_file():
        return []

    with open(index_path, encoding="utf-8") as f:
        index = yaml.safe_load(f)

    exercises: list[dict[str, Any]] = []
    for entry in index["exercises"]:
        ref = entry["ref"]
        ex_path = data / "exercises" / f"{ref}.yaml"
        try:
            with open(ex_path, encoding="utf-8") as f:
                exercises.append(yaml.safe_load(f))
        except (FileNotFoundError, yaml.YAMLError, KeyError) as e:
            st.error(f"Failed to load exercise `{ref}`: {e}")
            continue

    return exercises
