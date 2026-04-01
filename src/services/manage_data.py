import json
import os

from src.config.settings import (
    DATA_DIR,
    DEFAULT_DATA_FILE,
    KRITERIA_FILE,
    SMARTPHONES_FILE,
)
from src.models.criteria import Criteria
from src.models.smartphone import Smartphone

class DataManager:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)

    # Save smartphone list to JSON file
    def save_smartphones(self, smartphones: list):
        data = [sp.to_dict() for sp in smartphones]
        self._write_json(SMARTPHONES_FILE, data)

    # Load smartphone list from JSON file
    def load_smartphones(self) -> list:
        data = self._read_json(SMARTPHONES_FILE)
        if data is None:
            return []
        return [Smartphone.from_dict(item) for item in data]

    # Save criteria list to JSON file
    def save_criteria(self, criteria_list: list):
        data = [cr.to_dict() for cr in criteria_list]
        self._write_json(KRITERIA_FILE, data)

    # Load criteria list from JSON file
    def load_criteria(self) -> list:
        data = self._read_json(KRITERIA_FILE)
        if data is None:
            return []
        return [Criteria.from_dict(item) for item in data]

    # Load default data from journal (criteria + smartphones)
    def load_default_data(self) -> tuple:
        data = self._read_json(DEFAULT_DATA_FILE)
        if data is None:
            return [], []

        criteria_list = [Criteria.from_dict(item) for item in data.get("kriteria", [])]
        smartphone_list = [Smartphone.from_dict(item) for item in data.get("smartphones", [])]

        return criteria_list, smartphone_list

    # Reset all data to journal defaults
    def reset_to_default(self) -> tuple:
        criteria_list, smartphone_list = self.load_default_data()

        if criteria_list:
            self.save_criteria(criteria_list)
        if smartphone_list:
            self.save_smartphones(smartphone_list)

        return criteria_list, smartphone_list

    # Write data to JSON file
    def _write_json(self, filepath: str, data):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # Read data from JSON file, returns None if file doesn't exist
    def _read_json(self, filepath: str):
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    # Check if smartphone and criteria data files exist
    def is_data_available(self) -> bool:
        return (
            os.path.exists(SMARTPHONES_FILE)
            and os.path.exists(KRITERIA_FILE)
        )
